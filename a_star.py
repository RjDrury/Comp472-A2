from heuristics import *
from Puzzle import *
from helper import *
import heapq
import time

''' node class stores a state with a reference to it's parent and the cost to the initial state'''
class Node:
    def __init__(self, parent_index, state, cost):
        self.f_val = None
        self.state = state
        self.parent_index = parent_index
        self.cost = cost

    def print_node(self):
        print(str(self.state)+"\nparent index: "+str(self.parent_index)+"\ncost from start: "+str(self.cost_to_initial))

'''computes heuristic'''
def h(puzzle_state, goal_state, heuristic):
    if heuristic == 0:
        return h0_naive(puzzle_state)
    if heuristic == 1:
        return h1_hamming(puzzle_state, goal_state)
    if heuristic == 2:
        return h2_manhathan(puzzle_state, goal_state)

"converts numerical heuristic to text"
def h_to_text(h):
    if h == 0:
        return "h0"
    if h == 1:
        return "h1"
    if h == 2:
        return "h2"


''' estimated cost to goal '''
def f(node, goal_state, heuristic, parent, closed):
    g = get_cost(node, parent, closed)
    return g + h(node.state, goal_state, heuristic)

''' determines if goal state 1 or 2 has a better f value and returns the better one'''
def get_best_f(node, heuristic, parent, closed):
    f1 = f(node, goal_state1, heuristic, parent, closed)
    f2 = f(node, goal_state2, heuristic, parent, closed)
    if f1 > f2:
        return f2

    else:
        return f1

''' finds cost to start node '''
def get_cost(node, parent, closed):
    cst = 0

    while not parent is None:
        cst += node.cost
        node = parent
        try:
            parent = closed[parent.parent_index]
        except TypeError:
            parent = None
    return cst


def a_star(puzzle, heuristic_no):
    # initialize
    start_time = time.time()
    open_list = []
    closed_list = []
    entry = 0 # serves as a tie break for items with the same priority so they are popped in FIFO order

    start_node = Node(None, puzzle.state, 0)
    
    f_init= get_best_f(start_node, heuristic_no, None, closed_list)

    start_node.f_val = f_init
    heapq.heappush(open_list, (start_node.f_val, entry, start_node))
    current = heapq.heappop(open_list)[2] # set current node to the initial state to start the search
    puzzle_goal1 = Puzzle(current.state)
    puzzle_goal2 = Puzzle(current.state)
    puzzle_goal1.set_goal_state(goal_state1)
    puzzle_goal2.set_goal_state(goal_state2)

    while not np.array_equal(puzzle_goal1.state, goal_state1) or np.array_equal(puzzle_goal2.state, goal_state2):
        if time.time() - start_time > 60:
            return 0, 0

        # get moves from current node
        moves = puzzle_goal1.get_dict_of_possible_states_with_cost()

        # add moves to open
        for key in moves:
            for new_state in moves[key]:
                already_added = False
                new = Node(len(closed_list), new_state, key)
                new_f = get_best_f(new, heuristic_no, current, closed_list)
                new.f_val = new_f

                if not len(open_list) == 0:
                    # check if state is already in open_list
                    for i in range(0, len(open_list)):
                        if (new.state == open_list[i][2].state).all() and open_list[i][0] > new.f_val:
                            open_list[i] = (new.f_val, entry, new)
                            entry +=1
                            heapq.heapify(open_list)
                            already_added = True
                            break
                        # check for state in closed list
                    if not len(closed_list) == 0:
                        for j in range(0, len(closed_list)):
                            if (new.state == closed_list[j].state).all():
                                if closed_list[j].f_val > new.f_val:
                                    closed_list[j].f_val = new.f_val
                                    closed_list[j].parent_index = current.parent_index
                                    heapq.heappush(open_list, (new.f_val, entry, new))
                                    entry += 1
                                    already_added = True
                                    break
                                if closed_list[j].f_val <= new.f_val:
                                    already_added = True
                                    break
                        if not already_added:
                            heapq.heappush(open_list, (new.f_val, entry, new))
                            entry += 1

                else:
                    heapq.heappush(open_list, (new.f_val, entry, new))
                    entry+=1

        # close current state
        closed_list.append(current)

        # get next state
        current = heapq.heappop(open_list)[2]

        # update puzzle
        puzzle_goal1 = Puzzle(current.state)
        puzzle_goal2 = Puzzle(current.state)
        puzzle_goal1.set_goal_state(goal_state1)
        puzzle_goal2.set_goal_state(goal_state2)

    # append solution state to closed
    closed_list.append(current)

    # trace path
    done = False
    solution_path = [current]
    if not np.array_equal(current.state, start_node.state):
        while not done is True:
            prev = closed_list[current.parent_index]
            solution_path.append(prev)
            if np.array_equal(prev.state, start_node.state):
                done = True
            else:
                current = prev
    return solution_path, closed_list

def solve_astar(puzzle_index, puzzle_array):
    puzzle = Puzzle(puzzle_array)
    for i in range(1, 3):
        print('- heuristic:', i)
        start_time = time.time()
        solution, visited = a_star(puzzle, i)
        end_time = time.time()
        if solution == 0:
            with open("output/" + str(puzzle_index) + "_astar-" + h_to_text(i) + "_search.txt", "w") as search_file:
                search_file.write("no solution")
            with open("output/" + str(puzzle_index) + "_astar-" + h_to_text(i) + "_solution.txt", "w") as solution_file:
                solution_file.write("no solution")
        else:
            solution.reverse()
            index = 0
            with open("output/" + str(puzzle_index) + "_astar-" + h_to_text(i) + "_solution.txt", "w") as solution_file:
                for step in solution:
                    if index == 0:
                        tc = "0 0"
                        index += 1
                    else:
                        tc = str(np.amax(np.bitwise_xor(step.state, solution[index - 1].state))) \
                             +" "+str(step.cost)
                        index += 1
                    solution_file.write(tc+" " + getArrayInString(step.state) +"\n")
                    total_cost = get_cost(visited[len(visited)-1], visited[visited[len(visited) - 1].parent_index], visited)
                solution_file.write(str(total_cost)+" "+str(round(end_time - start_time, 4)))


            index = 0
            with open("output/" + str(puzzle_index) + "_astar-" + h_to_text(i) + "_search.txt", "w") as search_file:
                for visit in visited:
                    try:
                        parent = visited[visit.parent_index]
                    except TypeError:
                        parent = None
                    search_file.write(str(visit.f_val)+" "+str(get_cost(visit, parent, visited))+" "+str(visit.f_val-get_cost(visit, parent, visited))
                                      + " " + getArrayInString(visit.state)+"\n")
                    index += 1

#solve_astar(99, [1, 3, 5, 7, 2, 4, 6, 0])