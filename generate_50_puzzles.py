import random
def generate_puzzles():
    output_file = open("random_puzzles.txt", "w")
    for i in range (50):
        arr = [0,1,2,3,4,5,6,7]
        random.shuffle(arr)
        

        for item in arr:
            output_file.write(str(item) + " ")
        output_file.write('\n')

if __name__ == '__main__':
    generate_puzzles()