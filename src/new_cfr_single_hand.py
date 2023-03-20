import numpy as np
from pokerface import *
import time

# Number of actions a player can take at a decision node.
_N_ACTIONS = 2
_N_CARDS = 52 * 52

_SMALL_STACK = 20
_BB_ANTE = 1

def main():
    """
    Run iterations of counterfactual regret minimization algorithm.
    """
    i_map = {}  # map of information sets
    n_iterations = 40
    expected_game_value = 0

    for a in range(n_iterations):
        # print(i_map)
        print(a)
        expected_game_value += cfr(i_map)
        for _, v in i_map.items():
            v.next_strategy()

    expected_game_value /= n_iterations

    display_results(expected_game_value, i_map)


def cfr(i_map, history="", card_1=-1, card_2=-1, pr_1=1, pr_2=1, pr_c=1):
    """
    Counterfactual regret minimization algorithm.

    Parameters
    ----------

    i_map: dict
        Dictionary of all information sets.
    history : [{'r', 'c', 'b'}], str
        A string representation of the game tree path we have taken.
        Each character of the string represents a single action:

        'r': random chance action
        'c': check action
        'b': bet action
    card_1 : (0, 52*52), int
        player A's card
    card_2 : (0, 52*52), int
        player B's card
    pr_1 : (0, 1.0), float
        The probability that player A reaches `history`.
    pr_2 : (0, 1.0), float
        The probability that player B reaches `history`.
    pr_c: (0, 1.0), float
        The probability contribution of chance events to reach `history`.
    """
    if is_chance_node(history):
        return chance_util(i_map)

    if is_terminal(history):
        return terminal_util(history, card_1, card_2)

    n = len(history)
    is_player_1 = n % 2 == 0
    info_set = get_info_set(i_map, card_1 if is_player_1 else card_2, history)

    strategy = info_set.strategy
    if is_player_1:
        info_set.reach_pr += pr_1
    else:
        info_set.reach_pr += pr_2

    # Counterfactual utility per action.
    action_utils = np.zeros(_N_ACTIONS)

    for i, action in enumerate(["c", "b"]):
        next_history = history + action
        if is_player_1:
            action_utils[i] = -1 * cfr(i_map, next_history,
                                       card_1, card_2,
                                       pr_1 * strategy[i], pr_2, pr_c)
        else:
            action_utils[i] = -1 * cfr(i_map, next_history,
                                       card_1, card_2,
                                       pr_1, pr_2 * strategy[i], pr_c)

    # Utility of information set.
    util = sum(action_utils * strategy)
    regrets = action_utils - util
    if is_player_1:
        info_set.regret_sum += pr_2 * pr_c * regrets
    else:
        info_set.regret_sum += pr_1 * pr_c * regrets

    return util


def is_chance_node(history):
    """
    Determine if we are at a chance node based on tree history.
    """
    return history == ""

def chance_util(i_map):
    expected_value = 0
    n_possibilities = _N_CARDS * _N_ACTIONS
    for i in range(_N_CARDS):
        for j in [2702]:
            if i != j:
                a,b = card_str(i)[0:2], card_str(i)[2:]
                c,d = card_str(j)[0:2], card_str(j)[2:]
                if a == c or a == d or b == c or b == d or a == b or c == d:
                    continue
                expected_value += cfr(i_map, "rr", i, j,
                                      1, 1, 1/n_possibilities)
    return expected_value/n_possibilities

def is_terminal(history):
    """
    Returns true if the history is a terminal history.
    """
    return len(history) == 4

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

def terminal_util(history, card_1, card_2):
    """
    Run the board and determine a winner
    """
    n = len(history)

    card_player = card_1 if n % 2 == 0 else card_2
    card_opponent = card_2 if n % 2 == 0 else card_1

    # print("terminal")
    # print(history)
    # print(card_1, card_2)
    # print(card_str(card_1), card_str(card_2))
    # input()
    if history == "rrbc":
        # Last player folded. The current player wins.
        return 3
    elif history == "rrcc" or history == "rrcb":
        # Showdown with no bets
        return -1
    elif history == "rrbb":
        # We run it
        # print("Running ", card_str(card_player), "against", card_str(card_opponent))
        # a = int(card_player / 52)
        # b = int(card_player % 52)

        # c = int(card_opponent / 52)
        # d = int(card_opponent / 52)

        # if max(a,b) > max(c,d):
        #     return 10
        # else:
        #     return 0

        val = run_game(card_str(card_player), card_str(card_opponent))
        # print(val)
        # input()
        return val


    raise Exception("Shouldn't be here")
    # Showdown with 1 bet
    # return 2 if card_1 > card_2 else -2


def card_str(card):
    s = "23456789TJKQA"
    suit = "hscd"
    cards = [i + j for i in s for j in suit]
    return cards[int(card / 52)] + cards[int(card % 52)]

def get_info_set(i_map, card, history):
    """
    Retrieve information set from dictionary.
    """
    key = card_str(card) + " " + history
    info_set = None

    if key not in i_map:
        info_set = InformationSet(key)
        i_map[key] = info_set
        return info_set

    return i_map[key]


class InformationSet():
    def __init__(self, key):
        self.key = key
        self.regret_sum = np.zeros(_N_ACTIONS)
        self.strategy_sum = np.zeros(_N_ACTIONS)
        self.strategy = np.repeat(1/_N_ACTIONS, _N_ACTIONS)
        self.reach_pr = 0
        self.reach_pr_sum = 0

    def next_strategy(self):
        self.strategy_sum += self.reach_pr * self.strategy
        self.strategy = self.calc_strategy()
        self.reach_pr_sum += self.reach_pr
        self.reach_pr = 0

    def calc_strategy(self):
        """
        Calculate current strategy from the sum of regret.
        """
        strategy = self.make_positive(self.regret_sum)
        total = sum(strategy)
        if total > 0:
            strategy = strategy / total
        else:
            n = _N_ACTIONS
            strategy = np.repeat(1/n, n)

        return strategy


    def get_average_strategy(self):
        """
        Calculate average strategy over all iterations. This is the
        Nash equilibrium strategy.
        """
        strategy = self.strategy_sum / self.reach_pr_sum

        # Purify to remove actions that are likely a mistake
        strategy = np.where(strategy < 0.001, 0, strategy)

        # Re-normalize
        total = sum(strategy)
        strategy /= total

        return strategy

    def make_positive(self, x):
        return np.where(x > 0, x, 0)

    def __str__(self):
        strategies = ['{:03.2f}'.format(x) for x in self.get_average_strategy()]
        return '{} {}'.format(self.key.ljust(6), strategies)


def display_results(ev, i_map):
    print('player 1 expected value: {}'.format(ev))
    print('player 2 expected value: {}'.format(-1 * ev))

    print()
    print('player 1 strategies:')
    sorted_items = sorted(i_map.items(), key=lambda x: x[0])
    for _, v in filter(lambda x: len(x[0]) % 2 == 0, sorted_items):
        print(v)
    print()
    print('player 2 strategies:')
    for _, v in filter(lambda x: len(x[0]) % 2 == 1, sorted_items):
        print(v)


if __name__ == "__main__":
    main()