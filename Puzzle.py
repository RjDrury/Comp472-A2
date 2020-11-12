import numpy as np
from constants import *

class Puzzle:
    def __init__(self, puzzle_elements, length_x=4, length_y=2):
        arr = np.array(puzzle_elements)
        self.state = np.reshape(arr, (length_y, length_x))
        self.goal_state = []

    def is_equal(self,test_state):
        '''
        Accepts a 2d numpy array to compare the with the current state of the puzzle
        '''
        if (self.state == test_state).all():
            return True
        return False
    def set_goal_state(self,state, length_x=4, length_y=2):
        '''
        Takes a goal state and assigns it to this object
        '''
        if isinstance(state, list):
            self.goal_state = state
        else:
            self.goal_state = state
    def current_state_is_goal_state(self):
        '''
        compare if goal state is the current state
        '''
        if isinstance(self.goal_state, list):
            for goal in self.goal_state:
                if (self.state == goal).all():
                    return True
        if (self.state == self.goal_state).all():
            return True
        return False

    def display_state(self):
        print(self.state)

    def is_empty_in_corner(self):
        '''
        return true if 0 is in one of the four corners
        '''
        y_length, x_length = self.state.shape
        y_coordinate, x_coordinate = np.where(self.state == 0)

        is_in_top_left = y_coordinate[0] == 0 and x_coordinate[0] == 0
        is_in_top_right = y_coordinate[0] == 0 and x_coordinate[0] == x_length - 1
        is_in_bottom_left = y_coordinate[0] == y_length - 1 and x_coordinate[0] == 0
        is_in_bottom_right = y_coordinate[0] == y_length - 1 and x_coordinate[0] == x_length - 1

        if is_in_top_left or is_in_top_right or is_in_bottom_left or is_in_bottom_right:
            return True
        return False
    def get_list_of_moves(self):
        '''
        return list of possible moves
        '''
        list_of_moves = []
        zero_is_in_corner = self.is_empty_in_corner()
        y_coordinate, x_coordinate = np.where(self.state == 0)
        y_coordinate = y_coordinate[0]
        x_coordinate = x_coordinate[0]

        y_length, x_length = self.state.shape

        for y_move , x_move in always_available_moves:
            if y_move != 0:
                #checks if you go out of bounds of y axis
                if y_move + y_coordinate >= y_length or y_move + y_coordinate < 0:
                    continue
            if x_move != 0:
                #checks if you go out of bounds of x axis
                if (x_move + x_coordinate >= x_length or x_move + x_coordinate < 0):
                    #wraps around x axis
                    if zero_is_in_corner:
                        list_of_moves.append([y_move,x_move])
                    continue
                        
            list_of_moves.append([y_move,x_move])

        if zero_is_in_corner:
                is_in_top_left = y_coordinate == 0 and x_coordinate == 0
                is_in_top_right = y_coordinate == 0 and x_coordinate == x_length - 1
                is_in_bottom_left = y_coordinate == y_length - 1 and x_coordinate == 0
                is_in_bottom_right = y_coordinate== y_length - 1 and x_coordinate == x_length - 1
                
                if is_in_top_left:
                    list_of_moves.append([1,1])
                    list_of_moves.append([-1,-1])
                if is_in_bottom_left:
                    list_of_moves.append([-1,1])
                    list_of_moves.append([1,-1])
                if is_in_top_right:
                    list_of_moves.append([1,-1])
                    list_of_moves.append([-1,1])
                if is_in_bottom_right:
                    list_of_moves.append([-1,-1])
                    list_of_moves.append([1,1])
                    
        return list_of_moves

    def get_dict_of_moves_with_cost(self):
        '''
        return dict of costs with possible moves
        ex, 1: [[1,0],[0,1]] 2:[-1,0]
        '''
        dict_of_costs_with_moves = {}
        zero_is_in_corner = self.is_empty_in_corner()
        y_coordinate, x_coordinate = np.where(self.state == 0)
        y_coordinate = y_coordinate[0]
        x_coordinate = x_coordinate[0]

        y_length, x_length = self.state.shape

        for y_move , x_move in always_available_moves:
            if y_move != 0:
                #checks if you go out of bounds of y axis
                if y_move + y_coordinate >= y_length or y_move + y_coordinate < 0:
                    continue
            if x_move != 0:
                #checks if you go out of bounds of x axis
                if (x_move + x_coordinate >= x_length or x_move + x_coordinate < 0):
                    #wraps around x axis
                    if zero_is_in_corner:
                        if 2 in dict_of_costs_with_moves:
                            dict_of_costs_with_moves[2].append([y_move,x_move])
                        else:
                            dict_of_costs_with_moves[2] = [[y_move,x_move]]
                    continue
                        
                    
            if 1 in dict_of_costs_with_moves:
                dict_of_costs_with_moves[1].append([y_move,x_move])
            else:
                dict_of_costs_with_moves[1] = [[y_move,x_move]]

        if zero_is_in_corner:
                is_in_top_left = y_coordinate == 0 and x_coordinate == 0
                is_in_top_right = y_coordinate == 0 and x_coordinate == x_length - 1
                is_in_bottom_left = y_coordinate == y_length - 1 and x_coordinate == 0
                is_in_bottom_right = y_coordinate== y_length - 1 and x_coordinate == x_length - 1
                
                if is_in_top_left:
                    dict_of_costs_with_moves[3] = [[1,1],[-1,-1]]
                if is_in_bottom_left:
                    dict_of_costs_with_moves[3] = [[-1,1],[1,-1]]
                if is_in_top_right:
                    dict_of_costs_with_moves[3] = [[1,-1],[-1,1]]
                if is_in_bottom_right:
                    dict_of_costs_with_moves[3] = [[-1,-1],[1,1]]
                    
        return dict_of_costs_with_moves


    def get_dict_of_possible_states_with_cost(self):
        '''
        return a dict of cost: states
        '''
        dict_of_moves = self.get_dict_of_moves_with_cost()
        dict_of_states = {}
        if 1 in dict_of_moves:
            for y,x in dict_of_moves[1]:
                if 1 in dict_of_states:
                    dict_of_states[1].append(self.test_move(y,x))
                else:
                    dict_of_states[1] = [self.test_move(y,x)]
        if 2 in dict_of_moves:
            for y,x in dict_of_moves[2]:
                if 2 in dict_of_states:
                    dict_of_states[2].append(self.test_move(y,x))
                else:
                    dict_of_states[2] = [self.test_move(y,x)]
        if 3 in dict_of_moves:
            for y,x in dict_of_moves[3]:
                if 3 in dict_of_states:
                    dict_of_states[3].append(self.test_move(y,x))
                else:
                    dict_of_states[3] = [self.test_move(y,x)]
        return dict_of_states

    def get_list_of_possible_states(self):
        '''
        return list on np arrays with the associated states
        '''
        list_of_moves = self.get_list_of_moves()
        list_of_states = []

        for y,x in list_of_moves:
            list_of_states.append(self.test_move(y,x))
        return list_of_states

    def perform_move(self, y_move,x_move):
        '''
        input y,x
        Assuming its a valid move, this method could be used to cheat the board
        '''
        y_length, x_length = self.state.shape
        y_coordinate, x_coordinate = np.where(self.state == 0)
        y_coordinate_of_zero = y_coordinate[0]
        x_coordinate_of_zero = x_coordinate[0]

        y_coordinate_of_swap_location = (y_coordinate_of_zero + y_move)%y_length
        x_coordinate_of_swap_location = (x_coordinate_of_zero + x_move)%x_length

        swap_value = self.state[y_coordinate_of_swap_location][x_coordinate_of_swap_location]
        self.state[y_coordinate_of_swap_location][x_coordinate_of_swap_location] = 0
        self.state[y_coordinate_of_zero, x_coordinate_of_zero] = swap_value
        
    def test_move(self,y_move,x_move):

        '''
        input is y,x
        Return the state the board would be in after the entered move
        '''
        test_state = np.copy(self.state)
        y_length, x_length = test_state.shape
        y_coordinate, x_coordinate = np.where(test_state == 0)
        y_coordinate_of_zero = y_coordinate[0]
        x_coordinate_of_zero = x_coordinate[0]

        y_coordinate_of_swap_location = (y_coordinate_of_zero + y_move)%y_length
        x_coordinate_of_swap_location = (x_coordinate_of_zero + x_move)%x_length

        swap_value = test_state[y_coordinate_of_swap_location][x_coordinate_of_swap_location]
        test_state[y_coordinate_of_swap_location][x_coordinate_of_swap_location] = 0
        test_state[y_coordinate_of_zero, x_coordinate_of_zero] = swap_value

        return test_state
    def get_state_as_array(self):
        arr = []
        arr.extend(self.state[0])
        arr.extend(self.state[1])
        return arr