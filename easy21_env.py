import random

def step(state, action):
    # current_sum, deal_first_card = cardForState(state)
    if action == 0:
        return stick(state)
    else:
        return hit(state)

def stick(state):
    current_sum, deal_first_card = cardForState(state)
    deal_sum = deal_first_card
    deal_bust = False
    while ((not deal_bust) and deal_sum < 17):
        deal_sum = deal_sum + drawCard()
        deal_bust = sum_bust(deal_sum)
    if deal_bust:
        return stateForCard(current_sum, deal_first_card), True, 1
    else:
        reward = 0
        if current_sum > deal_sum:
            reward = 1
        elif current_sum < deal_sum:
            reward = -1
        else:
            reward = 0
        return stateForCard(current_sum, deal_first_card), True, reward

def hit(state):
    current_sum, deal_first_card = cardForState(state)
    new_sum = current_sum + drawCard()
    new_terminal = False
    reward = 0
    bust = sum_bust(new_sum)
    if bust:
        new_terminal = True
        reward = -1
    else:
        new_terminal = False
    return stateForCard(new_sum, deal_first_card), new_terminal, reward

def sum_bust(current_sum):
    return current_sum > 21 or current_sum < 1

def initGame():
    # return first state
    current_sum = drawFirstCard()
    deal_first_card = drawFirstCard()
    terminal = False
    reward = 0
    return stateForCard(current_sum, deal_first_card), terminal, reward

def drawCard():
    value = random.randint(1, 10)
    return value if random.randint(1, 3) < 3 else -value

def drawFirstCard():
    return random.randint(1, 10)

def nS():
    return 21 * 10
def nA():
    return 2
def actionSpace():
    return [0, 1]


def stateForCard(current_sum, deal_first_card):
    return (current_sum - 1) * 10 + deal_first_card

def cardForState(state):
    deal_first_card = state % 10
    current_sum = int(state / 10) + 1
    return current_sum, deal_first_card

# state
  # current sum
  # deal first card
  # terminal?
  # reward

#action
  # stick
  # hit