*This project has been created as part of the 42 curriculum by agbumbie, jabettin.*

---

## Description

A-Maze-ing is a Python maze generator and interactive terminal viewer. Given a configuration file, the program generates a random maze, finds the shortest path from entry to exit, saves the result to a file in hexadecimal wall encoding, and displays it in the terminal using ASCII block characters with ANSI colours. The user can regenerate the maze, toggle the solution path, and change wall colours through an interactive menu.

---

## Instructions

### Requirements

- Python 3.10 or later
- No external dependencies beyond the standard library

### Installation

```bash
# Clone the repository
git clone [your repo URL]
cd [repo folder]

# Install dependencies and the mazegen package
make install
```

### Running the program

```bash
make run
```

Or directly:

```bash
python3 a_maze_ing.py config.txt
```

If no config file is specified, `config.txt` in the current directory is used by default.

### Debug mode

```bash
make debug
```

Launches the program with Python's built-in debugger (pdb), pausing at the first line. Useful commands once inside pdb:

| Command | Description |
|---|---|
| `n` | Execute the next line |
| `c` | Continue running until the next breakpoint or end |
| `l` | Show the current code around where you are |
| `p <variable>` | Print the value of a variable |
| `b <line>` | Set a breakpoint at a line number |
| `q` | Quit the debugger |

### Linting

```bash
make lint
```

Runs flake8 for style checking and mypy for static type checking.

```bash
make lint-strict
```

Same as above but with mypy's strict mode enabled.

### Cleaning up

```bash
make clean
```

Removes `__pycache__`, `.mypy_cache`, build artifacts and other temporary files.

### Validating the maze output

```bash
python3 output_validator.py maze.txt
```

If no errors are printed, the maze encoding is valid.

---

## Configuration file

The configuration file uses `KEY=VALUE` format, one pair per line. Lines starting with `#` are comments and are ignored. All six keys below are mandatory.

| Key | Type | Description | Example |
|---|---|---|---|
| `WIDTH` | int | Number of cells horizontally | `WIDTH=20` |
| `HEIGHT` | int | Number of cells vertically | `HEIGHT=15` |
| `ENTRY` | x,y | Entry cell coordinates | `ENTRY=0,0` |
| `EXIT` | x,y | Exit cell coordinates | `EXIT=19,14` |
| `OUTPUT_FILE` | str | Path to write the maze output | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | bool | Whether to generate a perfect maze (one path only) | `PERFECT=True` |

Additional optional keys may be added (e.g. `SEED` for reproducibility).

---

## Maze generation algorithm

The maze is generated using **randomised depth-first search** (recursive backtracker). Starting from a random cell, the algorithm carves passages by recursively visiting unvisited neighbours in a random order. This produces a perfect maze (exactly one path between any two cells) when `PERFECT=True`.

### Why this algorithm?

Recursive backtracker is simple to implement, produces mazes with long winding corridors and relatively few dead ends, and is well understood — making it easy to reason about correctness and explain during evaluation. It also naturally produces a spanning tree, which is a perfect maze by definition.

---

## Reusable module

The maze generation logic is packaged as `mazegen`, installable via pip.

### Installation

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

### Basic usage

```python
from mazegen import generate_maze, solve_maze

# Generate a 20x15 maze with entry (0,0) and exit (19,14)
cells, has_42 = generate_maze(
    width=20,
    height=15,
    entry=(0, 0),
    exit=(19, 14),
    perfect=True,
)

# Find the shortest path
path = solve_maze(cells, entry=(0, 0), exit=(19, 14), width=20, height=15)
# path is a list of direction strings e.g. ['S', 'E', 'E', 'N', ...]
```

### Custom parameters

| Parameter | Type | Description |
|---|---|---|
| `width` | int | Number of cells horizontally |
| `height` | int | Number of cells vertically |
| `entry` | tuple(int, int) | Entry cell coordinates |
| `exit` | tuple(int, int) | Exit cell coordinates |
| `perfect` | bool | Whether to enforce a single solution path |

### Accessing the maze structure

`generate_maze()` returns a 2D list of integers (`cells`). Each integer encodes the walls of a cell as a 4-bit bitmask:

| Bit | Direction |
|---|---|
| 0 (LSB) | North |
| 1 | East |
| 2 | South |
| 3 | West |

A bit set to `1` means the wall is closed. Example: `9` (binary `1001`) means north and west walls are closed.

### Rebuilding and testing the package

```bash
# Step 1 — create a virtualenv and build the package
python3 -m venv build_env
source build_env/bin/activate
pip install build
python3 -m build
# output: dist/mazegen-1.0.0-py3-none-any.whl

# Step 2 — in a fresh virtualenv, install and test it
deactivate
python3 -m venv test_env
source test_env/bin/activate
pip install dist/mazegen-1.0.0-py3-none-any.whl
python3 a_maze_ing.py config.txt
deactivate
```

If the program runs correctly without import errors, the package is working.

---

## Resources

### References

- [Maze generation algorithms — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Recursive backtracker explained — Jamis Buck's blog](https://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking)
- [Python type hints — mypy documentation](https://mypy.readthedocs.io/en/stable/)
- [ANSI escape codes — Wikipedia](https://en.wikipedia.org/wiki/ANSI_escape_code)
- [PEP 257 — Docstring conventions](https://peps.python.org/pep-0257/)
- [Python docs - reading and writing files (for file_reader)](https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files)
- [Mypy documentation](https://mypy.readthedocs.io/en/stable/)

### AI usage

Claude (Anthropic) was used throughout this project as a learning and debugging tool:
- Conceptual explanations of bitwise operations, intersection-based rendering, and maze algorithms
- Socratic guidance through building the display files, and step by step explanation of new concepts
- Debugging mypy errors and flake8 norm issues
- Generating the process flow diagram for the README
- All code was understood, reviewed, and written by the team members

---

## Team and project management

### Roles

- **agbumbie** — visual layer: `file_reader.py`, `display.py`, `menu.py`
- **jabettin** — algorithm layer: `mazegen/` package, `config_parser.py`, `a_maze_ing.py`

### Planning

As this was our first team project, our plan was to divide the work in broad terms and have check-ins every couple of days.
It was hard to set a clear structure from the beginning (as we didn't know what to expect) but as we built our program, the steps
became more clear and we managed to create workflow for ourselves that suited our schedules.

Our plan evolved as follows: 
- dive into our individual assignments (algorithm for jabettin & visual representation for agbumbie)
- share our progress on files we will each need to create, see potential overlaps and dependencies
- work with mock maze, path and entry & exit point data to create visual part (agbumbie)
- meanwhile algorithm part was developed (jabettin)
- gluing these two parts together
- work on overall improvement of our code - quality (flake8, mypy, readability) and clarity of flow represented in a diagram
- final testing and checks for error handling

### What worked well

- splitting into algorithm/visual early
- defining the interface contract upfront (using an example from the subject as a reference)
- using mock data to develop display independently
- ??

### What could be improved

- crearer communication during work (we had overlapping menu.py file that we had to merge)
- earlier integration testing
- checkin in more often in smaller steps (that could make the big picture easier to understand once the project was finished)

### Tools used

- **Claude** (Anthropic) — learning support and debugging
- **draw.io** — project flow diagram
- **VSCode** — development environment
- **Git / vogsphere + GitHub** — version control and collaboration
