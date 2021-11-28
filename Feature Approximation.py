# Assumes function that add dict items of 'value' once trump is decided

class State():
    def __init__(self):
        self.hand = list()
        # Intialize feature weights
        self.w1 = 1
        self.w2 = 1
        self.w3 = 1

    def play_card(self, card, team):
        card['team'] = team
        self.hand.append(card)

    def value_approximation(self, action):
        f1 = self.num_card_feature()
        f2 = self.high_card_feature(action)
        f3 = self.leading_team_feature(action)
        return w1*f1 + w2*f2 + w3*f3

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
    
