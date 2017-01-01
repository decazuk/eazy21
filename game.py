from easy21_env import *
import numpy as np

# current_sum, deal_first_card, terminal, reward = initGame()
# current_sum, deal_first_card, terminal, reward = step(current_sum, deal_first_card, "hit")

actions = ["stick", "hit"]

N_table = {}
Q_table = {}

def N_action(current_sum, deal_first_card, action):
    key = buildTableKey(current_sum, deal_first_card)
    if key in N_table:
        return N_table[key][action]
    else:
        return 0
def N(current_sum, deal_first_card):
    key = buildTableKey(current_sum, deal_first_card)
    if key in N_table:
        count = 0
        for action in actions:
            if action in N_table[key]:
                count = count + N_table[key][action]
        return count
    else:
        return 0

def Q(current_sum, deal_first_card, action):
    key = buildTableKey(current_sum, deal_first_card)
    if key in Q_table:
        if action in Q_table[key]:
            return Q_table[key][action]
        else:
          0
    else:
        return 0

def Q_star_action(current_sum, deal_first_card):
    key = buildTableKey(current_sum, deal_first_card)
    if key in Q_table:
        max_value = -2
        max_action = ""
        for action in actions:
            if action in Q_table[key]:
                if Q_table[key][action] > max_value:
                    max_value = Q_table[key][action]
                    max_action = action
        return max_action
    else:
        return ""

def update_table(current_sum, deal_first_card, action, reward):
    key = buildTableKey(current_sum, deal_first_card)
    if key in N_table:
        if action in N_table[key]:
            original_count = N_table[key][action]
            N_table[key][action] = original_count + 1    
            # use mean value 
            Q_table[key][action] = (Q_table[key][action] * original_count + reward) / (original_count + 1)
        else:
            N_table[key][action] = 1
            Q_table[key][action] = reward
    else:
        N_table[key] = {}
        Q_table[key] = {}
        N_table[key][action] = 1
        Q_table[key][action] = reward


def buildTableKey(current_sum, deal_first_card):
    return "{},{}".format(current_sum, deal_first_card)

def choose_random_action(current_sum, deal_first_card):
    N0 = 100
    random_rate = float(N0) / (N0 + N(current_sum, deal_first_card))
    return (1 - random_rate) <= np.random.uniform(0, 1)

def playAndTrainGame():
    current_sum, deal_first_card, terminal, reward = initGame()
    while (not terminal):
        if choose_random_action(current_sum, deal_first_card):
            action = actions[random.randint(0, 1)]
        else:
            action = Q_star_action(current_sum, deal_first_card)

        current_sum_prime, deal_first_card, terminal, reward = step(current_sum, deal_first_card, action)
        update_table(current_sum_prime, deal_first_card, action, reward)
        current_sum = current_sum_prime

def startTrain():
    while (True):
        playAndTrainGame()

def drawDragram():
     



