import numpy as np
from Puzzle import *
from constants import *


# naive heuristic for demo
def h0_naive(puzzle_state):
    r, c = puzzle_state.shape
    if puzzle_state[r - 1, c - 1] == 0:
        return 0
    else:
        return 1


# hamming loss
def h1_hamming(puzzle_state, goal_state):
    return np.count_nonzero(np.bitwise_xor(puzzle_state, goal_state))


# Manhattan loss
def h2_manhathan(puzzle_state, goal_state):
    state = puzzle_state.flatten().tolist()
    goal = goal_state.flatten().tolist()
    return sum(abs(a % 4 - b % 4) + abs(a // 4 - b // 4)
               for a, b in ((state.index(i), goal.index(i)) for i in range(0, 8)))
