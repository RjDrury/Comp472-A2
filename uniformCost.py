from Puzzle import Puzzle
import numpy as np
from constants import *
from helper import *
import time
def uniform_cost(puzzle_array,puzzle_index):
    start_time = time.time()
    puzzle = Puzzle(puzzle_array)
    puzzle.set_goal_state([goal_state1,goal_state2])
    potential_states_with_cost = puzzle.get_dict_of_possible_states_with_cost()
    visited_states = []
    lowest_cost_key = 0
    search_file = open(str(puzzle_index)+"_ucs_search.txt", "w")
    while(not puzzle.current_state_is_goal_state()):
        visited_states.append(puzzle.state)

        #This gets the next step to take
        lowest_cost_key = min([*potential_states_with_cost.keys()])
        next_state = potential_states_with_cost[lowest_cost_key].pop()
        if not potential_states_with_cost[lowest_cost_key]:
            del potential_states_with_cost[lowest_cost_key]
        #this guarentees that the next cheapest hasn't been seen before, if it has, it will get the next cheapest one
        while (has_state_been_visited(next_state,visited_states)):
            lowest_cost_key = min([*potential_states_with_cost.keys()])
            next_state = potential_states_with_cost[lowest_cost_key].pop()
            if not potential_states_with_cost[lowest_cost_key]:
                del potential_states_with_cost[lowest_cost_key]

        puzzle.state = next_state

        new_potential_states = puzzle.get_dict_of_possible_states_with_cost()
        #add the states that can be reached by the new states to the potential states dict with the cost of the next move appended with the cost of the previous move
        for key in new_potential_states:
            if key + lowest_cost_key in potential_states_with_cost:
                potential_states_with_cost[key + lowest_cost_key].extend(new_potential_states[key])
            else:
                potential_states_with_cost[key + lowest_cost_key] = new_potential_states[key]
        search_file.write("f(n) = g(n) = " +str(lowest_cost_key) + " State " + str(puzzle.get_state_as_array())+"\n")

    search_file.write("\n")
    search_file.write("Execution time = " + str((time.time() - start_time) *1000)  + " ")
    print("Reached goal state, lowest cost : "+ str(lowest_cost_key))

