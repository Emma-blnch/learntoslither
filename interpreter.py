from constants import (
    Action, Cell,
    REWARD_GREEN, REWARD_RED, REWARD_STEP, REWARD_DEATH,
    DIRECTION_DELTA,
)

_EVENT_REWARDS = {
    'green': REWARD_GREEN,
    'red': REWARD_RED,
    'nothing': REWARD_STEP,
    'wall': REWARD_DEATH,
    'self': REWARD_DEATH,
    'starved': REWARD_DEATH,
}


class Interpreter:
    def get_vision(self, board, snake):
        vision = {}
        for action in Action:
            dr, dc = DIRECTION_DELTA[action]
            cells = []
            r = snake.head[0] + dr
            c = snake.head[1] + dc
            while 0 <= r < board.size and 0 <= c < board.size:
                cells.append(board.grid[r][c].value)
                r += dr
                c += dc
            cells.append(Cell.WALL.value)
            vision[action] = ''.join(cells)
        return vision

    def get_state_key(self, vision):
        return (
            vision[Action.UP],
            vision[Action.DOWN],
            vision[Action.LEFT],
            vision[Action.RIGHT],
        )

    def get_reward(self, event):
        return _EVENT_REWARDS[event]

    def format_terminal(self, vision, action):
        up = list(reversed(vision[Action.UP]))
        down = list(vision[Action.DOWN])
        left_rev = list(reversed(vision[Action.LEFT]))
        right = list(vision[Action.RIGHT])

        h_col = len(left_rev)
        lines = []

        for ch in up:
            lines.append(' ' * h_col + ch)

        lines.append(''.join(left_rev) + 'H' + ''.join(right))

        for ch in down:
            lines.append(' ' * h_col + ch)

        lines.append(f'Action: {action.name}')
        return '\n'.join(lines)
