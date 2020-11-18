import glob
list_of_files = glob.glob('./output/*.txt')


def has_state_been_visited(test_state, visited_states):
    for state in visited_states:
        if (state == test_state).all():
            return True
    return False


def get_array_in_string(array):
    final_string = ""
    if isinstance(array, int):
        return "0"
    if not isinstance(array, list):
        array = array.flatten().tolist()
    for i in range(len(array)):
        final_string += str(array[i]) + " "

    return final_string


def get_index_of_zero(array):
    array_as_list = array.flatten().tolist()
    for index, ele in enumerate(array_as_list):
        if ele == 0:
            return index


def get_analysis():
    analysis = open("analysis.txt", "w")

    uc = []
    gbfs_h1 = []
    gbfs_h2 = []
    a_star_h1 = []
    a_star_h2 = []

    for fileName in list_of_files:
        if fileName.find('uc') != -1:
            uc.append(fileName)

        elif fileName.find('astar-h1') != -1:
            a_star_h1.append(fileName)

        elif fileName.find('astar-h2') != -1:
            a_star_h2.append(fileName)

        elif fileName.find('gbfs-h1') != -1:
            gbfs_h1.append(fileName)

        elif fileName.find('gbfs-h2') != -1:
            gbfs_h2.append(fileName)

    functions = [uc, a_star_h1, a_star_h2, gbfs_h1, gbfs_h2]
    files = ['uc', 'astar-h1', 'astar-h2', 'gbfs-h1', 'gbfs-h2']

    for i in range(len(functions)):
        get_amounts(functions[i], files[i], analysis)
        get_empty(functions[i], files[i], analysis)
        get_solution(functions[i], files[i], analysis)
        analysis.write('\n')


def get_amounts(files, algorithm, file):
    total_search_lines = 0
    total_search_files = 0
    total_solution_lines = 0
    total_solution_files = 0

    for fileName in files:
        if fileName.find('solution') != -1:
            lines = open(fileName).read().splitlines()
            if len(lines) != 0 and lines[0] != 'no solution':
                total_solution_files += 1
                total_solution_lines += len(open(fileName).readlines())

            else:
                total_search_files += 1
                total_search_lines += len(open(fileName).readlines())

    file.write(str(algorithm) + " total search lines: " + str(total_search_lines) + "\n")
    file.write(str(algorithm) + " average search lines: " + str(total_search_lines / total_search_files) + "\n")
    file.write(str(algorithm) + " total solution lines: " + str(total_solution_lines) + "\n")
    file.write(str(algorithm) + " average solution lines: " + str(total_solution_lines / total_solution_files) + "\n")


def get_empty(files, algorithm, file):
    total = 0
    total_solution_files = 0

    for fileName in files:
        if fileName.find('solution') != -1:
            total_solution_files += 1

            if open(fileName).readline() == 'no solution':
                total += 1

    file.write(str(algorithm) + " total no solutions: " + str(total) + "\n")
    file.write(str(algorithm) + " average no solutions: " + str(total / total_solution_files) + "\n")


def get_solution(files, algorithm, file):
    total_cost = 0
    total_execution = 0
    total_files = 0

    for fileName in files:
        if fileName.find('solution') != -1:
            lines = open(fileName).read().splitlines()
            if len(lines) != 0 and lines[0] != 'no solution':
                total_files += 1
                last_line = lines[-1].split(" ")
                if len(last_line) == 2:
                    total_cost += int(last_line[0])
                    total_execution += float(last_line[1])

    file.write(str(algorithm) + " total cost: " + str(total_cost) + "\n")
    file.write(str(algorithm) + " average cost: " + str(total_cost / total_files) + "\n")
    file.write(str(algorithm) + " total execution: " + str(total_execution) + "\n")
    file.write(str(algorithm) + " average execution: " + str(total_execution / total_files) + "\n")


if __name__ == '__main__':
    get_analysis()