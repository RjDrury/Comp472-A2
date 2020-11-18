import numpy as np
from heuristics import *
from Puzzle import *
from helper import *
import time

test_puzzle = [1,0,3,4,
               2,5,6,7]

class Node:
    def __init__(self, parent, state, heuristic, cost):
        self.state = state
        self.parent = parent
        self.heuristic = heuristic
        self.cost = cost

    def print_node(self):
        print(str(self.state)+" "+str(self.parent)+" "+str(self.heuristic))


def gbfs(puzzle, heuristicIndex, start_time):
    # define which heuristic to run
    def h(p, g):
        if heuristicIndex == 0:
            return h0_naive(p)

        if heuristicIndex == 1:
            return h1_hamming(p, g)

        if heuristicIndex == 2:
            return h2_manhathan(p, g)

    # set goal state of puzzle (the one with lowest initial h())
    if not heuristicIndex == 0:
        if h(puzzle.state, goal_state1) < h(puzzle.state, goal_state2):
            puzzle.set_goal_state(goal_state1)
        else:
            puzzle.set_goal_state(goal_state2)

    else:
        puzzle.set_goal_state(goal_state1)


    # initial values
    start_node = Node(None, puzzle.state, 0, 0)
    open = [start_node]
    close = []

    # while current state is not the goal and time is not 1 minute
    while not puzzle.current_state_is_goal_state() and time.time() - start_time < 60:
        children = puzzle.get_dict_of_possible_states_with_cost()
        for cost in children:
            for node in children[cost]:
                new_node = Node(puzzle.state, node, h(node, puzzle.goal_state), cost)
                # append the children is not present in any list (not visited & not to be visited)
                if (not present_in_array(open, new_node)) and (not present_in_array(close, new_node)):
                    open.append(new_node)

        # sort open list (next nodes to be visited) -> priority queue
        open = sorted(open, key=lambda node: node.heuristic)
        # pop current state from open list and close the node (set as visited)
        open,node_popped = pop_element_from_array(open, puzzle.state)
        puzzle.state = open[0].state
        close.append(node_popped)


    solution = []
    cost = 0
    # if reach goal append goal to visited and start solution list
    if puzzle.current_state_is_goal_state():
        open, goal_state = pop_element_from_array(open, puzzle.state)
        close.append(goal_state)
        solution.append(goal_state)
    else:
        solution = "no solution"
        return solution, close, cost

    # get solution from closed nodes + total cost os solution
    for ele in solution:
        if get_parent_in_array(close, ele) is None:
            break
        solution.append(get_parent_in_array(close, ele))
        cost += ele.cost
    solution.reverse()

    return solution, close


def get_parent_in_array(array, child):
    for index, ele in enumerate(array):
        if child is not None and (child.parent == array[index].state).all():
            return array[index]
    return None


def present_in_array(array, element):
    for index, ele in enumerate(array):
        if (element.state == array[index].state).all():
            return True
    return False


def pop_element_from_array(initial_array, element):
    node_to_pop = {}
    for index, ele in enumerate(initial_array):
        if (element == initial_array[index].state).all():
            node_to_pop = initial_array.pop(index)

    return initial_array, node_to_pop;


def solve_gbfs(puzzle_array, puzzle_index):
    for i in range(1, 3):
        print('- heuristic:', i)
        puzzle = Puzzle(puzzle_array)
        start_time = time.time()
        search_file = open("output/" + str(puzzle_index) + "_gbfs-h" + str(i) + "_search.txt", "w")
        solution_file = open("output/" + str(puzzle_index) + "_gbfs-h" + str(i) + "_solution.txt", "w")

        solution, history = gbfs(puzzle, i, start_time)
        write_search(search_file, history, i)
        write_solution(solution_file, start_time, solution)



def write_search(search_file, history, i):
    for ele in history:
        if i == 0:
            ele.heuristic = 0
        search_file.write(str(0) + " " + str(0) + " " + str(ele.heuristic) + " " + get_array_in_string(ele.state) + "\n")


def write_solution(solution_file, start_time, solution):
    total_cost = 0
    time_to_complete = str(time.time() - start_time)

    for ele in solution:
        total_cost += ele.cost
        solution_file.write(str(get_index_of_zero(ele.state)) + " " + str(ele.cost) + " " + get_array_in_string(ele.state) + "\n")

    solution_file.write(str(total_cost) + " " + str(time_to_complete))
