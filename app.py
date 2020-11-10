from constants import *
from uniformCost import *
def main():
    puzzle_file = open(puzzle_file, "r")
    puzzle_data_entries = puzzle_file.readlines()

    for puzzle_data in puzzle_data_entries:
        puzzle_array = puzzle_data.split(" ")
        puzzle_array = [int(i) for i in puzzle_array] 

        #call method for search with puzzle array to make your puzzle object within the search
        #ex
        uniformCost(puzzle_array)

        
if __name__ == '__main__':
    main()