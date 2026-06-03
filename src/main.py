import argparse
import sys
from constants import BOARD_SIZE, FPS_DEFAULT, SNAKE_START_LENGTH
from environment import Board
from interpreter import Interpreter
from display import Display
from agent import Agent


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
    return p.parse_args()


def run_session(board, interp, agent, display, visual, session, max_steps):
    board.reset()
    step = 0
    max_length = board.snake.length
    alive = True

    vision = interp.get_vision(board, board.snake)
    state = interp.get_state_key(vision)

    while not board.is_game_over and alive and step < max_steps:
        action = agent.choose_action(state)
        event = board.apply_action(action)
        reward = interp.get_reward(event)

        next_vision = interp.get_vision(board, board.snake)
        next_state = interp.get_state_key(next_vision)

        agent.update(state, action, reward, next_state)

        if visual:
            print(interp.format_terminal(vision, action))

        alive = display.render(
            board,
            session=session,
            length=board.snake.length,
            step=step,
        )

        state = next_state
        vision = next_vision
        step += 1
        max_length = max(max_length, board.snake.length)

    agent.decay_epsilon()
    return max_length, step, alive


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

    for session in range(1, args.sessions + 1):
        max_length, duration, alive = run_session(
            board, interp, agent, display, visual, session, max_steps
        )
        overall_max_length = max(overall_max_length, max_length)
        overall_max_duration = max(overall_max_duration, duration)
        if not headless:
            print(
                f'Session {session}/{args.sessions} — '
                f'length: {max_length}, steps: {duration}'
            )
        if not alive:
            break

    print(
        f'Game over, max length = {overall_max_length}, '
        f'max duration = {overall_max_duration}'
    )

    if args.save:
        try:
            agent.save(args.save)
            print(f'Save learning state in {args.save}')
        except OSError as e:
            print(f'Error: cannot save model: {e}')

    display.close()


if __name__ == '__main__':
    main()
