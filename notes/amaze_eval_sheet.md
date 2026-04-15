# A-Maze-ing — Evaluation Sheet (& notes)


## Basics

### Submitted files and Norm
Check that all expected files are present in the Git repository:
- `README.md`
- `a_maze_ing.py`
- `mazegen.tar.gz` (the reusable package)
- A configuration file
- All needed elements to build the maze generator package again

> **note:** If any of these files is missing, the grade is automatically 0. The evaluator also checks that flake8 and mypy norm passes on all Python files!!
---

## README.md file

Does the repository contain a README.md at its root with all of the following?

- First line italicized: *This project has been created as part of the 42 curriculum by \<login\>, \<login\>.*
- A "Description" section explaining the project's purpose and a brief overview.
- An "Instructions" section with details about compilation, installation, and/or execution.
- A "Resources" section listing external references (documentation, tutorials, etc.) and explaining how AI was used — specifying for which tasks and which parts of the project.
- The complete description of the configuration file format.
- The chosen maze generation algorithm.
- The reason for choosing this algorithm.
- Short documentation about the maze generator reusable module.
- Team and project management section including:
  - The roles of each team member.
  - Your anticipated planning and how it evolved until the end.
  - What worked well and what could be improved.
  - Have you used any specific tools? Which ones?

> **note:** there can be more sections if we want but the required ones should be there

---

## Standard Usage

### Display
Run the `a_maze_ing.py` script using a default configuration file. You should get:
- A maze randomly generated.
- Displayed in the terminal or using a dedicated graphic window.
- A way to interact with the program.

> **note:** This is the basic test — does the program actually run and show something

### Interactive menu
Among the possible interactions, the mandatory ones are:
- Re-generate a new maze.
- A toggle to show and hide the shortest path from entry to exit.
- A button/option to change the colours of the walls.
- Extra interactions are possible (e.g., changing the colour of the '42' pattern, quitting the program...).

> **note:** These three interactions are the minimum, if any is missing or broken, its a fail

---

## Configuration file

### Format
Check that the configuration file follows the requirements:
- Comment lines start with `#`.
- Each line is in the `KEY=VALUE` format (lowercase is also OK).
- The expected keys are present: `WIDTH`, `HEIGHT`, `ENTRY`, `EXIT`, `OUTPUT_FILE`, `PERFECT`.

> **note:** The evaluator will open your config file and manually check these things

### Error Management
The evaluator will edit the configuration file to test that the program correctly handles errors:
- Remove a mandatory key.
- Add a line that doesn't respect the `KEY=VALUE` format (e.g., without the `=` sign).
- Replace numbers by letters (e.g., WIDTH=abc).
- Use an incorrect boolean for `PERFECT` (e.g., `PERFECT=maybe`).
- Use a wrong format for `ENTRY` or `EXIT` (e.g., wrong number of values or wrong type).

> **note:** If the program crashes on any of these — instead of printing a clear error message the final grade is 0. Config parser must be reaady for all the checks

---

## Output file

### Format
Run `a_maze_ing.py` and verify that the first generated maze is also stored in the defined output file. You should find:
- `HEIGHT` lines of `WIDTH` characters each (the hex-encoded maze).
- An empty line.
- The `ENTRY` tuple.
- The `EXIT` tuple.
- The shortest path from entry to exit described using directions `N`, `E`, `S`, `W`.

The validation script provided with the subject is used to control wall coherence. The shortest path sequence in the output file must match its visual representation.

> **note:** The coherence check is automated — the evaluator runs a script. The path in the file must match what is visually displayed.

---

## Maze Generator module

### Maze generation
The maze generator module must meet the subject's expectations:

- A randomly generated maze, eventually using Python's `random` module.
- Adopt a relevant behaviour when parameters are inconsistent (e.g., entry/exit outside the maze, negative width/height).
- All cells can be reached, except those creating the '42' pattern.
- Walls all around the maze (external borders are closed).
- No 3x3 or larger open zone without walls — the evaluator will ask how this was implemented or verified in the code.
- The '42' pattern is present in the maze (except if the size is too small — in that case a message should appear on the terminal).
- A perfect maze when `PERFECT=True` in the config file.
- The same maze is reproducible when using an identical seed.

> **note:** Jacob gets these questions. Make sure there is no-3x3 rule

### Reusable module
The evaluator will:
1. Ask you to re-generate the package in a virtualenv.
2. This must re-create the `mazegen-*.tar.gz` or `.whl` file.
3. Then, in a different virtualenv, install the newly created package and test it with `a_maze_ing.py` and its configuration file.
4. Check that everything works properly.

> **note:** This is a live test for being able to rebuild your package from scratch in a virtual environment. We should practice it before evaluation.

---

## Bonuses

Bonuses can only be considered if all previous questions were successful.
Up to 5 different working bonuses can be validated. Each bonus must represent a fair amount of work.

Some ideas:
- add animation during maze generation (?)
- make the output more interesting using mlx
- try combining the ascii symbols with mlx window and show the combination options
- add some color schemes
- some interaction besides the basic stuff
