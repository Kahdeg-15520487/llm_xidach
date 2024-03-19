import guidance
from guidance import models, select, block, gen
from treys import Deck, Card, Evaluator
from pokerHelper import parse_card, parse_card_str, parse_card_str_back, parse_hand, parse_hand_back, pretty_print_hand
from player import Player

path_to_model = "dolphin-2.6-mistral-7b-dpo-laser.Q4_K_M.gguf"
# path_to_model = "mistral-7b-v0.1.Q6_K.gguf"
ruleLm = models.LlamaCpp(path_to_model, n_gpu_layers=-1, echo=False, temperature=0.7, n_ctx=2048)
ruleLm+= "I'm playing black jack, with some custom rules, the custom rules are: "
ruleLm+= " at the beginning of the game, the dealer will deal everyone, including themselves, two cards, face down, so no one can see others cards."
ruleLm+= " the dealer will then go 1 last turn, asking the player whether they want to hit or stand until that player decide to stand, and then move on to the next player."
ruleLm+= " each player will only be able to draw their card in the above turn"
ruleLm+= " the dealer will then reveal their hand, and then draw cards until their total points exceed 15, then they will check other player hands."
ruleLm+= " the cards from 2 to 10 are worth their face value, face cards (jack,queen,king) are worth 10"
ruleLm+= " aces are worth either 10 or 11 when it is beneficial (push the score closer to 21) to the player, and 1 when player have a score of 12 or more without counting the ace."
ruleLm+= " if the hand's score is more than 21, the hand is busted"
ruleLm+= " if the hand's score is less than 16, the hand is not legal"
ruleLm+= " the best hand possible would be 5 card with score at most 21, then 2 Ace, then an Ace with a 10 or a face card, then the highest total points that is at most 21."
ruleLm+= " the player's hand must be at least 16 (legal), if the hand's scored is less than 16, the player will not earn their bet even if the dealer is busted."
ruleLm+= " the dealer can check if a player hand's score is legal (at least 16)"
ruleLm+= " a player can stand on any total points, but the dealer must be 15 or more to check other player hands"
ruleLm+= " the dealer can check if a player hand's score is larger than his hand or not"
ruleLm+= " the dealer can continue to draw cards until they choose to stop or their total points exceed 21."
ruleLm+= " if the dealer and player both have the same total points, the dealer wins."
ruleLm+= " a player can draw additional cards until they choose to stop or their total points exceed 21."
ruleLm+= " if the dealer is busted (total point exceed 21), all other player that is not busted earn their bet, all other player that is busted but unchecked does not lose their bet."
#lm+= " special hands are: double Ace earn double bet, 5 cards without busted earn double bet, ace and a ten or face card earn their bet"

playerLm = ruleLm + "I'm a player, i should think hard about my hands and whether i should hit or stand to earn my bet, my hand is "
dealerLm = ruleLm + "I'm the dealer, the rule said that i can check if a player hand's score is larger than me or not, my hand is "
dealerLmCheckQuestion = "Should i check if a player hand's score is larger than me? i should "

@guidance(stateless=True)
def card_value(self,lm,card):
    cardValueResult = lm
    with block(name="card_value"):
        cardValueResult+= parse_card(card) + "'s score is " + gen(name="value",max_tokens=2,regex='\d+')
    return cardValueResult

@guidance(stateless=True)
def player_hit(self,lm):
    resultLm= lm
    with block(name="hit"):
        resultLm+=", that's why i should " + select(name= "select", options= ["hit", "stand"])
    return resultLm

@guidance(stateless=True)
def player_score_evaluation(self,lm,score):
    resultLm = lm 
    with block(name="score_evaluation"):
        resultLm+= "my hand's score is " + score + ", which is " + select(options=["larger than","smaller than","equal to"]) + " 16"
        resultLm+=", so my hand is " + select(name="isLegal", options=["not legal","legal"])
        resultLm+= ". my hand's score is " + score + ", which is " + select(options=["larger than","smaller than","equal to"]) + " 21"
        resultLm+= ", which means that my hand is " + select(name="isBusted", options=["busted","not busted"])
    return resultLm

@guidance(stateless=True)
def player_score_estimation(self,ruleLm, lm, hand, cards):
    scoreLm = lm + cards + ", my hands has " + str(len(hand)) + " cards,"
    with block(name="score_estimation"):
        scoreLm+="my hand's card's score are: "
        for i, card in enumerate(hand):
            ev = card_value(ruleLm,card)
            if i < len(hand) - 1:
                scoreLm += ev["value"] + " + "
            else:
                scoreLm += ev["value"]
            print(ev["card_value"])
        scoreLm+=" = " + gen(name="score",max_tokens=2,regex='\d+') #+ ", which compare to 16 (the legal score) is " + select(options=["lesser","more","equal"])
    return scoreLm

@guidance(stateless=True)
def player_reasoning(self, ruleLm, lm, score):
    reasonLm=lm
    with block(name="reasoning"):
        reasonLm+= "my hand's score is " + score
        ev = player_score_evaluation(ruleLm,score)
        print("score evaluation: ",ev["score_evaluation"])
        if(ev["isLegal"] == "not legal"):
            reasonLm+= " which is "+ ev["isLegal"]
        else:
            reasonLm+= " which is "+ ev["isBusted"]
        reasonLm+= ", so i am thinking that" + gen(name="reason",max_tokens=50)
    return reasonLm

@guidance(stateless=True)
def dealer_hit_before_all(self,lm):
    return lm + ", should i hit before checking other player? i should " + select(name= "select", options= ["hit", "stand"])

playerCount = 4
deck = Deck(1)
players = [Player(100) for _ in range(playerCount)]
checkedPlayers = [False for _ in range(playerCount-1)]

for i in range(playerCount*2):
    players[i % 4].receive_card(deck.draw(1)[0])

# for i in range(playerCount-1):
#     while True:
#         print(parse_hand(players[i].hand))
#         hand = pretty_print_hand(players[i].hand)
#         score_estimation = player_score_estimation(playerLm, players[i].hand, hand)
#         print("score estimation:", score_estimation["score_estimation"])
#         reasoning_result = player_reasoning(score_estimation, score_estimation["score"])
#         print("thinking:", reasoning_result["reasoning"])
#         selection_result = player_hit(reasoning_result)
#         print("player",str(i),selection_result["select"])
#         if selection_result["select"] == "stand":
#             break
#         players[i].receive_card(deck.draw(1)[0])
    
j=1
while True:
    print(parse_hand(players[j].hand))
    hand = pretty_print_hand(players[j].hand)

    score_estimation = player_score_estimation(ruleLm, playerLm, players[j].hand, hand)
    print("score estimation:", score_estimation["score_estimation"])

    reasoning_result = player_reasoning(score_estimation, ruleLm, score_estimation["score"])
    print("thinking:", reasoning_result["reasoning"])

    selection_result = player_hit(reasoning_result)
    print("player",str(j),selection_result["select"])

    if selection_result["select"] == "stand":
        break
    players[j].receive_card(deck.draw(1)[0])
    

# testLm = ruleLm
# with block(name="eval"):
#     testLm+= "my hand's score is 22 " + select(options=["larger than","smaller than","equal to"]) + " 21"
#     testLm+= ", which means that my hand is " + select(name="isBusted", options=["busted","not busted"])
# print(testLm["eval"])
