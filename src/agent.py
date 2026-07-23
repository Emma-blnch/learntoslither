import json
import random
from collections import defaultdict
from constants import (
    Action,
    ALPHA, GAMMA,
    EPSILON_START, EPSILON_MIN, EPSILON_DECAY,
)


class Agent:
    def __init__(
        self,
        alpha=ALPHA,
        gamma=GAMMA,
        epsilon=EPSILON_START,
        epsilon_min=EPSILON_MIN,
        epsilon_decay=EPSILON_DECAY,
    ):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self._learning = True
        self.q_table = defaultdict(lambda: defaultdict(float))

    def set_learning(self, enabled):
        self._learning = enabled

    def choose_action(self, state):
        if self._learning and random.random() < self.epsilon:
            return random.choice(list(Action))
        return self._best_action(state)

    def _best_action(self, state):
        q_vals = {a: self.q_table[state][a] for a in Action}
        max_q = max(q_vals.values())
        best = [a for a, v in q_vals.items() if v == max_q]
        safe = [a for a in best if not state[a.value * 3]]
        return random.choice(safe or best)

    def update(self, state, action, reward, next_state):
        if not self._learning:
            return
        current_q = self.q_table[state][action]
        max_next_q = max(self.q_table[next_state][a] for a in Action)
        target = reward + self.gamma * max_next_q
        self.q_table[state][action] = (
            current_q + self.alpha * (target - current_q)
        )

    def decay_epsilon(self):
        if not self._learning:
            return
        self.epsilon = max(
            self.epsilon_min,
            self.epsilon * self.epsilon_decay,
        )

    def save(self, path):
        data = {
            'epsilon': self.epsilon,
            'q_table': {
                json.dumps(list(state)): {
                    a.name: v for a, v in actions.items()
                }
                for state, actions in self.q_table.items()
            },
        }
        with open(path, 'w') as f:
            json.dump(data, f)

    def load(self, path):
        with open(path) as f:
            data = json.load(f)
        self.epsilon = data['epsilon']
        self.q_table = defaultdict(lambda: defaultdict(float))
        for state_str, actions in data['q_table'].items():
            state = tuple(json.loads(state_str))
            for name, value in actions.items():
                self.q_table[state][Action[name]] = value
