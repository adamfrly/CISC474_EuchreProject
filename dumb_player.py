import random
import numpy as np
from rules import is_lead, legal_move, add_card_rank, is_trump, is_lead
from operator import itemgetter

# Three strategies of varying difficulty for non-learning agents to follow
# Other functions are included to assist in the implementation of these strategies

def argmax(iterable):
    """
    Returns the argmax of an iterable
    """
    return max(enumerate(iterable), key=lambda x: x[1])[0]

def argmin(iterable):
    """
    Returns the argmin of an iterable
    """
    return min(enumerate(iterable), key=lambda x: x[1])[0]

def random_choice(hand, trump, lead):
    """
    Gives an index from 0 to 4 on which card to play
    Randomly samples a card, if it's legal, that card is played
    """
    legal_choice = False
    while not legal_choice:
        choice = random.sample(hand, 1)[0]
        if lead == None: # If there is no lead set yet (i.e. this player is the leader)
            legal_choice = legal_move(choice, choice['suit'], hand, trump)
        else:
            legal_choice = legal_move(choice, lead, hand, trump)
    [add_card_rank(card, trump, choice['suit']) for card in hand]
    return hand.index(choice)

def greedy_choice(hand, trump, lead):
    """
    Gives an index from 0 to 4 on which card to play
    Plays the highest rank legal card (i.e. card that doesn't lead to reneging) each and every trick.
    """
    if lead == None: # If this is the lead card
        [add_card_rank(card, trump, card['suit']) for card in hand] # Adds the card_rank to the definition of the card's dictionary
        ranks_no_lead = list(map(itemgetter('card_rank'), hand))
        return argmax(ranks_no_lead) # Returns the index of the card with the highest rank
    
    [add_card_rank(card, trump, lead) for card in hand]
    ranks = list(map(itemgetter('card_rank'), hand))
    choices_avail = np.array([1 if legal_move(card, lead, hand, trump) else 0 for card in hand]) # Sets all illegal card ranks to zero

    return argmax(ranks * choices_avail) # Returns the index of the max ranked card 

def strategic_choice(hand, trump, lead):
    """
    Gives an index from 0 to 4 on which card to play
    Will play the highest trump and/or legal move if there is one, otherwise it'll play the lowest ranked card.
    """
    if lead == None: # If this is the lead card
        hand_with_ranks_no_lead = np.array([add_card_rank(card, trump, card['suit']) for card in hand])
        ranks_no_lead = list(map(itemgetter('card_rank'), hand_with_ranks_no_lead))
        if max(ranks_no_lead) < 10: # If the player doesn't have at least a non-trump king to lead with
            return argmin(ranks_no_lead) # Returns the index of the lowest possible legal move
        else:
            return argmax(ranks_no_lead) # Returns the index of the lowest possible legal move

    hand_with_ranks = np.array([add_card_rank(card, trump, lead) for card in hand]) # Finds the strength of each card in a players hand
    ranks = list(map(itemgetter('card_rank'), hand_with_ranks))
    choices_avail = np.array([1 if legal_move(card, lead, hand, trump) else 0 for card in hand]) 
    avail_ranks = ranks * choices_avail # Sets the rank of all illegal moves to 0

    trumps_avail = np.array([1 if is_trump(card, trump) else 0 for card in hand]) # Checks if there are any trumps available for the agent to play
    ranks_trump = avail_ranks * trumps_avail
    if not np.any(ranks_trump):
        return np.argmax(ranks_trump) # Tries to play its highest trump that is allowed
    
    leads_avail = np.array([1 if is_lead(card, trump, lead) else 0 for card in hand]) # Checks if the player has any lead cards it can play
    ranks_lead = avail_ranks * leads_avail
    if not np.any(ranks_lead):
        return np.argmax(ranks_lead) # Tries to play its highest lead suit that is allowed

    min_rank = np.min(avail_ranks[np.nonzero(avail_ranks)]) # Lowest rank non-zero (i.e. legal) card to play
    return np.where(avail_ranks == min_rank)[0][0] # Returns the index of the weakest legal card
