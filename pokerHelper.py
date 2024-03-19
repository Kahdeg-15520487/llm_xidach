from treys import Card

def parse_card(card: int):
    return parse_card_str(Card.int_to_str(card))

def parse_hand(hand: list):
    parsed_hand = []
    for card in hand:
        parsed_hand.append(parse_card_str(Card.int_to_str(card)))
    return parsed_hand

def parse_hand_back(hand: list):
    parsed_hand = []
    for card in hand:
        parsed_hand.append(parse_card_str_back(card))
    return parsed_hand

def parse_card_str(card_str):
    card_value = card_str[0]
    card_suit = card_str[1]

    card_value_dict = {
        'T': '10',
        'J': 'J',
        'Q': 'Q',
        'K': 'K',
        'A': 'A'
    }

    card_suit_dict = {
        's': 'Spades',
        'h': 'Hearts',
        'd': 'Diamonds',
        'c': 'Clubs'
    }

    return f"{card_value_dict.get(card_value, card_value)} of {card_suit_dict[card_suit]}"

def parse_card_str_back(card):
    card_str = card.split(" of ")
    card_value = card_str[0]
    card_suit = card_str[1]

    card_value_dict = {
        '10': 'T',
        'J': 'J',
        'Q': 'Q',
        'K': 'K',
        'A': 'A'
    }

    card_suit_dict = {
        'Spades': 's',
        'Hearts': 'h',
        'Diamonds': 'd',
        'Clubs': 'c'
    }

    return f"{card_value_dict.get(card_value, card_value)}{card_suit_dict[card_suit]}"

def pretty_print_hand(hand: list):
    return ', '.join(parse_hand(hand))