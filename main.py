import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from easy21env import *
from monte_carlo_learner import * 
from sarsa_lambda_learner import * 
import pickle

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

def train_q_star_with_monte_carlo_learner():
    env = Easy21Env()
    table = QTable(num_states = env.number_states, num_actions = env.number_actions)
    learner = MonteCarloLearner(env = env, table = table)
    i = 0
    while (i < 1000000):
        learner.train_learner()
        i = i + 1
    draw_dragram(table, env)
    pickle.dump(table, open('mc_q_star.p', 'wb'))

def train_q_with_sarsa_lambda(lamda):
    env = Easy21Env()
    table = QTable(num_states = env.number_states, num_actions = env.number_actions)
    q_star_table = pickle.load(open('mc_q_star.p', 'rb'))
    np_star = q_star_table.numpy_values_array()
    learner = SarsaLambdaLearner(env = env, table = table, lamda = lamda)
    i = 0
    learning_curve = []
    while (i < 500000):
        learner.train_learner()
        if (i > 0 and i % 1000 == 0):
            np_sarsa = learner.table.numpy_values_array()
            mean_squared_error = ((np_star - np_sarsa) ** 2).mean()
            learning_curve.append(mean_squared_error)
            print(mean_squared_error)
        i = i + 1
    return learning_curve

if __name__ == "__main__":
    # train_q_star_with_monte_carlo_learner()
    learning_curve1 = train_q_with_sarsa_lambda(0)
    pickle.dump(learning_curve1, open('lambda0learning_curve', 'wb'))
    learning_curve2 = train_q_with_sarsa_lambda(1)
    pickle.dump(learning_curve1, open('lambda1learning_curve', 'wb'))
    plt.plot(learning_curve1, color = 'r')
    plt.plot(learning_curve2, color = 'b')
    plt.show()
