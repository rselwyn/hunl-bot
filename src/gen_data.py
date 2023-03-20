from pokerface import *

def card_str(card):
    s = "23456789TJKQA"
    suit = "hscd"
    cards = [i + j for i in s for j in suit]
    return cards[int(card / 52)] + cards[int(card % 52)]

def run_game(card_play, card_opp):
    primary_game = NoLimitTexasHoldEm(Stakes(0, (0.5, 1)), (20, 20))
    sb, bb = primary_game.players
    primary_game.nature.deal_hole(parse_cards(card_play))
    primary_game.nature.deal_hole(parse_cards(card_opp))

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
        return 10
    elif x == y:
        return 0
    else:
        return -10

with open("data.csv", "w") as f:
    for iters in range(10):
        print(iters)
        for i in range(52 * 52):
            for j in range(52 * 52):
                if i != j:
                    a,b = card_str(i)[0:2], card_str(i)[2:]
                    c,d = card_str(j)[0:2], card_str(j)[2:]
                    if a == c or a == d or b == c or b == d or a == b or c == d:
                        continue
                    f.write(str(i) + "," + str(j) + "," + str(run_game(card_str(i), card_str(j))) + "\n")

