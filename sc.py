from easy21_env import *
import numpy as np
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

Q_table = {}
N_table = {}

def initTable():
    global Q_table
    global N_table
    for s in range(nS()):
        Q_table[s] = np.zeros(nA())
        N_table[s] = 0

def choose_random_action(state):
    global Q_table
    global N_table
    N0 = 100
    random_rate = float(N0) / (N0 + N_table[state])
    return (1 - random_rate) <= np.random.uniform(0, 1)

def take_action(state):
    global Q_table
    global N_table
    ap = actionSpace()
    if choose_random_action(state):
        return ap[random.randint(0, nA() - 1)]
    else:
        return ap[Q_table[state].argsort()[-1]]

def updateTable(state, action, reward):
    global Q_table
    global N_table
    original_count = N_table[state]
    N_table[state] = original_count + 1
    original_reward = Q_table[state][action]
    Q_table[state][action] = (original_reward * original_count + reward) / (original_count + 1)

def playAndTrainGame():
    state, terminal, reward = initGame()
    while(not terminal):
        action = take_action(state)
        state_prime, terminal, reward = step(state, action)
        updateTable(state, action, reward)
        state = state_prime

def startMCTrain():
    initTable()
    i = 0
    while (True):
      if (i > 0 and i % 10000 == 0):
          drawDragram()
      playAndTrainGame()
      i = i + 1

def drawDragram():
    global Q_table
    global N_table
    x = []
    y = []
    z = []
    for s in range(nS()):
        max_win_rate = np.amax(Q_table[s])
        current_sum, deal_first_card = cardForState(s)
        if current_sum >= 11:
            x.append(deal_first_card)
            y.append(current_sum)
            z.append(max_win_rate)
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.scatter(x, y, z, label='win rate dispatch')
    ax.legend()
    plt.show()

startMCTrain()