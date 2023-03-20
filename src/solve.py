import pandas as pd
import json

class NodeStrategy:
	def __init__(self, pot=1):
		self.strategy ={"check": (pot * 0, 1/2), 
						"bet": (pot * 0.5, 1/2)
						# "half": (pot * 0.5, 1/6), 
						# "threeq": (pot * 0.75, 1/6), 
						# "pot": (pot, 1/6), 
						# "double": (2 * pot, 1/6)
						}

	def dump(self):
		return json.dumps({"strategy": self.strategy})

class SolverSolution:
	def __init__(self, filename):
		self.solutions = pd.read_csv(filename)

	def load_hole_cards(self):
		pass

	def load_hand_solution(self, hole_cards, flop):
		pass

	def load_full_solution(self, hole_cards, flop, turn, river):
		pass

	def update_solution(self, flop=None, turn=None, river=None):
		pass

class Solver:
	def __init__(self, game, sb, bb):
		pass

	def solve_spot(self):
		pass