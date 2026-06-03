from collections import deque
from constants import DIRECTION_DELTA


class Snake:
    def __init__(self, head, body, direction):
        self.head = head
        self.body = deque(body)
        self.direction = direction

    @property
    def length(self):
        return 1 + len(self.body)

    @property
    def cells(self):
        return [self.head] + list(self.body)

    def next_head(self, action):
        dr, dc = DIRECTION_DELTA[action]
        return (self.head[0] + dr, self.head[1] + dc)

    def move(self, action):
        new_head = self.next_head(action)
        self.body.appendleft(self.head)
        self.head = new_head
        self.direction = action
        return self.body.pop()

    def grow(self, tail):
        self.body.append(tail)

    def shrink(self):
        if len(self.body) == 0:
            return None
        return self.body.pop()
