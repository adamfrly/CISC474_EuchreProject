import numpy as np
import copy

# Rules that need to be implemented:
# Adjusting the suit ranks depending on trump
# Checking if a move is legal depending on the lead and their hand
# Checking if they've reneged (alternative to the above rule)

def lower_bower(trump):
    return trump - 2 if trump - 2 >= 0 else trump + 2
# Need to ask Grace to have suits ordered like this ['Hearts', 'Spades', 'Diamonds', 'Clubs'] for this to work    

def is_leftbower(card, trump):
    if card['number'] != 2:
        return False
    l_bower = lower_bower(trump)
    if card['suit'] == l_bower:
        return True
    return False

def is_trump(card, trump):
    if card['suit'] == trump:
        return True
    if is_leftbower(card):
        return True
    return False

def is_lead(card, trump, lead):
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

    if (card['number'] == 2) or (other['number'] == 2): # Getting rid of bowers
        if card == {'suit' : trump, 'number' : 2}: # Right bower
            return True
        elif other == {'suit' : trump, 'number' : 2}:
            return False
        elif card == {'suit' : l_bower, 'number' : 2}: # Left Bower
            return True 
        elif other == {'suit' : l_bower, 'number' : 2}:
            return False
    if card['suit'] == trump:
        c_rank += 12
    if other['suit'] == trump:
        o_rank += 12
    if card['suit'] == lead:
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
            return 27
        elif card['suit'] == l_bower: # Left Bower
            return 26 
    if card['suit'] == trump:
        rank += 12
    elif card['suit'] == lead:
        rank += 6
    return rank

def add_card_rank(card, trump, lead):
    """
    Adds the rank of the card to the dictionary that describes it. The dictionary key is "card_rank".
    """
    rank = card_rank(card, trump, lead)
    card['card_rank'] = rank

def legal_move(played, lead, hand_with, trump):
    hand = copy.deepcopy(hand_with)
    hand.remove(played)
    l_bower = lower_bower(trump)
    left_in_hand = {'suit' : l_bower, 'number' : 2} in hand
    left_played = {'suit' : l_bower, 'number' : 2} == played

    if not (left_in_hand and left_played): # Left bower is not involved at all
        played_lead = played['suit'] == lead
        has_lead_suit = any(card['suit']==lead for card in hand)
        return played_lead or not has_lead_suit # Check with Grace, this might be wrong, I made a truth table but not sure
    elif left_played:
        played_lead = trump == lead
        has_lead_suit = any(card['suit']==lead for card in hand)
        return played_lead or not has_lead_suit
    elif left_in_hand:
        played_lead = played['suit'] == lead
        has_lead_suit = any(card['suit']==lead for card in hand) or lead == trump
        return played_lead or not has_lead_suit
    return "Somehow you fucked up bad"


# def main():
#     # {'suit' : suit, 'number' : number}
#     # ['Hearts', 'Spades', 'Diamonds', 'Clubs']
#     # (card, other, lead, trump)
#     nine_hearts = {'suit': 0, 'number' : 0}
#     queen_diamonds = {'suit': 2, 'number' : 3}
#     jack_hearts = {'suit': 0, 'number' : 2}
#     jack_diamonds = {'suit': 2, 'number' : 2}
#     ace_spades = {'suit': 1, 'number' : 5}
#     ten_clubs = {'suit': 3, 'number' : 1}
#     ten_hearts = {'suit': 0, 'number' : 1}

#     print(greater_than(nine_hearts, ten_hearts, 3, 1))
#     print(greater_than(nine_hearts, ten_hearts, 3, 0))
#     print(greater_than(nine_hearts, ten_hearts, 0, 0))
#     print(greater_than(queen_diamonds, jack_diamonds, 0, 0))
#     print(greater_than(queen_diamonds, jack_hearts, 0, 0))
#     print(greater_than(ace_spades, jack_diamonds, 1, 0))
#     print(greater_than(ten_clubs, jack_diamonds, 3, 2))
#     print(greater_than(nine_hearts, ace_spades, 0, 2))
#     print(greater_than(nine_hearts, ace_spades, 0, 1))
#     print(greater_than(nine_hearts, ace_spades, 1, 0))

# main()
