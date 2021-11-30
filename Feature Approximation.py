import random
# Assumes function that add dict items of 'value' once trump is decided

class State():
    def __init__(self):
        self.hand = list()
        
    # Adds each card being played to the current hand
    def play_card(self, card, team, player):
        card['team'] = team
        card['player'] = player
        self.hand.append(card)

    # Returns the feature approximated Q-value a state-action pair
    def value_approximation(self, action):
        f1 = self.num_card_feature()
        f2 = self.high_card_feature(action)
        f3 = self.leading_team_feature(action)
        features = np.array(f1, f2, f3, f4)
        return np.dot(weights, features)

    # F1 - how many cards have been played
    def num_card_feature(self):
        return len(self.hand)

    # F2 - value of card in relation to the highest one played
    def high_card_feature(self, action):
        if len(state.hand) == 0:
            return action['value']
        maximum = self.hand[-1]['value']
        for i in range(len(self.hand)-1):
            if self.hand[i]['value'] > maximum:
                maximum = self.hand[i]['value']
        diff = action['value'] - maximum
        if diff > 0:
            return diff
        return 1/action['value']

    # F3 - value of card in relation to which team is leading the hand
    def leading_team_feature(self, action):
        if len(self.hand) == 0:
            return 0
        maxi = 0
        for i in range(1, len(self.hand)):
            if self.hand[i]['value'] > self.hand[maxi]['value']:
                maxi = i
        if self.hand[maxi]['team'] == 'us':
            return 1/action['value']
        else:
            return action['value']

    # Pick which action the learning player will use
    # Add a call to only pick from legal moves
    def select_action(self, deck, trump, lead):
        # Epsilon greedy policy
        prob = random.random()
        if prob > epsilon:
            # Greedy selection
            return self.select_max_action(deck)# Greedy selection
        # Random action with probability epsilon
        return random.choice(deck.hand_1)

    # Greedy move selection
    # Choose the action that has to the highest Q-value
    # Add a call to only pick from legal moves
    def select_max_action(self, deck):
        max = 0    
        for i in range(len(deck.hand_1) - 1):
            q1 = self.value_approximation(self, deck.hand_1[i])
            q2 = self.value_approximation(self, deck.hand_1[i+1])
            if q1 > q2:
                max = i
            else:
                max = i + 1
        return deck.hand_1[max]

    # Assuming learning agent is team 'us'
    def reward(self):
        maxi = 0
        for i in range(1, len(self.hand)):
            if self.hand[i]['value'] > self.hand[maxi]['value']:
                maxi = i
        if self.hand[maxi]['team'] == 'us':
            return 1 # Positive reward for winning a trick
        else:
            return -1 # Negative reward for losing a trick
    
