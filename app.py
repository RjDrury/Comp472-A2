from constants import *
from uniformCost import *
from heuristics import *
from a_star import *
from greedy_best_first import *

def main():
    puzzle_file = open(puzzle_directory, "r")
    puzzle_data_entries = puzzle_file.readlines()
    puzzle_index = 0
    for puzzle_data in puzzle_data_entries:
        puzzle_array = puzzle_data.split(" ")
        puzzle_array = [int(i) for i in puzzle_array] 

        PUZZLE = puzzle_array
        #print('Uniform Cost for puzzle:', puzzle_index)
        #uniform_cost(PUZZLE, puzzle_index)
        print('A star for puzzle:', puzzle_index)
        solve_astar(puzzle_index, PUZZLE)
        #print('Greedy Best First for puzzle:', puzzle_index)
        #solve_gbfs(PUZZLE, puzzle_index)
        puzzle_index += 1

if __name__ == '__main__':
    main()