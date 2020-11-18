from Puzzle import Puzzle
from constants import *
from helper import *
import time


def uniform_cost(puzzle_array,puzzle_index):
    start_time = time.time()
    puzzle = Puzzle(puzzle_array)
    puzzle.set_goal_state([goal_state1,goal_state2])
    potential_states_with_cost = puzzle.get_dict_of_possible_states_with_cost()
    potential_states_with_history = covert_state_dict_to_dict_board_history(potential_states_with_cost, puzzle.state)

    visited_states = []
    lowest_cost_key = 0
    next_state = Board_State_History(0,[0],[0],[0])
    search_file = open("output/"+str(puzzle_index)+"_ucs_search.txt", "w")
    solution_file = open("output/"+str(puzzle_index)+"_ucs_solution.txt", "w")
    iteration = 0

    while not puzzle.current_state_is_goal_state() and time.time() - start_time < 60:
        visited_states.append(puzzle.state)
        iteration += 1

        # This gets the next step to take
        lowest_cost_key = min([*potential_states_with_history.keys()])
        next_state = potential_states_with_history[lowest_cost_key].pop()
        if not potential_states_with_history[lowest_cost_key]:
            del potential_states_with_history[lowest_cost_key]

        # this guarentees that the next cheapest hasn't been seen before, if it has, it will get the next cheapest one
        while (has_state_been_visited(next_state.state,visited_states)):
            lowest_cost_key = min([*potential_states_with_history.keys()])
            next_state = potential_states_with_history[lowest_cost_key].pop()
            if not potential_states_with_history[lowest_cost_key]:
                del potential_states_with_history[lowest_cost_key]

        puzzle.state = next_state.state

        new_potential_states = puzzle.get_dict_of_possible_states_with_cost()
        new_potentials_with_history = covert_old_state_to_map_new_dict(next_state, new_potential_states)

        # add the states that can be reached by the new states to the potential states dict with the cost of the next move appended with the cost of the previous move
        for key in new_potentials_with_history:
            if key + lowest_cost_key in potential_states_with_history:
                potential_states_with_history[key + lowest_cost_key].extend(new_potentials_with_history[key])
            else:
                potential_states_with_history[key + lowest_cost_key] = new_potentials_with_history[key]
        search_file.write(str(0) + " " + str(lowest_cost_key) + " " + str(0) + " " + get_array_in_string(puzzle.get_state_as_array()) + "\n")

    search_file.write("\n")
    time_to_complete = str(time.time() - start_time)

    if not puzzle.current_state_is_goal_state():
        solution_file.write("no solution")
        search_file.close()
        repopen_search_file = open("output/"+str(puzzle_index)+"_ucs_search.txt", "w")
        repopen_search_file.write("no solution")

    else:
        print("Reached goal state, lowest cost : " + str(lowest_cost_key))
        write_solution_file(puzzle, next_state, solution_file, str(lowest_cost_key) , time_to_complete)


class Board_State_History:
    def __init__(self, puzzle_elements, parent_states, parent_moves, parent_costs):
        self.state = puzzle_elements
        self.past_states = parent_states
        self.past_moves = parent_moves
        self.past_move_costs = parent_costs

    def get_state_as_array(self,nparr):
        if isinstance(nparr,int ):
            return 0
        arr = []
        arr.extend(nparr[0])
        arr.extend(nparr[1])
        return arr


def covert_state_dict_to_dict_board_history(states_with_cost, parent_state):
    new_dict = {}
    for key in states_with_cost:
        for state in states_with_cost[key]:
            change_zero_with = move_zero_with(parent_state, state)
            if key in new_dict:
                new_dict[key].append(Board_State_History(state,[parent_state],[change_zero_with], [key]))
            else:
                new_dict[key] = [Board_State_History(state,[parent_state],[change_zero_with], [key])]
    return new_dict


def move_zero_with(old_state, new_state):
    y_coordinate, x_coordinate = np.where(new_state == 0)
    return old_state[y_coordinate[0]][x_coordinate[0]]


def covert_old_state_to_map_new_dict(old_state, children):
    new_dict = {}

    for key in children:
        for state in children[key]:
            old_states = old_state.past_states.copy()
            old_moves = old_state.past_moves.copy()
            old_costs = old_state.past_move_costs.copy()
            change_zero_with = move_zero_with(old_state.state, state)
            old_states.append(old_state.state)
            old_moves.append(change_zero_with)
            old_costs.append(key)
            if key in new_dict:
                new_dict[key].append(Board_State_History(state,old_states,old_moves,old_costs))
            else:
                new_dict[key] = [Board_State_History(state,old_states,old_moves,old_costs)]
    return new_dict


def write_solution_file(puzzle, board_history, file, cost, time_to_complete):
    file.write("0 0 " + get_array_in_string(puzzle.get_state_as_array()) + "\n")
    for i in range(len(board_history.past_moves)):
        file.write(str(board_history.past_moves[i]) + " " + str(board_history.past_move_costs[i]) + " " + get_array_in_string(board_history.get_state_as_array(board_history.past_states[i])) + "\n")
    file.write(cost + " " + time_to_complete)