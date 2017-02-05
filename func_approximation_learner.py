from qtable import *
import numpy as np

class FuncApproximationLearner(object):
    def __init__(self, lamda = 0.5, gamma = 1, env):
        self.theta = np.zeros(36)
        self.env = env
        self.rng = np.random.RandomState()
        self.alpha = 0.01
        self.eps = 0.05

    def state_action_to_linear_feature(self, state, action):
        current_sum, deal_first_card = self.env.card_for_state(state)
        return self.card_action_to_linear_feature(current_sum, deal_first_card, action)

    def card_action_to_linear_feature(self, current_sum, deal_first_card, action):
        vec = np.zeros(36)
        ds = [(1, 5), (5, 8), (8, 11)]
        ps = [(1, 7), (4, 10), (7, 13), (10, 16), (13, 19), (16, 22)]
        a_s = [0, 1]
        index = 0
        for d_val in ds:
            for p_val in ps:
                for a_val in a_s:
                    if deal_first_card in range(d_val[0], d_val[1]) and \
                       current_sum in range(p_val[0], p_val[1]) and \
                       a_val == action:
                          vec[index] = 1
                    index += 1
        return vec

    def train_learner(self):
        state, terminal, reward = self.env.init_game()
        action = self.env.action_space[self.rng.randint(0, self.env.num)]
        e_fetures = np.zeros(36)
        while(not terminal):
            linear_feature = self.state_action_to_linear_feature(state, action)
            e_fetures[np.where(linear_feature == 1)] += 1
            state_prime, terminal, reward = self.env.step(state, action)
            delta = reward - np.sum(self.theta[np.where(linear_feature == 1)])

            # add max value in delta
            qa = self.get_state_actions_qa(state)
            delta += self.gamma * max(qa)

            self.theta += self.alpha * delta * e_fetures
            rnd = self.rng.rand()
            if rnd < self.eps:
                e_fetures = np.zeros(36)
                action = self.rng.randint(len(self.env.action_space))
            else:
                qa = self.get_state_actions_qa(state)
                index = np.argmax(qa)
                action = self.env.action_space[index]
                e_fetures *= self.gamma * self.lamda
            state = state_prime

    def get_state_actions_qa(self, state):
        qa = []
        for action in self.env.action_space:
            feature = self.state_action_to_linear_feature(state, action)
            qa.append(np.sum(self.theta[np.where(feature == 1)]))
        return qa


            