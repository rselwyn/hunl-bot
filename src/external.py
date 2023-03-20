import numpy as np
import random
from collections import defaultdict

class Node:
	def __init__(self, bet_options):
		self.num_actions = 2
		self.regret_sum = defaultdict(int)
		self.strategy = defaultdict(int)
		self.strategy_sum = defaultdict(int)
		self.bet_options = [0, 2]

	def get_strategy(self):
		normalizing_sum = 0
		for a in self.bet_options:
			if self.regret_sum[a] > 0:
				self.strategy[a] = self.regret_sum[a]
			else:
				self.strategy[a] = 0
			normalizing_sum += self.strategy[a]

		for a in self.bet_options:
			if normalizing_sum > 0:
				self.strategy[a] /= normalizing_sum
			else:
				self.strategy[a] = 1.0/self.num_actions

		return self.strategy

	def get_average_strategy(self):
		avg_strategy = defaultdict(int)
		normalizing_sum = 0
		
		for a in self.bet_options:
			normalizing_sum += self.strategy_sum[a]
		for a in self.bet_options:
			if normalizing_sum > 0:
				avg_strategy[a] = self.strategy_sum[a] / normalizing_sum
			else:
				avg_strategy[a] = 1.0 / self.num_actions
		
		return avg_strategy

class LeducCFR:
	def __init__(self, iterations, decksize, starting_stack):
		#self.nbets = 2
		self.iterations = iterations
		self.decksize = decksize
		self.nodes = {}

	def cfr_iterations_external(self):
		util = np.zeros(2)
		for t in range(1, self.iterations + 1): 
			for i in range(2):
					random.shuffle(self.cards)
					util[i] += self.external_cfr(self.cards[:3], [[], []], 0, 2, 0, i, t)
		print('Average game value: {}'.format(util[0]/(self.iterations)))
		
		with open('leducnlstrat.txt', 'w+') as f:
			for i in sorted(self.nodes):
				f.write('{}, {}\n'.format(i, self.nodes[i].get_average_strategy()))
				print(i, self.nodes[i].get_average_strategy())

	def valid_bets(self, history, rd, acting_player):
		return [0, 5]
		

	def external_cfr(self, cards, history, rd, pot, nodes_touched, traversing_player, t):
		if t % 1000 == 0 and t>0:
			print('THIS IS ITERATION', t)
		plays = len(history[rd])
		acting_player = plays % 2
		# print('*************')
		# print('HISTORY RD', history[rd])
		# print('PLAYS', plays)

		if plays >= 2:
			p0total = np.sum(history[rd][0::2])
			p1total = np.sum(history[rd][1::2])
			# print('P0 TOTAL', p0total)
			# print('P1 TOTAL', p1total)
			# print('ROUND BEG', rd)
				
			if p0total == p1total:
				if rd == 0 and p0total != 19:
					rd = 1
					# print('ROUND TO 1')
				else:
					# print('SHOWDOWN RETURN')
					winner = self.winning_hand(cards)
					if winner == -1:
						return 0
					elif traversing_player == winner:
						return pot/2
					elif traversing_player != winner:
						return -pot/2

			elif history[rd][-1] == 0: #previous player folded
				# print('FOLD RETURN')
				if acting_player == 0 and acting_player == traversing_player:
					return p1total+1
				elif acting_player == 0 and acting_player != traversing_player:
					return -(p1total +1)
				elif acting_player == 1 and acting_player == traversing_player:
					return p0total+1
				elif acting_player == 1 and acting_player != traversing_player:
					return -(p0total +1)
		# print('ROUND AFTER', rd)
		if rd == 0:
			infoset = str(cards[acting_player]) + str(history)
		elif rd == 1:
			infoset = str(cards[acting_player]) + str(cards[2]) + str(history)

		if acting_player == 0:
			infoset_bets = self.valid_bets(history, rd, 0)
		elif acting_player == 1:
			infoset_bets = self.valid_bets(history, rd, 1)
		# print('ROUND', rd)
		# print('INFOSET BETS', infoset_bets)
		if infoset not in self.nodes:
			self.nodes[infoset] = Node(infoset_bets)

		# print(self.nodes[infoset])
		# print(infoset)

		nodes_touched += 1

		if acting_player == traversing_player:
			util = defaultdict(int)
			node_util = 0
			strategy = self.nodes[infoset].get_strategy()
			for a in infoset_bets:
				if rd == 0:
					next_history = [history[0] + [a], history[1]]
				elif rd == 1:
					next_history = [history[0], history[1] + [a]]
				pot += a
				util[a] = self.external_cfr(cards, next_history, rd, pot, nodes_touched, traversing_player, t)
				node_util += strategy[a] * util[a]

			for a in infoset_bets:
				regret = util[a] - node_util
				self.nodes[infoset].regret_sum[a] += regret
			return node_util

		else: #acting_player != traversing_player
			strategy = self.nodes[infoset].get_strategy()
			# print('STRATEGY', strategy)
			dart = random.random()
			# print('DART', dart)
			strat_sum = 0
			for a in strategy:
				strat_sum += strategy[a]
				if dart < strat_sum:
					action = a
					break
			# print('ACTION', action)
			if rd == 0:
				next_history = [history[0] + [action], history[1]]
			elif rd == 1:
				next_history = [history[0], history[1] + [action]]
			pot += action
			# if acting_player == 0:
			# 	p0stack -= action
			# elif acting_player == 1:
			# 	p1stack -= action
			# print('NEXT HISTORY2', next_history)
			util = self.external_cfr(cards, next_history, rd, pot, nodes_touched, traversing_player, t)
			for a in infoset_bets:
				self.nodes[infoset].strategy_sum[a] += strategy[a]
			return util

if __name__ == "__main__":
	k = LeducCFR(1000, 3, 20)
	k.cfr_iterations_external()
	# for i in range(20):
	# 	print(k.valid_bets([[i],[]], 0, 19))
	#a = k.valid_bets([[4, 18],[]], 0, 15)
	#print(a)