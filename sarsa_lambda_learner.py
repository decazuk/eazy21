from qtable import *

class SarsaLambdaLearner(object):
    def __init__(self, env, table, lamda = 0.5):
        self.env = env
        self.table = table
        self.table.reset_tables()
        self.e_table = {}
        self.gamma = 1.0
        self.lamda = lamda
    def train_learner(self):
        self.reset_etable()
        state, terminal, reward = self.env.init_game()
        action = self.table.choose_action(state, self.env.action_space)
        while(not terminal):
            state_prime, terminal, reward = self.env.step(state, action)
            delta = 0.0
            if terminal:
                delta = reward - self.table.win_rate(state, action)
            else:
                action_prime = self.table.choose_action(state_prime, self.env.action_space)
                delta = reward + self.gamma * self.table.win_rate(state_prime, action_prime) - self.table.win_rate(state, action)
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
        self.table.n_table[state] += 1
        for s in range(self.env.number_states):
            for a in range(self.env.number_actions):
                alpha = 1.0 / self.table.n_table[s] if self.table.n_table[s] != 0 else 0
                self.table.q_table[s][a] += alpha * delta * self.e_table[s][a]
                self.e_table[s][a] = self.gamma * self.lamda * self.e_table[s][a]