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

    # renvoie toutes les cases occupées par serpent :
    @property
    def cells(self):
        return [self.head] + list(self.body)

    # calcule ou irait tête si on jouait action,
    # sans modifier l'état :
    def next_head(self, action):
        dr, dc = DIRECTION_DELTA[action]
        return (self.head[0] + dr, self.head[1] + dc)

    # déplacement réel :
    def move(self, action):
        new_head = self.next_head(action)
        # ancienne tete devient premier morceau du corps
        self.body.appendleft(self.head)
        self.head = new_head  # tete avance
        self.direction = action
        # retire et renvoie dernier element
        return self.body.pop()

    # pomme verte, serpent grandit :
    def grow(self, tail):
        self.body.append(tail)

    # pomme rouge, serpent rétrécit :
    def shrink(self):
        # si corps deja vide alors mort
        if len(self.body) == 0:
            return None
        return self.body.pop()
