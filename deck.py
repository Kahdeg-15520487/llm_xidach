import random

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __repr__(self):
        return f"{self.value} of {self.suit}"

    @classmethod
    def from_string(cls, card_str):
        value, suit = card_str.split(' of ')
        return cls(suit, value)

    def __eq__(self, other):
        if isinstance(other, Card):
            return self.suit == other.suit and self.value == other.value
        return False

    def __lt__(self, other):
        if isinstance(other, Card):
            value_order = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
            suit_order = ["Clubs", "Diamonds", "Hearts", "Spades"]
            return value_order.index(self.value) < value_order.index(other.value) or \
                   (value_order.index(self.value) == value_order.index(other.value) and 
                    suit_order.index(self.suit) < suit_order.index(other.suit))
        return NotImplemented

    def __le__(self, other):
        return self == other or self < other

    def __gt__(self, other):
        return not self <= other

    def __ge__(self, other):
        return self == other or self > other

class Deck:
    def __init__(self):
        self.cards = [Card(s, v) for s in ["Spades", "Clubs", "Hearts", "Diamonds"]
                      for v in ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]]

    def shuffle(self, seed=1):
        if len(self.cards) > 1:
            random.seed(seed)
            random.shuffle(self.cards)

    def deal(self):
        if len(self.cards) > 1:
            return self.cards.pop(0)
        
class HandCombination:
    def __init__(self, combination, cards):
        self.combinations = combination
        self.cards = cards

    def __repr__(self):
        return self.combinations + ": " + ", ".join(str(card) for card in self.cards)
    
    
        
class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card: Card):
        self.cards.append(card)
        self.cards.sort(reverse=True)

    def __repr__(self):
        return ", ".join(str(card) for card in self.cards)
    
    def classify(self):
        # Define all possible hand combinations
        combinations = ["High Card", "Pair", "Two Pairs", "Three of a Kind", "Straight", "Flush", 
                        "Full House", "Four of a Kind", "Straight Flush", "Royal Flush"]
        possible_combinations = []

        # Check for each combination
        for combination in combinations:
            if getattr(self, f"is_{combination.replace(' ', '_').lower()}")():
                possible_combinations.append(HandCombination(combination, self.cards))

        return possible_combinations

    # Define methods to check for each hand combination
    def is_high_card(self):
        return len(self.cards) > 0

    def is_pair(self):
        values = [card.value for card in self.cards]
        return len(set(values)) < len(values)

    def is_two_pairs(self):
        values = [card.value for card in self.cards]
        return len(set(values)) <= len(values) - 2

    def is_three_of_a_kind(self):
        values = [card.value for card in self.cards]
        return any(values.count(value) == 3 for value in values)

    def is_straight(self):
        values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        card_values = [values.index(card.value) for card in self.cards]
        card_values.sort()
        return all(card_values[i] - card_values[i-1] == 1 for i in range(1, len(card_values)))

    def is_flush(self):
        suits = [card.suit for card in self.cards]
        return len(set(suits)) == 1

    def is_full_house(self):
        return self.is_three_of_a_kind() and self.is_pair()

    def is_four_of_a_kind(self):
        values = [card.value for card in self.cards]
        return any(values.count(value) == 4 for value in values)

    def is_straight_flush(self):
        return self.is_straight() and self.is_flush()

    def is_royal_flush(self):
        return self.is_straight_flush() and all(card.value in ["10", "J", "Q", "K", "A"] for card in self.cards)
    
if __name__ == "__main__":
    # Create a new deck of cards
    deck = Deck()

    # Shuffle the deck
    deck.shuffle(10)

    # Create two hands
    hand1 = Hand()
    hand2 = Hand()

    # Deal the cards to each hand
    for _ in range(5):
        hand1.add_card(deck.deal())
        hand2.add_card(deck.deal())

    # Print the hands
    print("Hand 1: ", hand1)
    print("combinations: ")
    for combination in hand1.classify():
        print(combination)
    print()
    print("Hand 2: ", hand2)
    print("combinations: ")
    for combination in hand2.classify():
        print(combination)