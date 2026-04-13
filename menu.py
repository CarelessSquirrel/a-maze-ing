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
    while True:
        print("=== A-Maze-ing ===")
        print("1. Re-generating a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Change maze colors")
        print("4. Quit")
        choice = input("Choice (1-4): ")
        if choice == "1":
            re_generate_maze()
        elif choice == "2":
            show_hide_path()
        elif choice == "3":
            change_colors()
        elif choice == "4":
            break
