import random
import numpy as np
from rules import is_lead, legal_move, add_card_rank, is_trump, is_lead
from operator import itemgetter
# Creating types player that plays somewhat intelligently (strong emphasis on somewhat)
# (Done) 1. Random player: Will randomly pick a card to play until it picks a legal one (very bad)
# (Done) 2. Greedy Player: Will play the highest rank card it is allowed to play (pretty bad)
# (Done) 3. Strategic Player: Plays the highest card it can if it has either a trump card, lead suit card or is leading, otherwise plays the lowest card it can

def argmax(iterable):
    return max(enumerate(iterable), key=lambda x: x[1])[0]

def argmin(iterable):
    return min(enumerate(iterable), key=lambda x: x[1])[0]

def random_choice(hand, trump, lead):
    """
    Gives an index from 0 to 4 on which card to play
    How a random player would choose which cards to play
    """
    legal_choice = False
    while not legal_choice:
        choice = random.sample(hand, 1)[0]
        if lead == None:
            legal_choice = legal_move(choice, choice['suit'], hand, trump)
        else:
            legal_choice = legal_move(choice, lead, hand, trump)
    [add_card_rank(card, trump, choice['suit']) for card in hand]
    return hand.index(choice)

def greedy_choice(hand, trump, lead):
    """
    Gives an index from 0 to 4 on which card to play
    Plays the highest rank legal card (i.e. card that doesn't lead to reneging) each and every trick.
    This function will also add the "card_ranks" key to the dictonary that describes the cards
    """
    if lead == None: # If this is the lead card
        [add_card_rank(card, trump, card['suit']) for card in hand]
        ranks_no_lead = list(map(itemgetter('card_rank'), hand))
        return argmax(ranks_no_lead)
    
    [add_card_rank(card, trump, lead) for card in hand]
    ranks = list(map(itemgetter('card_rank'), hand))
    choices_avail = np.array([1 if legal_move(card, lead, hand, trump) else 0 for card in hand])

    return argmax(ranks * choices_avail)

def strategic_choice(hand, trump, lead):
    """
    Gives an index from 0 to 4 on which card to play
    Will play the highest trump and/or legal move if there is one, otherwise it'll play the lowest ranked card.
    This function will also add the "card_ranks" key to the dictonary that describes the cards
    """
    if lead == None: # If this is the lead card
        hand_with_ranks_no_lead = np.array([add_card_rank(card, trump, card['suit']) for card in hand])
        ranks_no_lead = list(map(itemgetter('card_rank'), hand_with_ranks_no_lead))
        if max(ranks_no_lead) < 10: # If the player doesn't have at least a non-trump king to lead with
            return argmin(ranks_no_lead)
        else:
            return argmax(ranks_no_lead)

    hand_with_ranks = np.array([add_card_rank(card, trump, lead) for card in hand]) # Finds the strength of each card in a players hand
    ranks = list(map(itemgetter('card_rank'), hand_with_ranks))
    choices_avail = np.array([1 if legal_move(card, lead, hand, trump) else 0 for card in hand])
    avail_ranks = ranks * choices_avail

    trumps_avail = np.array([1 if is_trump(card, trump) else 0 for card in hand])
    ranks_trump = avail_ranks * trumps_avail
    if not np.any(ranks_trump):
        return np.argmax(ranks_trump) # Tries to play its highest trump that is allowed
    
    leads_avail = np.array([1 if is_lead(card, trump, lead) else 0 for card in hand])
    ranks_lead = avail_ranks * leads_avail
    if not np.any(ranks_lead):
        return np.argmax(ranks_lead) # Tries to play its highest lead suit that is allowed

    min_rank = np.min(avail_ranks[np.nonzero(avail_ranks)]) # Lowest rank non-zero (i.e. legal) card to play
    return np.where(avail_ranks == min_rank)[0][0] # returns the index of that card
