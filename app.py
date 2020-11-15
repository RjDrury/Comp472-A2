from constants import *
from uniformCost import *
from heuristics import *
from greedy_best_first import *

def main():
    puzzle_file = open(puzzle_directory, "r")
    puzzle_data_entries = puzzle_file.readlines()
    puzzle_index = 0
    for puzzle_data in puzzle_data_entries:
        puzzle_array = puzzle_data.split(" ")
        puzzle_array = [int(i) for i in puzzle_array] 

        #call method for search with puzzle array to make your puzzle object within the search
        #ex
        uniform_cost(puzzle_array, puzzle_index)
        puzzle_index += 1
        # solve_gbfs(puzzle_array, puzzle_index)

if __name__ == '__main__':
    main()