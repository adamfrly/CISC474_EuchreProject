# Rules that need to be implemented:
# Adjusting the suit ranks depending on trump
# Checking if a move is legal depending on the lead and their hand
# Checking if they've reneged (alternative to the above rule)

def lower_bower(trump):
    return trump - 2 if trump - 2 > 0 else trump + 2
# Need to ask Grace to have suits ordered like this ['Hearts', 'Spades', 'Diamonds', 'Clubs'] for this to work

def greater_than(card, other, trump):
    """
    Checks if one card is larger than another based on the current trump
    """
    c_rank = card['number']
    o_rank = other['number']
    if card['number'] != 2: # Isn't a jack
        if card['suit'] == trump:
            c_rank += 6
        if other['suit'] == trump:
            o_rank += 6
    else:
        l_bower = lower_bower(trump)
        if card['suit'] == trump:
            c_rank = 13
        elif card['suit'] == l_bower:
            c_rank = 12
        if other['suit'] == trump:
            o_rank = 13
        elif other['suit'] == l_bower:
            o_rank = 12
    return c_rank > o_rank

def legal_move(played, lead, hand, trump):
    l_bower = lower_bower(trump)
    if not ({'suit' : l_bower, 'number' : 2} in hand and {'suit' : l_bower, 'number' : 2} == played): # If left bower is not involved at all
        played_lead = played['suit'] == lead
        has_lead_suit = any(card['suit']==lead for card in hand)
        return played_lead or not has_lead_suit # Check with Grace, this might be wrong, I made a truth table but not sure
    elif {'suit' : l_bower, 'number' : 2} == played:
        played_lead = trump == lead
        has_lead_suit = any(card['suit']==lead for card in hand)
        return played_lead or not has_lead_suit # Check with Grace, this might be wrong, I made a truth table but not sure
    elif {'suit' : l_bower, 'number' : 2} in hand:
        played_lead = played['suit'] == lead
        has_lead_suit = any(card['suit']==lead for card in hand) or lead == trump
        return played_lead or not has_lead_suit # Check with Grace, this might be wrong, I made a truth table but not sure
    return "Somehow you fucked up bad"