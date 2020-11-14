def has_state_been_visited(test_state, visited_states):
    for state in visited_states:
        if (state == test_state).all():
            return True
    return False


def write_solution_file(puzzle, board_history, file, cost, time_to_complete):
    file.write("0 0 " + str(puzzle.get_state_as_array())+"\n")
    for i in range(len(board_history.past_moves)):
        file.write(str(board_history.past_moves[i]) + str(board_history.past_move_costs[i]) + str(board_history.get_state_as_array(board_history.past_states[i])) +"\n")
    file.write(cost + time_to_complete)