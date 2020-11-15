import numpy as np
from heuristics import *
from Puzzle import *
from helper import *
import time

test_puzzle = [1,0,3,4,
               2,5,6,7]

class Node:
    def __init__(self, parent, state, heuristic):
        self.state = state
        self.parent = parent
        self.heuristic = heuristic

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


    # start
    start_node = Node(None, puzzle.state, 0)
    open = [start_node]
    close = []
    history = []
    cost = 0

    while not puzzle.current_state_is_goal_state() or time.time() - start_time == 60:

        children = puzzle.get_list_of_possible_states()
        for node in children:
            new_node = Node(puzzle.state, node, h(node, puzzle.goal_state))
            if (not present_in_array(open, new_node)) and (not present_in_array(close, new_node)):
                open.append(new_node)

        open = sorted(open, key=lambda node: node.heuristic)
        open,node_popped = pop_element_from_array(open, puzzle.state)
        puzzle.state = open[0].state
        close.append(node_popped)


    print('FOUND IT')
    print('close: ')
    for ele in close:
        print(ele.state.flatten().tolist())
        print(ele.heuristic)

    return close, history, cost


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
    puzzle = Puzzle(puzzle_array)

    for i in range(0, 3):
        start_time = time.time()
        search_file = open("output/" + str(puzzle_index) + "_gbfs-h" + str(i) + "_search.txt", "w")
        solution_file = open("output/" + str(puzzle_index) + "_gbfs-h" + str(i) + "_solution.txt", "w")

        solution, history, cost = gbfs(puzzle, i, start_time)
        # print(solution)
        # print(history)
        # print(cost)

        # hitory = {past_moves[], past_move_costs[], past_states[], past_states[], get_state_as_array()}
        # time_to_complete = str(time.time() - start_time)
        # write_solution_file(puzzle, history, solution_file, str(cost), time_to_complete)


solve_gbfs(test_puzzle, 1)