import numpy as np
import copy

# A series of logical checks and operations that are useful when enforcing the rules of Euchre

def lower_bower(trump):
    """
    Suits are represented by a number from 0-3. This function tells you the number of the
    left bower's suit (the suit with the same colour)
    """
    return trump - 2 if trump - 2 >= 0 else trump + 2

def is_leftbower(card, trump):
    """
    Determines if a card is the left bower (Jack with suit of the same colour as the trump suit)
    """
    if card['number'] != 2:
        return False
    l_bower = lower_bower(trump)
    if card['suit'] == l_bower:
        return True
    return False

def is_trump(card, trump):
    """
    Determines if a suit is trump. The left bower is considered a trump
    """
    if card['suit'] == trump:
        return True
    if is_leftbower(card):
        return True
    return False

def is_lead(card, trump, lead):
    """
    Determines if a card is the lead suit. The left bower is considered the same suit as trump
    """
    if card['suit'] == lead:
        return True
    if lead == trump:
        if is_leftbower(card, trump):
            return True
    return False

def greater_than(card, other, lead, trump):
    """
    Checks if one card is larger than another based on the current trump
    """
    l_bower = lower_bower(trump)
    c_rank = card['number']
    o_rank = other['number']

    if (card['number'] == 2) or (other['number'] == 2): # Dealing with the annoying case of bowers
        if card == {'suit' : trump, 'number' : 2}: # Right bower is always largest
            return True
        elif other == {'suit' : trump, 'number' : 2}:
            return False
        elif card == {'suit' : l_bower, 'number' : 2}: # Left Bower is always second largest
            return True 
        elif other == {'suit' : l_bower, 'number' : 2}:
            return False
    if card['suit'] == trump: # Trumps are always above non-trumps
        c_rank += 12
    if other['suit'] == trump:
        o_rank += 12
    if card['suit'] == lead: # Leads are always above non-lead cards
        c_rank += 6
    if other['suit'] == lead:
        o_rank += 6
    print(f"First rank: {c_rank}\nSecond rank: {o_rank}")
    return c_rank > o_rank

def card_rank(card, trump, lead):
    """
    Finds the strength of a card from 0 to 25 based on its rank, the trump suit, and the lead suit
    """
    rank = card['number']
    l_bower = lower_bower(trump)
    if card['number'] == 2: # Getting rid of bowers
        if card['suit'] == trump: # Right bower
            return 25
        elif card['suit'] == l_bower: # Left Bower
            return 24 
    if card['suit'] == trump:
        rank += 12
    elif card['suit'] == lead:
        rank += 6
    return rank

def add_card_rank(card, trump, lead):
    """
    Adds the rank of the card to the dictionary that describes it. The dictionary key is "card_rank".
    Card dictionary is {suit: int, number: int, card_rank: int}
    Number is the value on the face of the card. Rank is the strength of the card for that hand
    """
    rank = card_rank(card, trump, lead)
    card['card_rank'] = rank

def legal_move(played, lead, hand_with, trump):
    """
    Checks if the card to be played is legal. There are three main cases, all revolving
    around how involved the left bower is
    """
    hand = copy.deepcopy(hand_with) # Creating a copy of the hand to manipulate
    hand.remove(played) # Hand without the card to be played

    l_bower = lower_bower(trump)
    left_in_hand = {'suit' : l_bower, 'number' : 2} in hand # Boolean if the left bower is in the player's hand
    left_played = {'suit' : l_bower, 'number' : 2} == played # Boolean if the left bower is being played

    if not (left_in_hand and left_played): # Left bower is not involved at all
        played_lead = played['suit'] == lead
        has_lead_suit = any(card['suit']==lead for card in hand)
        return played_lead or not has_lead_suit # Returns True when a lead suit is played or when a non lead uit is played but the player doesn't have any lead suit
    elif left_played: # Left bower was played
        played_lead = trump == lead # Makes sure l_bower is treated as a trump
        has_lead_suit = any(card['suit']==lead for card in hand)
        return played_lead or not has_lead_suit
    elif left_in_hand: # Left bower is in hand
        played_lead = played['suit'] == lead
        has_lead_suit = any(card['suit']==lead for card in hand) or lead == trump # Ensures l_bower is treated as trump
        return played_lead or not has_lead_suit
    return "You should not be getting to this point"
