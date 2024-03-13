
class Player:
    def __init__(self, initial_money):
        self.hand = []
        self.money = initial_money
        self.bet = 0

    def place_bet(self, amount):
        if amount > self.money:
            raise ValueError("Bet amount cannot be greater than available money")
        self.bet = amount
        self.money -= amount

    def receive_card(self, card):
        self.hand.append(card)
        self.hand.sort()

    def clear_hand(self):
        self.hand = []

    def win(self):
        self.money += 2 * self.bet
        self.bet = 0

    def lose(self):
        self.bet = 0