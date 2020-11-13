from Puzzle import *
from constants import *


# naive heuristic for demo
def h0_naive(puzzle):
    r, c = puzzle.state.shape
    if puzzle.state[r - 1, c - 1] == 0:
        return 0
    else:
        return 1


# hamming loss
def h1_hamming(puzzle_state, goal_state):
    return np.count_nonzero(np.bitwise_xor(puzzle_state, goal_state))


# Manhattan loss
def h2_manhathan(puzzle_array):
    puzzle = Puzzle(puzzle_array)

    if not puzzle.goal_state:
        puzzle.goal_state = goal_state1

    config = puzzle.state
    goal_arr = puzzle.goal_state
    state = config.flatten().tolist()
    goal = goal_arr.flatten().tolist()

    total = sum(abs(a % 4 - b % 4) + abs(a // 4 - b // 4)
                for a, b in ((state.index(i), goal.index(i)) for i in range(0, 8)))

    return total
