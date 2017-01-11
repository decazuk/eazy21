import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from easy21env import *
from monte_carlo_learner import * 
from sarsa_lambda_learner import * 

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

if __name__ == "__main__":
    env = Easy21Env()
    learner = QLearner(num_states = env.number_states, num_actions = env.number_actions)
    saras = SarsaLambdaLearner(env, learner)
    i = 0
    while (True):
        if (i > 0 and i % 1000 == 0):
            draw_dragram(saras.learner, env)
        saras.train_learner()
        i = i + 1