from display import create_grid

# handles all user interactions — showing the menu, waiting for input,
# and calling the right function based on what the user chooses
# Options:
#   Re-generate a new maze
#   Show/hide the solution path
#   Change wall colours
#   Quit


def show_menu(maze: list,
              width: int,
              height: int,
              entry: tuple,
              exit: tuple,
              path: list) -> None:
    """
    description
    """
    show_path = False
    colors = ['\033[37m', '\033[32m', '\033[33m', '\033[34m', '\033[35m']
    color_index = 0
    while True:
        create_grid(maze, 25, 20, entry, exit, path if show_path else None, colors[color_index])
        print("=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Change maze colors")
        print("4. Quit")
        choice = input("Choice (1-4): ")
        if choice == "1":
            pass
        elif choice == "2":
            show_path = not show_path
        elif choice == "3":
            color_index = (color_index + 1) % len(colors)
        elif choice == "4":
            break
