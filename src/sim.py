import numpy as np
import random
from pokerface import *

data = [[0 for i in range(13)] for j in range(13)]

f = open("chart.txt", "r").readlines()
d = [i.replace("\n", "") for i in f]
for line in d:
    # if "rrb" not in line:
    #     continue
    one, two, suited = line[0], line[2], line[1] == line[3]
    prop = float(line.split("'")[3])
    m = {"A": 0, "K": 1, "Q":2, "J":3, "T":4,"9":5, "8": 6, "7": 7, "6":8, "5":9, "4":10,"3":11, "2": 12}
    if m[two] < m[one]:
        one, two = two, one

    if suited:
        data[m[one]][m[two]] = prop
    else:
        data[m[two]][m[one]] = prop

def card_str(card):
    s = "23456789TJKQA"
    suit = "hscd"
    cards = [i + j for i in s for j in suit]
    return cards[int(card / 52)] + cards[int(card % 52)]

def run_game():
    primary_game = NoLimitTexasHoldEm(Stakes(0, (0.5, 1)), (20, 20))
    sb, bb = primary_game.players
    primary_game.nature.deal_hole()
    primary_game.nature.deal_hole()

    card_play = str(sb.hole[0].show()) + str(sb.hole[1].show())
    card_opp = str(bb.hole[0].show()) + str(bb.hole[1].show())

    bb.bet_raise(2)
    sb.check_call()
    primary_game.nature.deal_board()
    sb.check_call()
    bb.check_call()
    primary_game.nature.deal_board()
    sb.check_call()
    bb.check_call()
    primary_game.nature.deal_board()
    sb.check_call()
    bb.check_call()

    sb.showdown()
    bb.showdown()

    evaluator = StandardEvaluator()
    board = "".join([str(i) for i in list(primary_game.board)])
    # print(board)
    x = evaluator.evaluate_hand(parse_cards(card_play), parse_cards(board))
    y = evaluator.evaluate_hand(parse_cards(card_opp), parse_cards(board))
    if x > y:
        return 100, card_play, card_opp
    elif x == y:
        return 0, card_play, card_opp
    else:
        return -100, card_play, card_opp

random_data = [[random.random() for i in range(13)] for j in range(13)]

for line in data:
    print(line)

print("random")

for line in random_data:
    print(line)


total_wl = 0

with open("results100bbshoveuniform.csv", "w") as f:
    for hand_count in range(5000):
        score, card_one, card_two = run_game()
        # print(cards)

        one, two, suited = card_one[0], card_one[2], card_one[1] == card_one[3]

        m = {"A": 0, "K": 1, "Q":2, "J":3, "T":4,"9":5, "8": 6, "7": 7, "6":8, "5":9, "4":10,"3":11, "2": 12}
        if m[two] < m[one]:
            one, two = two, one

        if suited:
            prop = data[m[one]][m[two]]
            r_prop = random_data[m[one]][m[two]]
        else:
            prop = data[m[two]][m[one]]
            r_prop = random_data[m[two]][m[one]]

        outcome = 0
        if random.random() < prop:
            # We are playing the hand
            if random.random() < 0.5:
                # Both players are in 
                outcome = score
            else:
                outcome = 3
        else:
            outcome = -1

        total_wl += outcome
        # print(card_one, "vs", card_two, "outcome", outcome)
        print("Total Won After", hand_count + 1, " is" , total_wl)
        f.write(str(hand_count + 1) + "," + str(total_wl) + "\n")
