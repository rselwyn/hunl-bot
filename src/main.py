from pokerface import *
from solve import Solver, SolverSolution

PARAMS = {
	STACK_DEPTH: 100,
}

def main()
	primary_game = NoLimitTexasHoldEm(Stakes(0, (0.5, 1)), (PARAMS.STACK_DEPTH, PARAMS.STACK_DEPTH))
	sb, bb = primary_game.players
	primary_game.nature.deal_hole()
	primary_game.nature.deal_hole()

	solver = Solver(primary_game, sb, bb):
	solution = solver.solve_spot()

if __name__ == "__main__":
