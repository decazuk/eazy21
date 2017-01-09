from easy21env import *
import numpy as np
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

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

    def update_table(self, state, action, reward):
        original_count = self.n_table[state]
        self.n_table[state] = original_count + 1
        original_reward = self.q_table[state][action]
        self.q_table[state][action] = (original_reward * original_count + reward) / (original_count + 1)

    def max_win_rate(self, state):
        return np.amax(self.q_table[state])

    def win_rate(self, state, action):
        return self.q_table[state][action]

def easy21_with_monte_carlo():
    env = Easy21Env()
    learner = QLearner(num_states = env.number_states, num_actions = env.number_actions)
    learner.reset_tables()
    def play_and_train_game():    
        state, terminal, reward = env.init_game()
        while(not terminal):
            action = learner.choose_action(state, env.action_space)
            state_prime, terminal, reward = env.step(state, action)
            learner.update_table(state, action, reward)
            state = state_prime
    i = 0
    while(True):
        if (i > 0 and i % 10000 == 0):
            draw_dragram(learner, env)
        play_and_train_game()
        i = i + 1

def draw_dragram(learner, env):
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

def easy21_with_sara_lambda():
    env = Easy21Env()
    learner = QLearner(num_states = env.number_states, num_actions = env.number_actions)
    learner.reset_tables()

    def play_and_train_game(lamda):
        e_table = {}
        for s in range(env.number_states):
            e_table[s] = np.zeros(env.number_actions)
        gamma = 1.0
        state, terminal, reward = env.init_game()
        action = learner.choose_action(state, env.action_space)
        while(not terminal):
            state_prime, terminal, reward = env.step(state, action)
            learner.n_table[state] += 1
            delta = 0.0
            if terminal:
                delta = reward
            else:
                action_prime = learner.choose_action(state_prime, env.action_space)
                delta = reward + gamma * learner.win_rate(state_prime, action_prime) - learner.win_rate(state, action)
            e_table[state][action] = e_table[state][action] + 1
            for s in range(env.number_states):
                for a in range(env.number_actions):
                    alpha = 1.0 / learner.n_table[s] if learner.n_table[s] != 0 else 0
                    learner.q_table[s][a] += alpha * delta * e_table[s][a]
                    e_table[s][a] = gamma * lamda * e_table[s][a]
            if not terminal:
                state = state_prime
                action = action_prime
    i = 0
    while(True):
        if (i > 0 and i % 10000 == 0):
            draw_dragram(learner, env)
        play_and_train_game(0.1)
        i = i + 1


if __name__ == "__main__":
    easy21_with_sara_lambda()
