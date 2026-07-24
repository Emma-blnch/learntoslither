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
        # defaultdict renvoie 0.0 pour tout etat jamais vu
        # sans avoir a l'initialiser explicitement

    # -dontlearn
    def set_learning(self, enabled):
        self._learning = enabled

    # epsilon-greedy : si random tombe sous epsilon alors explor sinon exploit
    def choose_action(self, state):
        if self._learning and random.random() < self.epsilon:
            return random.choice(list(Action))
        return self._best_action(state)

    def _best_action(self, state):
        # recupere q-value de chaque action pour cet etat
        q_vals = {a: self.q_table[state][a] for a in Action}
        max_q = max(q_vals.values())  # trouve le max
        # garde toutes les actions a egalite
        best = [a for a, v in q_vals.items() if v == max_q]
        # filtre parmis celles pas signalees dangereuses (state[a.value * 3])
        safe = [a for a in best if not state[a.value * 3]]
        # choisit au hasard dans ce sous ensemble (ou dans best)
        return random.choice(safe or best)

    def update(self, state, action, reward, next_state):
        # si -dontlearn, ne fais rien
        if not self._learning:
            return
        current_q = self.q_table[state][action]  # estimation actuelle
        # meilleure valeur possible depuis etat suivant
        max_next_q = max(self.q_table[next_state][a] for a in Action)
        # recompenses immediate + valeur future
        target = reward + self.gamma * max_next_q
        # rqpproche current_q de target d'un pas alpha
        # (pour ne pas ecraser ce qui a ete appris avant)
        self.q_table[state][action] = (
            current_q + self.alpha * (target - current_q)
        )

    # reduit epsilon une fois par session
    def decay_epsilon(self):
        if not self._learning:
            return
        self.epsilon = max(
            self.epsilon_min,
            self.epsilon * self.epsilon_decay,
        )

    # serialise epsilon et q table en JSON
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

    # recharge epsilon et reconstruit q table depius JSON
    def load(self, path):
        with open(path) as f:
            data = json.load(f)
        self.epsilon = data['epsilon']
        self.q_table = defaultdict(lambda: defaultdict(float))
        for state_str, actions in data['q_table'].items():
            state = tuple(json.loads(state_str))
            for name, value in actions.items():
                self.q_table[state][Action[name]] = value
