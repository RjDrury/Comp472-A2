import numpy as np
from heuristics import *
from Puzzle import *
import heapq
import time
''' node class stores a state with a reference to it's parent and the cost to the initial state'''
class Node:
    def __init__(self, parent_index, state, cost_to_initial):
        self.state = state
        self.parent_index = parent_index
        self.cost_to_initial = cost_to_initial

    def print_node(self):
        print(str(self.state)+"\nparent index: "+str(self.parent_index)+"\ncost from start: "+str(self.cost_to_initial))

# test puzzle
test_puzzle = Puzzle([1,0,3,4,2,5,6,7])

'''computes heuristic'''
def h(puzzle_state, goal_state, heuristic):
    if heuristic == 0:
        return h0_naive(puzzle_state)
    if heuristic == 1:
        return h1_hamming(puzzle_state, goal_state)
    if heuristic == 2:
        puzzle_array = np.ravel(puzzle_state).tolist()
        return h2_manhathan(puzzle_array)

"converts numerical heuristic to text"
def h_to_text(h):
    if h == 0:
        return "h0"
    if h == 1:
        return "h1"
    if h == 2:
        return "h2"


''' estimated cost to goal '''
def f(node, goal_state, heuristic):
    return node.cost_to_initial + h(node.state, goal_state, heuristic)

''' determines if goal state 1 or 2 has a better f value and returns the better one'''
def get_best_f(node, heuristic):
    if f(node, goal_state1, heuristic) > f(node, goal_state2, heuristic):
        return f(node, goal_state2, heuristic)
    else:
        return f(node, goal_state1, heuristic)


def a_star(puzzle, heuristic_no):
    # initialize
    start_time = time.time()
    open_list = []
    closed_list = []
    entry = 0 # serves as a tie break for items with the same priority so they are popped in FIFO order
    start_node = Node(None, puzzle.state, 0)
    heapq.heappush(open_list, (get_best_f(start_node, heuristic_no), entry, start_node))
    current = heapq.heappop(open_list)[2] # set current node to the initial state to start the search
    puzzle_goal1 = puzzle_goal2 = Puzzle(current.state)
    puzzle_goal1.set_goal_state(goal_state1)
    puzzle_goal2.set_goal_state(goal_state2)

    while not (np.array_equal(puzzle_goal1.state, goal_state1) or np.array_equal(puzzle_goal2.state, goal_state2)) or time.time() - start_time == 60:
        #get moves from current node
        moves = puzzle_goal1.get_dict_of_possible_states_with_cost()
        # add moves to open
        for key in moves:
            for new_state in moves[key]:
                new = Node(len(closed_list), new_state, current.cost_to_initial + key)
                new_f = get_best_f(new, heuristic_no)

                #check if state is already in array
                if not len(open_list) == 0:
                    for i in range(0, len(open_list)):
                        if (new.state == open_list[i][2].state).all() and open_list[i][0] < new_f:
                            open_list[i] = (new_f, entry, new)
                            entry +=1
                            heapq.heapify(open_list)
                            break

                    heapq.heappush(open_list, (new_f, entry, new))
                    entry += 1

                else:
                    heapq.heappush(open_list, (new_f, entry, new))
                    entry+=1

        # close current state
        closed_list.append(current)

        # get next state
        current = heapq.heappop(open_list)[2]
        # update puzzle
        puzzle_goal1 = puzzle_goal2 = Puzzle(current.state)
        puzzle_goal1.set_goal_state(goal_state1)
        puzzle_goal2.set_goal_state(goal_state2)

    # trace path
    done = False
    solution_path = [current.state]
    #print(current.state)
    if not np.array_equal(current.state, start_node.state):
        #print("    ^\n    |")
        while not done is True:
            prev = closed_list[current.parent_index]
            solution_path.append(prev.state)
            #print(prev.state)
            if np.array_equal(prev.state, start_node.state):
                done = True
            else:
                #print("    ^\n    |")
                current = prev
    # returns solution path and visited states arrays
    return solution_path.reverse(), closed_list

def solve_astar(puzzle_index, puzzle_array):
    puzzle= Puzzle(puzzle_array)
    start_time = time.time()
    for i in range(1, 3):
        solution, visited = a_star(puzzle, i)
        search_file = open(str(puzzle_index) + "_astar-" + h_to_text(i) + "_search.txt", "w")

a_star(test_puzzle, 1)