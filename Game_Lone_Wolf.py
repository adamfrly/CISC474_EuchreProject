# File for setting up a run-through of the game
# Not yet integrated with all the files
    # Havent' been able to confirm that it works because of this

# Global for the game
# Initialize feaure weights
import numpy as np
# w1, w2, w3, b = 1, 1, 0
#SUITS = ['Spades', 'Hearts', 'Clubs', 'Diamonds']
SUITS = [0, 1, 2, 3]
#CARDS = ['9', '10', 'Jack', 'Queen', 'King', 'Ace']
# CARDS = [2, 3, 4, 5, 6, 7]

from Feature_Lone_Wolf import State
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
            
def run_round(deck, state, strategy, learning_player, epsilon, alpha, gamma, weights):
    trump = pick_trump()
    #print("trump: ", trump)  
    tricks = 0
    # Full round
    hand = 0 # 5 hands per game
    while hand < 4: # In the last hand, q_learning is different
        # Each hand
        # Seaparate the leading player
        #print(learning_player)
        if deck.players[0] == learning_player:
            for k in deck.players[0]:
                add_card_rank(k, trump, None)
            action = state.select_action(deck.players[0], trump, None, epsilon, weights)
            #print("lead action: ", action)
            lead = action['suit']
            deck.players[0].remove(action)
            state.play_card(action, 0, 'me')     
        else:
            #print("lead player's hand (CPU): ", deck.players[0])
            card = strategy(deck.players[0], trump, None)
            #print("Lead card (CPU): ", card)
            lead = deck.players[0][card]['suit']
            state.play_card(deck.players[0][card], 0, 'them')
            deck.players[0].pop(card)
            for k in range(len(deck.players)):
                if deck.players[k] == learning_player:
                    for f in deck.players[k]:
                        add_card_rank(f, trump, lead)
        # Everybody else
        for i in range(1, len(deck.players)):
            #print(f"{i}th player's hand: ", deck.players[i])
            if deck.players[i] == learning_player:
                #print("Lead suit: ", lead)
                #print(state.hand)
                action = state.select_action(deck.players[i], trump, lead, epsilon, weights)
                #print(f"{i}th player's action: ", action)
                deck.players[i].remove(action)
                state.play_card(action, i, 'me')
                # Q-learning
                if hand > 0:
                    a2 = state.select_max_action(deck.players[i], trump, lead, weights)
                    maxQ = state.value_approximation(a2, weights)
                    # w <- w + alpha(r + gamma(maxQ(s',a) - Q(s,a))grad(Q(s,a))
                    #print("weights: ", weights, "alpha: ", alpha, "reward: ", reward, "gamma: ",  gamma, "maxQ: ", maxQ, "q: ", q_value, "state: ", f_value)
                    weights = weights + alpha*(reward + gamma*maxQ - q_value) * f_value
                    #print("update: ", weights)   
            else:
                card = strategy(deck.players[i], trump, lead)
                #print(f"{i}th player's action (CPU): ", card)
                state.play_card(deck.players[i][card], i, 'them')
                deck.players[i].pop(card)
        # End of this state
        # Collect data for Q_learning
        #print(state.hand)
        reward = state.reward()
        #print("reward: ", reward)
        q_value = state.value_approximation(action, weights)
        #print("q_value: ", q_value)
        f_value = state.features
        #print("f_value: ", f_value)
        # To finish Q_learning we need data from next state
                
        # See who leads next
        maxi = 0
        for i in range(1, len(state.hand)):
            if state.hand[i]['card_rank'] > state.hand[maxi]['card_rank']:
                maxi = i
        winner = state.hand[maxi]['index']
        deck.players = deck.players[winner:] + deck.players[:winner]
        trick = state.hand[maxi]['player']
        if trick == 'me':
            tricks += 1
        #print("Ending state: ", state.hand)
        #print("tricks won by agent: ", tricks)
        # Next hand begins
        hand += 1
        state.hand = []
    weights = weights + alpha*(reward - q_value) * f_value
    return weights, tricks


# Strategy = random_choice, greedy_choice, or strategic_choice
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
