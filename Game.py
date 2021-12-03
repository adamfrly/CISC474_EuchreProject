# File for setting up a run-through of the game
# Not yet integrated with all the files
    # Havent' been able to confirm that it works because of this

# Global for the game
# Initialize feaure weights
import numpy as np
# w1, w2, w3, b = 1, 1, 1, 0
#SUITS = ['Spades', 'Hearts', 'Clubs', 'Diamonds']
SUITS = [0, 1, 2, 3]
#CARDS = ['9', '10', 'Jack', 'Queen', 'King', 'Ace']
# CARDS = [2, 3, 4, 5, 6, 7]

from Feature_Approximation import State
from Deck import Deck
from rules import add_card_rank
from dumb_player import random_choice, greedy_choice, strategic_choice

import random
import copy

def pick_trump():
    return random.choice(SUITS)

def pick_lead_player():
    # Represents an index in the list of players
    # Each player linked to a hand
    return random.choice([0, 1, 2, 3])
            
def run_round(deck, state, strategy, players, epsilon, alpha, gamma, weights):
    trump = pick_trump()    
    # Full round
    hand = 0 # 5 hands per game
    while hand < 4: # In the last hand, q_learning is different
        # Each hand
        # Seaparate the leading player
        if players[0] == deck.hand_1:
            for k in deck.hand_1:
                print(deck.hand_1)
                add_card_rank(k, trump, None)
            action = state.select_action(deck, trump, None, epsilon, weights)
            lead = action['suit']
            deck.hand_1.remove(action)
            state.play_card(action, 'us', 0)     
        else:
            if players[0] == deck.hand_3:
                team = 'us'
            else:
                team = 'them'
            card = strategy(players[0], trump, None)
            lead = players[0][0]['suit']
            state.play_card(players[0][card], team, 0)
            print(card)
            print(deck.hand_3)
            deck.hand_3.pop(card)    
            for k in deck.hand_1:
                add_card_rank(k, trump, lead)
        # Everybody else
        for i in range(1, len(players)):
            if players[i] == deck.hand_1:
                action = state.select_action(deck, trump, lead, epsilon, weights)
                deck.hand_1.remove(action)
                state.play_card(action, 'us', 0)
                # Q-learning
                if hand > 0:
                    if hand == 4:
                        maxQ = 0
                    else:
                        a2 = state.select_max_action(deck, trump, lead, weights)
                        maxQ = state.value_approximation(a2, weights)
                    # w <- w + alpha(r + gamma(maxQ(s',a) - Q(s,a))grad(Q(s,a))
                    weights = weights + alpha*(reward + gamma*maxQ - q) * state.features       
            else:
                if players[i] == deck.hand_3:
                    team = 'us'
                else:
                    team = 'them'
                card = strategy(players[i], trump, lead)
                state.play_card(players[i][card], team, i)
                if card in deck.hand_2:
                    deck.hand_2.pop(card)
                elif card in deck.hand_3:
                    deck.hand_3.pop(card)
                elif card in deck.hand_4:
                    deck.hand_4.pop(card)
        # End of this state
        # Collect data for Q_learning
        print(state.hand)
        reward = state.reward()
        q = state.value_approximation(action, weights)
        # To finish Q_learning we need data from next state
                
        # See who leads next
        maxi = 0
        for i in range(1, len(state.hand)):
            if state.hand[i]['card_rank'] > state.hand[maxi]['card_rank']:
                maxi = i
        winner = state.hand[maxi]['player']
        players = players[winner:] + players[:winner]
        # Next hand begins
        hand += 1
        state.hand = []
    return weights


# Strategy = random_choice, greedy_choice, or strategic_choice
def game_setup(strategy, epsilon, alpha, gamma):
    weights = np.array([1, 1, 1, 0])
    state = State()
    deck = Deck()
    for i in range(10):
        deck.shuffle()
        deck.deal()
        lead_player = pick_lead_player()
        players = [deck.hand_1, deck.hand_2, deck.hand_3, deck.hand_4]
        players = players[lead_player:] + players[:lead_player]
        weights = run_round(deck, state, strategy, players, epsilon, alpha, gamma, weights)
        print(weights)
    

game_setup(random_choice, 0.1, 0.5, 0.8)
