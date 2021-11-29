import random
# Assumes function that add dict items of 'value' once trump is decided
# Assuming we're using bias
    # Could easily be removed

# Global for the game
# Initialize feaure weights
w1, w2, w3, b = 1, 1, 1, 0

class State():
    def __init__(self):
        self.hand = list()
        
    def play_card(self, card, team):
        card['team'] = team
        self.hand.append(card)

    def value_approximation(self, action):
        f1 = self.num_card_feature()
        f2 = self.high_card_feature(action)
        f3 = self.leading_team_feature(action)
        return w1*f1 + w2*f2 + w3*f3 + b

    def num_card_feature(self):
        return len(self.hand)

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

# Q-learning without function approximation
# Q(s,a) <- Q(s,a) + alpha[R + gamma(maxQ(s',a) - Q(s,a)]

# With function approximation
# w <- w + alpha(r + gamma(maxQ(s',a) - Q(s,a))grad(Q(s,a))
# Linear, so graident is a vector (f1, f2, f3)
    # With bias(f1, f2, f3, 1)
    def select_action(self, deck):
        prob = random.random()
        if prob > epsilon:
            return self.select_max_action(deck)# Greedy selection
        # Random action with probability epsilon
        return random.choice(deck.hand_1)

    
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


# Currently very preliminary
# Has the equations for q-learning updates
# Needs to be integrated with the enviornment functionality to actually have it play cards properly
def Q_learning(s1, deck):
    while len(deck.hand_1()) > 0:
        # Other players play cards
        # s <- initial state of episode
            # s = state
        # a <- action given by policy pi
        a = s1.select_action(deck)
        deck.hand_1.remove(a) # 1 less card in hand
        s1.play_card(a, 'us')
        # Rest of players play cards
        # Take action a, observe reward r and next state s'
        r = s1.reward()
        # Assuming some functon for getting the next hand
            # Will need gameplay rules
        s2 = play_round()
        # w <- w + alpha(r + gamma(maxQ(s',a) - Q(s,a))grad(Q(s,a))
            # Find maxQ(s',a)
            a2 = select_max_action(s2, deck)
            maxQ = s2.value_approximation(a2)
            # calculate alpha(r + gamma(maxQ(s',a) = Q(s,a)
            # Go through weights and features
                # w1 = w1 + const*f1
                #...
                # b = b + const
    
        # s <- s'
        s1 = s2
    
