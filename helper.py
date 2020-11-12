def has_state_been_visited(test_state, visited_states):
    for state in visited_states:
        if (state == test_state).all():
            return True
    return False
