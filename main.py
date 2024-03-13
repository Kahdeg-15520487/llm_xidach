import guidance
from guidance import models, select, block, gen
from treys import Deck, Card, Evaluator
from pokerHelper import parse_card, parse_card_back, parse_hand, parse_hand_back
from player import Player

path_to_model = "dolphin-2.6-mistral-7b-dpo-laser.Q4_K_M.gguf"
lm = models.LlamaCpp(path_to_model, n_gpu_layers=-1, echo=False)
playerLm = lm + "I'm playing black jack, my hands are "
dealerLm = lm + "I'm playing black jack, i'm the dealer, the rule said that i can check if a player hand's score is larger than me or not, my hands are"

@guidance(stateless=True)
def player_hit(self,lm):
    return lm + ", should i hit or stand? i should " + select(name= "select", options= ["hit", "stand"])

@guidance(stateless=True)
def dealer_hit(self,lm):
    return lm + ", should i hit before checking other player? i should " + select(name= "select", options= ["hit", "stand"])

playerCount = 4
deck = Deck(1)
players = [Player(100) for _ in range(playerCount)]

for i in range(playerCount*2):
    players[i % 4].receive_card(deck.draw(1)[0])

for i in range(playerCount-1):
    while True:
        print(parse_hand(players[i].hand))
        prompt = ', '.join(parse_hand(players[i].hand))
        selection_result = player_hit(lm + prompt)
        print("player",str(i),selection_result["select"])
        if selection_result["select"] == "stand":
            break
        players[i].receive_card(deck.draw(1)[0])

