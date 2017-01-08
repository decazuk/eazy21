import random

class Easy21Env(object):

    def __init__(self):
        self.number_states = 21 * 10
        self.number_actions = 2
        self.action_space = [0, 1]
  
    def draw_card(self):
        value = random.randint(1, 10)
        return value if random.randint(1, 3) < 3 else -value

    def draw_first_card(self):
        return random.randint(1, 10)        

    def state_for_card(self, current_sum, deal_first_card):
        return (current_sum - 1) * 10 + deal_first_card

    def card_for_state(self, state):
        deal_first_card = state % 10
        current_sum = int(state / 10) + 1
        return current_sum, deal_first_card        

    def sum_bust(self, current_sum):
        return current_sum > 21 or current_sum < 1

    def init_game(self):
        current_sum = self.draw_first_card()
        deal_first_card = self.draw_first_card()
        terminal = False
        reward = 0
        return self.state_for_card(current_sum, deal_first_card), terminal, reward

    def step(self, state, action):
        if action == 0:
            return self.stick(state)
        else:
            return self.hit(state)

    def stick(self, state):
        current_sum, deal_first_card = self.card_for_state(state)
        deal_sum = deal_first_card
        deal_bust = False
        while((not deal_bust) and deal_sum < 17):
            deal_sum = deal_sum + self.draw_card()
            deal_bust = self.sum_bust(deal_sum)
        if deal_bust:
            return self.state_for_card(current_sum, deal_first_card), True, 1
        else:
            reward = 0
            if current_sum > deal_sum:
                reward = 1
            elif current_sum < deal_sum:
                reward = -1
            else:
                reward = 0
            return self.state_for_card(current_sum, deal_first_card), True, reward

    def hit(self, state):
        current_sum, deal_first_card = self.card_for_state(state)
        new_sum = current_sum + self.draw_card()
        new_terminal = False
        reward = 0
        bust = self.sum_bust(new_sum)
        if bust:
            new_terminal = True
            reward = -1
        else:
            new_terminal = False
        return self.state_for_card(new_sum, deal_first_card), new_terminal, reward

    