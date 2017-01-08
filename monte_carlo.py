from easy21env import *
import numpy as np
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

class MonteCarloControl(object):
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
            return action_space[self.q_table[state].argsort()[-1]]

    def choose_random_action(self, state):
        N0 = 100
        random_rate = float(N0) / (N0 + self.n_table[state])
        return (1 - random_rate) <= np.random.uniform(0, 1)

    def update_table(self, state, action, reward):
        original_count = self.n_table[state]
        self.n_table[state] = original_count + 1
        original_reward = self.q_table[state][action]
        self.q_table[state][action] = (original_reward * original_count + reward) / (original_count + 1)

    def max_win_rate(self, state):
        return np.amax(self.q_table[state])

def easy21_with_monte_carlo():
    env = Easy21Env()
    learner = MonteCarloControl(num_states = env.number_states, num_actions = env.number_actions)
    learner.reset_tables()
    def play_and_train_game():    
        state, terminal, reward = env.init_game()
        while(not terminal):
            action = learner.choose_action(state, env.action_space)
            state_prime, terminal, reward = env.step(state, action)
            learner.update_table(state, action, reward)
            state = state_prime
    def draw_dragram():
        x = []
        y = []
        z = []
        for s in range(learner.num_states):
            current_sum, deal_first_card = env.card_for_state(s)
            if current_sum >= 11:
                x.append(deal_first_card)
                y.append(current_sum)
                z.append(learner.max_win_rate(s))
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.scatter(x, y, z, label='win rate dispatch')
        ax.legend()
        plt.show()
    i = 0
    while(True):
        if (i > 0 and i % 10000 == 0):
            draw_dragram()
        play_and_train_game()
        i = i + 1

if __name__ == "__main__":
    easy21_with_monte_carlo()
