# File for setting up a run-through of the game
# Not yet integrated with all the files
    # Havent' been able to confirm that it works because of this

# Global for the game
# Initialize feaure weights
w1, w2, w3, b = 1, 1, 1, 0

import random
import copy

def pick_trump():
    return random.choice(SUITS)

def pick_lead_player():
    # Represents an index in the list of players
    # Each player linked to a hand
    return random.choice([0, 1, 2, 3])
            
def run_round(strategy):
    state = State()
    deck = Deck()
    deck.shuffle()
    deck.deal()
    trump = pick_trump()
    learning_player = copy.deepcopy(deck.hand_1)
    
    # Full round
    hand = 0 # 5 hands per game
    while hand < 4: # In the last hand, q_learning is different
        # Each hand
        # Seaparate the leading player
        if players[0] == learning_player:
            action = state.select_action(deck, trump, None)
            lead = action['suit']
            deck.hand_1.remove(action)
            state.play_card(action, 'us', 0)     
        else:
            card = strategy(players[i], trump, lead)
            lead = players[i]['suit']
            state.play_card(players[i][card], team, i)
            deck.players[i].delete(card)
                
        # Everybody else
        for i in range(1, len(players)):
            if players[i] == learning_player:
                action = state.select_action(deck, trump, lead)
                deck.hand_1.remove(action)
                state.play_card(action, 'us', 0)
                # Q-learning
                if hand > 0:
                    a2 = select_max_action(state, deck, trump, lead)
                    maxQ = state.value_approximation(a2)
                    # w <- w + alpha(r + gamma(maxQ(s',a) - Q(s,a))grad(Q(s,a))
                    weights = weights + alpha*(reward + gamma*maxQ - q)             
            else:
                if players[i] == deck.hand_3:
                    team = 'us'
                else:
                    team = 'them'
                card = strategy(players[i], trump, lead)
                state.play_card(players[i][card], team, i)
                deck.players[i].delete(card)
        # End of this state
        # Collect data for Q_learning
        reward = state.reward()
        q = state.value_approximation(action)
        # To finish Q_learning we need data from next state
                
        # See who leads next
        maxi = 0
        for i in range(1, len(self.hand)):
            if self.hand[i]['value'] > self.hand[maxi]['value']:
                maxi = i
        winner = self.hand[maxi]['player']
        players = players[winner:] + players[:winner]
        # Next hand begins
        hand += 1
    # Only one card left per players
    
    # Seaparate the leading player     
    lead =
    
    # Everybody else
    for i in range(1, len(players)):
        if players[i] == learning_player:
            action = deck.hand_1[0]
            deck.hand_1.remove(action)
            state.play_card(action, 'us', 0)
            # Q-learning
            # Terminal state has Q value of 0
            # w <- w + alpha(r + gamma(maxQ(s',a) - Q(s,a))grad(Q(s,a))
            weights = weights + alpha*(reward - q)             
        else:
            if players[i] == deck.hand_3:
                team = 'us'
            else:
                team = 'them'
            card = deck.players[i][0]
            deck.players[i].remove(card)
            state.play_card(card, team, i)
                
# Needs a overarching function for 'your turn'
def turn(hand, strategy, state, trump, deck):
    if len(state.hand) == 0:
        lead = None
    card = strategy(hand, trump, lead)
    return card

# Strategy = random_choice, greedy_choice, or strategic_choice
def game_setup(strategy):
    lead_player = pick_lead_player()
    players = [deck.hand_1, deck.hand_2, deck.hand_3, deck.hand_4]
    players = players[lead_player:] + players[:lead_player]
    run_round(strategy, players)
    
    
