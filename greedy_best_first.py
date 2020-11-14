import numpy as np
from heuristics import *
from Puzzle import *
import time

def solve_gbfs(puzzle_array, puzzle_index):
    start_time = time.time()
    puzzle = Puzzle(puzzle_array)
    open = []
    closed = []

    search_file = open("output/" + str(puzzle_index) + "_gbfs-h1_search.txt", "w")
    solution_file = open("output/" + str(puzzle_index) + "_gbfs-h1_solution.txt", "w")
