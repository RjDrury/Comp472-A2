import numpy as np
from Puzzle import *
from constants import *

''' naive heuristic for demo'''
def h0_naive(puzzle):
    r, c = puzzle.state.shape
    if puzzle.state[r - 1, c - 1] == 0:
        return 0
    else:
        return 1

''' hamming loss'''
def h1_hamming(puzzle):
    if puzzle.goal_state == []:
        puzzle.goal_state = goal_state1
    config = puzzle.state
    goal = puzzle.goal_state
    return np.count_nonzero(np.bitwise_xor(config, goal))
