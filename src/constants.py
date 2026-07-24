from enum import Enum


class Action(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class Cell(Enum):
    EMPTY = '0'
    HEAD = 'H'
    BODY = 'S'
    GREEN = 'G'
    RED = 'R'
    WALL = 'W'


# parametres plateau de jeu
BOARD_SIZE = 10
SNAKE_START_LENGTH = 3
GREEN_APPLE_COUNT = 2
RED_APPLE_COUNT = 1
CELL_SIZE = 60
FPS_DEFAULT = 8
FPS_FAST = 60

# recompenses par evenement
REWARD_GREEN = 15.0
REWARD_RED = -10.0
REWARD_STEP = -0.5
REWARD_DEATH = -100.0

# couleurs
COLOR_BG = (200, 200, 200)
COLOR_GRID = (170, 170, 170)
COLOR_SNAKE_HEAD = (0, 0, 180)
COLOR_SNAKE_BODY = (0, 0, 255)
COLOR_GREEN_APPLE = (0, 200, 0)
COLOR_RED_APPLE = (220, 0, 0)

# taux d'apprentissage
ALPHA = 0.1
# facteur d'actualisation (poids donner aux recompenses futures)
GAMMA = 0.9
# taux d'exploration initial
EPSILON_START = 1.0
# plancher d'exploration (eviter le 0 sinon plus jamais d'exploration)
EPSILON_MIN = 0.01
# vitesse a laquelle epsilon diminue apres chaque session
EPSILON_DECAY = 0.995

DIRECTION_DELTA = {
    Action.UP: (-1, 0),
    Action.DOWN: (1, 0),
    Action.LEFT: (0, -1),
    Action.RIGHT: (0, 1),
}
