from qlearner import *

class SarsaLambdaLearner(object):
    def __init__(self, env, learner, lamda = 0.5):
        self.env = env
        self.learner = learner
        self.learner.reset_tables()
        self.e_table = {}
        self.gamma = 1.0
        self.lamda = lamda
    def train_learner(self):
        self.reset_etable()
        state, terminal, reward = self.env.init_game()
        action = self.learner.choose_action(state, self.env.action_space)
        while(not terminal):
            state_prime, terminal, reward = self.env.step(state, action)
            delta = 0.0
            if terminal:
                delta = reward - self.learner.win_rate(state, action)
            else:
                action_prime = self.learner.choose_action(state_prime, self.env.action_space)
                delta = reward + self.gamma * self.learner.win_rate(state_prime, action_prime) - self.learner.win_rate(state, action)
            self.update_table(state, action, delta)  
            if (not terminal):
                state = state_prime
                action = action_prime

    def reset_etable(self):
        self.e_table = {}
        for s in range(self.env.number_states):
            self.e_table[s] = np.zeros(self.env.number_actions)

    def update_table(self, state, action, delta):
        self.e_table[state][action] = self.e_table[state][action] + 1
        self.learner.n_table[state] += 1
        for s in range(self.env.number_states):
            for a in range(self.env.number_actions):
                alpha = 1.0 / self.learner.n_table[s] if self.learner.n_table[s] != 0 else 0
                self.learner.q_table[s][a] += alpha * delta * self.e_table[s][a]
                self.e_table[s][a] = self.gamma * self.lamda * self.e_table[s][a]