import os
def has_state_been_visited(test_state, visited_states):
    for state in visited_states:
        if (state == test_state).all():
            return True
    return False


def getArrayInString(array):
    finalString = ""
    if isinstance(array, int):
        return "0"
    if not isinstance(array, list):
        array = array.flatten().tolist()
    for i in range(len(array)):
        finalString += str(array[i]) + " "

    return finalString


def get_index_of_zero(array):
    array_as_list = array.flatten().tolist()
    for index, ele in enumerate(array_as_list):
        if ele == 0:
            return index

