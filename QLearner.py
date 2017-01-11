import numpy as np
import random
class QLearner(object):
    def __init__(self, num_states, num_actions):
        self.num_states = num_states
        self.num_actions = num_actions
        self.q_table = {}
        self.n_table = {}

    def reset_tables(self):
        for s in range(self.num_states):
            self.q_table[s] = np.zeros(self.num_actions)
            self.n_table[s] = 0

    def choose_action(self, state, action_space):
        if self.choose_random_action(state):
            return action_space[random.randint(0, self.num_actions - 1)]
        else:
            return self.choose_greedy_action(state, action_space)

    def choose_greedy_action(self, state, action_space):
        return action_space[self.q_table[state].argsort()[-1]]

    def choose_random_action(self, state):
        N0 = 100
        random_rate = float(N0) / (N0 + self.n_table[state])
        return (1 - random_rate) <= np.random.uniform(0, 1)

    def max_win_rate(self, state):
        return np.amax(self.q_table[state])

    def win_rate(self, state, action):
        return self.q_table[state][action]