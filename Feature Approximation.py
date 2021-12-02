import random
import numpy as np

class State():
    def __init__(self):
        self.hand = list()
        self.features = np.empty(4)
        
    # Adds each card being played to the current hand
    def play_card(self, card, team, player):
        card['team'] = team
        card['player'] = player
        self.hand.append(card)

    # Returns the feature approximated Q-value a state-action pair
    def value_approximation(self, action):
        self.features[0] = self.num_card_feature(action)
        self.features[1] = self.high_card_feature(action)
        self.features[2] = self.leading_team_feature(action)
        self.features[3] = 1
        return weights*features
    
    # F1 - how many cards have been played
    def num_card_feature(self, action):
        return len(self.hand) * action['card_rank']

    # F2 - value of card in relation to the highest one played
    def high_card_feature(self, action):
        if len(state.hand) == 0:
            return action['card_rank']
        maximum = self.hand[-1]['card_rank']
        for i in range(len(self.hand)-1):
            if self.hand[i]['card_rank'] > maximum:
                maximum = self.hand[i]['card_rank']
        diff = action['card_rank'] - maximum
        if diff > 0:
            return diff
        return 1/action['card_rank']

    # F3 - value of card in relation to which team is leading the hand
    def leading_team_feature(self, action):
        if len(self.hand) == 0:
            return 0
        maxi = 0
        for i in range(1, len(self.hand)):
            if self.hand[i]['card_rank'] > self.hand[maxi]['card_rank']:
                maxi = i
        if self.hand[maxi]['team'] == 'us':
            return 1/action['card_rank']
        else:
            return action['card_rank']

    # Pick which action the learning player will use
    # Add a call to only pick from legal moves
    def select_action(self, deck, trump, lead, epsilon):
        # Epsilon greedy policy
        prob = random.random()
        if prob > epsilon:
            # Greedy selection
            return self.select_max_action(deck)# Greedy selection
        # Random action with probability epsilon
        # Legal moves
        choices = list()
        for x in deck.hand_1:
            if legal_move(x, trump, lead):
                choices.append(x)
        return random.choice(choices)

    # Greedy move selection
    # Choose the action that has to the highest Q-value
    # Add a call to only pick from legal moves
    def select_max_action(self, deck):
        max = 0  
        # legal_moves
        choices = list()
        for x in deck.hand_1:
            if legal_move(x, trump, lead):
                choices.append(x)              
        for i in range(len(choices) - 1):
            q1 = self.value_approximation(self, choices[i])
            q2 = self.value_approximation(self, choices[i+1])
            if q1 > q2:
                max = i
            else:
                max = i + 1
        return choices[max]

    # Assuming learning agent is team 'us'
    def reward(self):
        maxi = 0
        for i in range(1, len(self.hand)):
            if self.hand[i]['card_rank'] > self.hand[maxi]['card_rank']:
                maxi = i
        if self.hand[maxi]['team'] == 'us':
            return 1 # Positive reward for winning a trick
        else:
            return -1 # Negative reward for losing a trick
    
