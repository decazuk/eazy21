from QLearner import *

class MonteCarloLearner(object):
    def __init__(self, env, learner):
        self.env = env
        self.learner = learner
        self.learner.reset_tables()
    def train_learner(self):
        state, terminal, reward = self.env.init_game()
        while(not terminal):
            action = self.learner.choose_action(state, self.env.action_space)
            state_prime, terminal, reward = self.env.step(state, action)
            self.update_table(state, action, reward)
            state = state_prime
    def update_table(self, state, action, reward):
        original_count = self.learner.n_table[state]
        self.learner.n_table[state] = original_count + 1
        original_reward = self.learner.q_table[state][action]
        self.learner.q_table[state][action] = (original_reward * original_count + reward) / (original_count + 1)
