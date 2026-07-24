from constants import (
    Action, Cell,
    REWARD_GREEN, REWARD_RED, REWARD_STEP, REWARD_DEATH,
    DIRECTION_DELTA,
)

# fait correspondre chaque event possible de Board.apply_action
# a recompense définit dans constants.py
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
        # pour chacune des 4 directions
        for action in Action:
            dr, dc = DIRECTION_DELTA[action]
            cells = []
            # on part de la case juste apres la tete
            r = snake.head[0] + dr
            c = snake.head[1] + dc
            # tant qu'on ets dans plateau on avance case par case
            # en accumulant les caracteres des cases
            while 0 <= r < board.size and 0 <= c < board.size:
                cells.append(board.grid[r][c].value)
                r += dr
                c += dc
            # quand on sort du plateau on ajoute un mur 'W' et on arrete
            cells.append(Cell.WALL.value)
            vision[action] = ''.join(cells)
        # retourne un dict Action:chaine de caractere
        # du case par case par direction
        return vision

    # transforme la vision en clé d'état a 12 bool
    def get_state_key(self, vision):
        # _danger = {'W', 'S', 'H'}
        _danger = {Cell.WALL.value, Cell.BODY.value, Cell.HEAD.value}
        state = []
        for action in [Action.UP, Action.DOWN, Action.LEFT, Action.RIGHT]:
            # chaine de vision dans cette direction
            v = vision[action]
            # regarde premier caractere (case adjacente a tete)
            state.append(int(v[0] in _danger))
            # regarde toute chaine (check si pomme verte visible
            # dans direction peu importe distance)
            state.append(int(Cell.GREEN.value in v))
            state.append(int(Cell.RED.value in v))  # same que pomme verte
        return tuple(state)

    def get_reward(self, event):
        return _EVENT_REWARDS[event]

    # construit bloc de texte affiché dans terminal
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
