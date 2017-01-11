from easy21env import *
from qlearner import *
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from monte_carlo_learner import * 

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
                delta = reward - learner.win_rate(state, action)
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
        if (i > 0 and i % 1000 == 0):
            draw_dragram(learner, env)
        play_and_train_game(0.1)
        i = i + 1


if __name__ == "__main__":
    env = Easy21Env()
    learner = QLearner(num_states = env.number_states, num_actions = env.number_actions)
    mc = MonteCarloLearner(env, learner)
    i = 0
    while (True):
        if (i > 0 and i % 1000 == 0):
            draw_dragram(mc.learner, env)
        mc.train_learner()
        i = i + 1