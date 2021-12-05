import numpy as np
#SUITS = ['Spades', 'Hearts', 'Clubs', 'Diamonds']
SUITS = [0, 1, 2, 3]

from Feature_Lone_Wolf import State
from Deck import Deck
from rules import add_card_rank
from dumb_player import random_choice, greedy_choice, strategic_choice

import random
import copy

# Randomly choose the trump for a round
def pick_trump():
    return random.choice(SUITS)

# Randomly pick one player to lead the first hand
def pick_lead_player():
    # Represents an index in the list of players
    # Each player linked to a hand
    return random.choice([0, 1, 2, 3])
            
def run_round(deck, state, strategy, learning_player, epsilon, alpha, gamma, weights):
    trump = pick_trump()  
    tricks = 0
    # Full round
    hand = 0 # 5 hands per game
    while hand < 4:
        # Each hand
        # Seaparate the leading player
        if deck.players[0] == learning_player:
            # Learning agent is leading
            for k in deck.players[0]:
                # Rank all of the learning agents card values
                add_card_rank(k, trump, None)
            action = state.select_action(deck.players[0], trump, None, epsilon, weights)
            # Set lead as the suit of this first card played
            lead = action['suit']
            deck.players[0].remove(action)
            state.play_card(action, 0, 'me')     
        else:
            # Non-learning agent is leading
            card = strategy(deck.players[0], trump, None)
            # Set lead of the suit of this first card played
            lead = deck.players[0][card]['suit']
            state.play_card(deck.players[0][card], 0, 'them')
            deck.players[0].pop(card)
            for k in range(len(deck.players)):
                if deck.players[k] == learning_player:
                    for f in deck.players[k]:
                        # Rank all of the learning agents card values
                        add_card_rank(f, trump, lead)
        # Non-leading players
        for i in range(1, len(deck.players)):
            if deck.players[i] == learning_player:
                action = state.select_action(deck.players[i], trump, lead, epsilon, weights)
                deck.players[i].remove(action)
                state.play_card(action, i, 'me')
                # Q-learning
                if hand > 0:
                    # Requires information from the next hand, so weights are updated starting at the 2nd hand
                    a2 = state.select_max_action(deck.players[i], trump, lead, weights)
                    maxQ = state.value_approximation(a2, weights)
                    # w <- w + alpha(r + gamma(maxQ(s',a) - Q(s,a))grad(Q(s,a))
                    #print("weights: ", weights, "alpha: ", alpha, "reward: ", reward, "gamma: ",  gamma, "maxQ: ", maxQ, "q: ", q_value, "state: ", f_value)
                    weights = weights + alpha*(reward + gamma*maxQ - q_value) * f_value  
            else:
                # Non-learning agent plays a card
                card = strategy(deck.players[i], trump, lead)
                state.play_card(deck.players[i][card], i, 'them')
                deck.players[i].pop(card)
        # End of this state
        # Collect data for Q_learning
        reward = state.reward()
        q_value = state.value_approximation(action, weights)
        f_value = state.features
        # To finish Q_learning we need data from next state
                
        # See who leads next
        maxi = 0
        for i in range(1, len(state.hand)):
            if state.hand[i]['card_rank'] > state.hand[maxi]['card_rank']:
                maxi = i
        winner = state.hand[maxi]['index']
        deck.players = deck.players[winner:] + deck.players[:winner]
        trick = state.hand[maxi]['player']
        # Check if the learning player won the trick
        if trick == 'me':
            tricks += 1
        # Next hand begins
        hand += 1
        state.hand = []
    # Final weight update after the last hand of the round
    # maxQ = 0
    weights = weights + alpha*(reward - q_value) * f_value
    return weights, tricks


# Strategy = random_choice, greedy_choice, or strategic_choice
# Run through iterations of the model
# Length of for loops indicates the number of training trials
def game_setup(strategy, epsilon, alpha, gamma):
    weights = np.array([0, 0, 0, 0, 0])
    state = State()
    deck = Deck()
    trick_total = 0
    for j in range(100):
        trick_total = 0
        for i in range(100):
            deck.shuffle()
            deck.deal()
            lead_player = pick_lead_player()
            learning_player = deck.players[0]
            deck.players = deck.players[lead_player:] + deck.players[:lead_player]
            weights, tricks = run_round(deck, state, strategy, learning_player, epsilon, alpha, gamma, weights)
            trick_total += tricks
        print(trick_total/100)
        print(weights, tricks)
    

game_setup(greedy_choice, 0.1, 0.1, 0.8)
