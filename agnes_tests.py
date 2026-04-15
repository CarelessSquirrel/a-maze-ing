from file_reader import read_maze_file
from file_reader import decode_cell
from file_reader import process_directions
from display import create_grid
from menu import show_menu

# a place to test my functions

# test file_reader

# directions = ['S', 'W', 'S', 'E', 'S', 'W', 'S', 'E', 'S', 'W', 'S', 'S', 'S', 'E', 'E', 'S', 'E', 'E', 'E', 'E', 'N', 'E', 'E', 'S', 'E', 'S', 'E', 'E', 'S', 'S', 'S', 'E', 'E', 'E', 'S', 'S', 'S', 'E', 'E', 'E', 'N', 'N', 'E', 'N', 'E', 'E']

directions = ['E','S','S','W','S','S','S','S','E','N','E','S','S','E','N','E','N','W','N','W','W','N','E','N','N','N','E','E','E','E','S','E','S','W','W','W','W','S','E','E','E','E','E','N','E','E','E','E','S','W','W','S','E','E','E','S','E','E','E','S','W','S','S','E','N','E','N','E','S','S','S','W','S','S','W','W','W','W','S','W','W','S','S','E','N','E','E','N','E','S','S','E','E','E','N','W','N','E','N','E','S','S','S']

# print(read_maze_file("temp_mock_maze.txt"))
# print(decode_cell('A'))
# print(process_directions(directions, (1, 1)))

# test display

result = read_maze_file("jacobs_maze.txt")
maze = result[0]
entry = result[1]
exit = result[2]
path = process_directions(directions, entry)
show_menu(maze, 20, 15, entry, exit, path)
