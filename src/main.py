import argparse
import json
import os
import sys
from collections import Counter
from constants import BOARD_SIZE, FPS_DEFAULT, SNAKE_START_LENGTH
from environment import Board
from interpreter import Interpreter
from display import Display
from agent import Agent


# toutes options d'arg possibles
def parse_args():
    p = argparse.ArgumentParser(prog='snake')
    p.add_argument('-sessions', type=int, default=1,
                   metavar='N')
    p.add_argument('-save', type=str, default=None,
                   metavar='PATH')
    p.add_argument('-load', type=str, default=None,
                   metavar='PATH')
    p.add_argument('-visual', choices=['on', 'off'], default='on')
    p.add_argument('-dontlearn', action='store_true')
    p.add_argument('-step-by-step', action='store_true',
                   dest='step_by_step')
    p.add_argument('-board-size', type=int, default=BOARD_SIZE,
                   dest='board_size', metavar='N')
    p.add_argument('-speed', type=int, default=FPS_DEFAULT,
                   metavar='FPS')
    p.add_argument('-max-steps', type=int, default=0,
                   dest='max_steps', metavar='N',
                   help='max steps per session (0 = board_size^2 * 10)')
    p.add_argument('-stats-out', type=str, default=None,
                   dest='stats_out', metavar='PATH',
                   help='save per-session statistics as JSON to PATH')
    return p.parse_args()


# partie complete
def run_session(board, interp, agent, display, visual, session, max_steps):
    board.reset()
    step = 0
    max_length = board.snake.length
    alive = True
    event = None
    green_eaten = 0
    red_eaten = 0

    # vision et etat initial
    vision = interp.get_vision(board, board.snake)
    state = interp.get_state_key(vision)

    while not board.is_game_over and alive and step < max_steps:
        action = agent.choose_action(state)  # choisit action
        event = board.apply_action(action)  # applique cette action
        reward = interp.get_reward(event)  # calcule recompense

        # compte pommes
        if event == 'green':
            green_eaten += 1
        elif event == 'red':
            red_eaten += 1

        # calcule etat/vision suivants
        next_vision = interp.get_vision(board, board.snake)
        next_state = interp.get_state_key(next_vision)

        # maj q-table
        agent.update(state, action, reward, next_state)

        # si -visual on on affiche texte terminal
        if visual:
            print(interp.format_terminal(next_vision, action))

        # rend frame pygame
        alive = display.render(
            board,
            session=session,
            length=board.snake.length,
            step=step,
        )

        # avance etatcourant au suivant
        state = next_state
        vision = next_vision
        step += 1
        max_length = max(max_length, board.snake.length)

    agent.decay_epsilon()

    # determine outcome
    if board.is_game_over:
        outcome = event
    elif not alive:
        outcome = 'quit'
    else:
        outcome = 'timeout'

    # renvoi dict recapitulatif de session
    return {
        'session': session,
        'length': max_length,
        'steps': step,
        'alive': alive,
        'outcome': outcome,
        'green_eaten': green_eaten,
        'red_eaten': red_eaten,
    }


def _summarize_stats(records):
    if not records:
        return None
    lengths = [r['length'] for r in records]
    steps = [r['steps'] for r in records]
    n = len(records)
    return {
        'sessions_run': n,
        'length_max': max(lengths),
        'length_avg': sum(lengths) / n,
        'steps_max': max(steps),
        'steps_avg': sum(steps) / n,
        'green_eaten_total': sum(r['green_eaten'] for r in records),
        'red_eaten_total': sum(r['red_eaten'] for r in records),
        'outcomes': dict(Counter(r['outcome'] for r in records)),
    }


def print_stats_summary(records):
    summary = _summarize_stats(records)
    if summary is None:
        return
    outcomes = ', '.join(
        f'{k}={v}' for k, v in sorted(summary['outcomes'].items())
    )
    print('--- Stats ---')
    print(
        f"Length — max: {summary['length_max']}, "
        f"avg: {summary['length_avg']:.2f}"
    )
    print(
        f"Steps  — max: {summary['steps_max']}, "
        f"avg: {summary['steps_avg']:.2f}"
    )
    print(
        f"Apples — green: {summary['green_eaten_total']}, "
        f"red: {summary['red_eaten_total']}"
    )
    print(f'Outcomes — {outcomes}')


def save_stats(path, records):
    data = {
        'sessions': records,
        'summary': _summarize_stats(records),
    }
    dirname = os.path.dirname(path)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)


def main():
    args = parse_args()
    visual = args.visual == 'on'
    headless = not visual

    if args.board_size < SNAKE_START_LENGTH:
        print(
            f'Error: board-size must be at least {SNAKE_START_LENGTH}',
            file=sys.stderr,
        )
        sys.exit(1)

    max_steps = args.max_steps or args.board_size ** 2 * 10

    board = Board(size=args.board_size)
    interp = Interpreter()
    agent = Agent()
    display = Display(
        board_size=args.board_size,
        headless=headless,
    )

    if args.load:
        try:
            agent.load(args.load)
            print(f'Load trained model from {args.load}')
        except FileNotFoundError:
            print(f'Error: model file not found: {args.load}')
            display.close()
            sys.exit(1)
        except (ValueError, KeyError):
            print(f'Error: invalid model file: {args.load}')
            display.close()
            sys.exit(1)

    display.set_speed(args.speed)
    display.set_step_by_step(args.step_by_step)
    agent.set_learning(not args.dontlearn)

    overall_max_length = 0
    overall_max_duration = 0
    session_records = []

    for session in range(1, args.sessions + 1):
        record = run_session(
            board, interp, agent, display, visual, session, max_steps
        )
        session_records.append(record)
        overall_max_length = max(overall_max_length, record['length'])
        overall_max_duration = max(overall_max_duration, record['steps'])
        if not headless:
            print(
                f'Session {session}/{args.sessions} — '
                f"length: {record['length']}, steps: {record['steps']}"
            )
        if not record['alive']:
            break

    print(
        f'Game over, max length = {overall_max_length}, '
        f'max duration = {overall_max_duration}'
    )

    print_stats_summary(session_records)

    if args.stats_out:
        try:
            save_stats(args.stats_out, session_records)
            print(f'Save session statistics in {args.stats_out}')
        except OSError as e:
            print(f'Error: cannot save statistics: {e}')

    if args.save:
        try:
            agent.save(args.save)
            print(f'Save learning state in {args.save}')
        except OSError as e:
            print(f'Error: cannot save model: {e}')

    display.close()


if __name__ == '__main__':
    main()
