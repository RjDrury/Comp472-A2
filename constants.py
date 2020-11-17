import numpy as np

puzzle_directory = "sample_puzzles.txt"
random_puzzle_directory = "random_puzzles.txt"
always_available_moves = [(1,0),(0,1),(-1,0),(0,-1)]
diagonal_moves = [(1,1), (1,-1),(-1,0),(-1,-1)]
goal_state1 = np.array([[1, 2, 3, 4], [5, 6, 7, 0]])
goal_state2 = np.array([[1, 3, 5, 7], [2, 4, 6, 0]])