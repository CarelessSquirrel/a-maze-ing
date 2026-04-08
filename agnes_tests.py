from file_reader import read_maze_file
from file_reader import decode_cell
from file_reader import process_directions

# Place to test my functions

directions = ['S', 'W', 'S', 'E', 'S', 'W', 'S', 'E', 'S', 'W', 'S', 'S', 'S', 'E', 'E', 'S', 'E', 'E', 'E', 'E', 'N', 'E', 'E', 'S', 'E', 'S', 'E', 'E', 'S', 'S', 'S', 'E', 'E', 'E', 'S', 'S', 'S', 'E', 'E', 'E', 'N', 'N', 'E', 'N', 'E', 'E']

print(read_maze_file("temp_mock_maze.txt"))
print(decode_cell('A'))
print(process_directions(directions, (1, 1)))
