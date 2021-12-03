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
            
def run_round(deck, state, strategy, learning_player, teammate, epsilon, alpha, gamma, weights):
    trump = pick_trump()    
    # Full round
    hand = 0 # 5 hands per game
    while hand < 4: # In the last hand, q_learning is different
        # Each hand
        # Seaparate the leading player
        if deck.players[0] == learning_player:
            for k in deck.players[0]:
                print(deck.players[0])
                add_card_rank(k, trump, None)
            action = state.select_action(deck, trump, None, epsilon, weights)
            lead = action['suit']
            deck.players[0].remove(action)
            learning_player.remove(action)
            state.play_card(action, 'us', 0)     
        else:
            if deck.players[0] == teammate:
                team = 'us'
            else:
                team = 'them'
            card = strategy(deck.players[0], trump, None)
            lead = deck.players[0][0]['suit']
            state.play_card(deck.players[0][card], team, 0)
            deck.players[0].pop(card)
            if deck.players[0] == teammate:
                teammate.pop(card)
            for k in deck.hand_1:
                add_card_rank(k, trump, lead)
        # Everybody else
        for i in range(1, len(deck.players)):
            if deck.players[i] == learning_player:
                action = state.select_action(deck, trump, lead, epsilon, weights)
                deck.players[i].remove(action)
                learning_player.remove(action)
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
                if deck.players[i] == teammate:
                    team = 'us'
                else:
                    team = 'them'
                card = strategy(deck.players[i], trump, lead)
                state.play_card(deck.players[i][card], team, i)
                deck.players[i].pop(card)
                if deck.players[0] == teammate:
                    teammate.pop(card)
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
        learning_player = deck.players[0]
        teammate = deck.players[2]
        deck.players = deck.players[lead_player:] + deck.players[:lead_player]
        weights = run_round(deck, state, strategy, learning_player, teammate, epsilon, alpha, gamma, weights)
        print(weights)
    

game_setup(random_choice, 0.1, 0.5, 0.8)
