import random
from constants import (
    Action, Cell,
    BOARD_SIZE, SNAKE_START_LENGTH,
    GREEN_APPLE_COUNT, RED_APPLE_COUNT,
    DIRECTION_DELTA,
)
from snake import Snake


class Board:
    def __init__(self, size=BOARD_SIZE):
        self.size = size
        self.grid = None
        self.snake = None
        self.green_apples = set()
        self.red_apples = set()
        self._game_over = False
        self.reset()

    @property
    def is_game_over(self):
        return self._game_over

    def reset(self):
        self.grid = [
            [Cell.EMPTY] * self.size for _ in range(self.size)
        ]
        self.green_apples = set()
        self.red_apples = set()
        self._game_over = False
        self._place_snake()
        for _ in range(GREEN_APPLE_COUNT):
            self._place_apple(Cell.GREEN)
        for _ in range(RED_APPLE_COUNT):
            self._place_apple(Cell.RED)

    def _place_snake(self):
        direction = random.choice(list(Action))
        dr, dc = DIRECTION_DELTA[direction]
        span = SNAKE_START_LENGTH - 1
        min_r = max(0, dr * span)
        max_r = min(self.size - 1, self.size - 1 + dr * span)
        min_c = max(0, dc * span)
        max_c = min(self.size - 1, self.size - 1 + dc * span)
        head_r = random.randint(min_r, max_r)
        head_c = random.randint(min_c, max_c)
        head = (head_r, head_c)
        body = [
            (head_r - dr * i, head_c - dc * i)
            for i in range(1, SNAKE_START_LENGTH)
        ]
        self.snake = Snake(head, body, direction)
        self.grid[head[0]][head[1]] = Cell.HEAD
        for pos in body:
            self.grid[pos[0]][pos[1]] = Cell.BODY

    def _place_apple(self, color):
        free = self.get_free_cells()
        if not free:
            return None
        pos = random.choice(free)
        self.grid[pos[0]][pos[1]] = color
        if color == Cell.GREEN:
            self.green_apples.add(pos)
        else:
            self.red_apples.add(pos)
        return pos

    def get_free_cells(self):
        return [
            (r, c)
            for r in range(self.size)
            for c in range(self.size)
            if self.grid[r][c] == Cell.EMPTY
        ]

    def _is_out_of_bounds(self, pos):
        r, c = pos
        return r < 0 or r >= self.size or c < 0 or c >= self.size

    def apply_action(self, action):
        next_head = self.snake.next_head(action)

        if self._is_out_of_bounds(next_head):
            self._game_over = True
            return 'wall'

        if next_head in self.snake.cells[:-1]:
            self._game_over = True
            return 'self'

        cell_at_next = self.grid[next_head[0]][next_head[1]]
        old_head = self.snake.head
        old_tail = self.snake.move(action)

        self.grid[old_tail[0]][old_tail[1]] = Cell.EMPTY
        self.grid[old_head[0]][old_head[1]] = Cell.BODY
        self.grid[next_head[0]][next_head[1]] = Cell.HEAD

        if cell_at_next == Cell.GREEN:
            self.green_apples.discard(next_head)
            self.snake.grow(old_tail)
            self.grid[old_tail[0]][old_tail[1]] = Cell.BODY
            self._place_apple(Cell.GREEN)
            return 'green'

        if cell_at_next == Cell.RED:
            self.red_apples.discard(next_head)
            removed = self.snake.shrink()
            if removed is None:
                self._game_over = True
                return 'starved'
            self.grid[removed[0]][removed[1]] = Cell.EMPTY
            self._place_apple(Cell.RED)
            return 'red'

        return 'nothing'
