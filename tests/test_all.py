"""
Comprehensive tests for A-Maze-ing.
Tests config_parser, file_reader, and display functions.
Run with: python3 test_all.py
"""

import os
import tempfile
import traceback

PASS = "\033[32mPASS\033[0m"
FAIL = "\033[31mFAIL\033[0m"
SECTION = "\033[34m"
RESET = "\033[0m"
passed = 0
failed = 0


def test(name: str, fn) -> None:
    global passed, failed
    try:
        fn()
        print(f"  {PASS}  {name}")
        passed += 1
    except Exception as e:
        print(f"  {FAIL}  {name}")
        print(f"        {e}")
        traceback.print_exc()
        failed += 1


def write_config(content: str) -> str:
    """Write a temporary config file and return its path."""
    f = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
    f.write(content)
    f.close()
    return f.name


def write_maze_file(content: str) -> str:
    """Write a temporary maze output file and return its path."""
    f = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
    f.write(content)
    f.close()
    return f.name


# ─────────────────────────────────────────────────────────────────────────────
# CONFIG PARSER TESTS
# ─────────────────────────────────────────────────────────────────────────────
print(f"\n{SECTION}── config_parser ──────────────────────────────────────{RESET}")

from config_parser import parse_config  # noqa: E402


def test_valid_config():
    path = write_config(
        "WIDTH=20\nHEIGHT=15\nENTRY=0,0\nEXIT=19,14\n"
        "OUTPUT_FILE=maze.txt\nPERFECT=True\n"
    )
    cfg = parse_config(path)
    assert cfg['WIDTH'] == 20
    assert cfg['HEIGHT'] == 15
    assert cfg['ENTRY'] == (0, 0)
    assert cfg['EXIT'] == (19, 14)
    assert cfg['OUTPUT_FILE'] == 'maze.txt'
    assert cfg['PERFECT'] is True
    os.unlink(path)


test("valid config parses correctly", test_valid_config)


def test_comments_ignored():
    path = write_config(
        "# this is a comment\nWIDTH=10\nHEIGHT=10\n"
        "ENTRY=0,0\nEXIT=9,9\nOUTPUT_FILE=out.txt\nPERFECT=False\n"
    )
    cfg = parse_config(path)
    assert cfg['WIDTH'] == 10
    os.unlink(path)


test("comment lines are ignored", test_comments_ignored)


def test_lowercase_keys():
    path = write_config(
        "width=10\nheight=10\nentry=0,0\nexit=9,9\n"
        "output_file=out.txt\nperfect=true\n"
    )
    cfg = parse_config(path)
    assert cfg['WIDTH'] == 10
    os.unlink(path)


test("lowercase keys are accepted", test_lowercase_keys)


def test_missing_key():
    path = write_config(
        "WIDTH=20\nHEIGHT=15\nENTRY=0,0\nEXIT=19,14\nPERFECT=True\n"
    )
    try:
        parse_config(path)
        assert False, "should have raised ValueError"
    except ValueError as e:
        assert "OUTPUT_FILE" in str(e) or "Missing" in str(e)
    finally:
        os.unlink(path)


test("missing key raises ValueError", test_missing_key)


def test_no_equals_sign():
    path = write_config(
        "WIDTH 20\nHEIGHT=15\nENTRY=0,0\nEXIT=19,14\n"
        "OUTPUT_FILE=out.txt\nPERFECT=True\n"
    )
    try:
        parse_config(path)
        assert False, "should have raised ValueError"
    except ValueError as e:
        assert "KEY=VALUE" in str(e) or "format" in str(e)
    finally:
        os.unlink(path)


test("line without '=' raises ValueError", test_no_equals_sign)


def test_width_not_integer():
    path = write_config(
        "WIDTH=abc\nHEIGHT=15\nENTRY=0,0\nEXIT=19,14\n"
        "OUTPUT_FILE=out.txt\nPERFECT=True\n"
    )
    try:
        parse_config(path)
        assert False, "should have raised ValueError"
    except ValueError as e:
        assert "WIDTH" in str(e)
    finally:
        os.unlink(path)


test("non-integer WIDTH raises ValueError", test_width_not_integer)


def test_negative_width():
    path = write_config(
        "WIDTH=-5\nHEIGHT=15\nENTRY=0,0\nEXIT=19,14\n"
        "OUTPUT_FILE=out.txt\nPERFECT=True\n"
    )
    try:
        parse_config(path)
        assert False, "should have raised ValueError"
    except ValueError as e:
        assert "WIDTH" in str(e)
    finally:
        os.unlink(path)


test("negative WIDTH raises ValueError", test_negative_width)


def test_invalid_perfect():
    path = write_config(
        "WIDTH=20\nHEIGHT=15\nENTRY=0,0\nEXIT=19,14\n"
        "OUTPUT_FILE=out.txt\nPERFECT=maybe\n"
    )
    try:
        parse_config(path)
        assert False, "should have raised ValueError"
    except ValueError as e:
        assert "PERFECT" in str(e)
    finally:
        os.unlink(path)


test("invalid PERFECT value raises ValueError", test_invalid_perfect)


def test_entry_wrong_format():
    path = write_config(
        "WIDTH=20\nHEIGHT=15\nENTRY=0\nEXIT=19,14\n"
        "OUTPUT_FILE=out.txt\nPERFECT=True\n"
    )
    try:
        parse_config(path)
        assert False, "should have raised ValueError"
    except ValueError as e:
        assert "ENTRY" in str(e)
    finally:
        os.unlink(path)


test("ENTRY with wrong format raises ValueError", test_entry_wrong_format)


def test_entry_letters():
    path = write_config(
        "WIDTH=20\nHEIGHT=15\nENTRY=a,b\nEXIT=19,14\n"
        "OUTPUT_FILE=out.txt\nPERFECT=True\n"
    )
    try:
        parse_config(path)
        assert False, "should have raised ValueError"
    except ValueError as e:
        assert "ENTRY" in str(e)
    finally:
        os.unlink(path)


test("ENTRY with letters raises ValueError", test_entry_letters)


def test_entry_outside_bounds():
    path = write_config(
        "WIDTH=10\nHEIGHT=10\nENTRY=99,99\nEXIT=9,9\n"
        "OUTPUT_FILE=out.txt\nPERFECT=True\n"
    )
    try:
        parse_config(path)
        assert False, "should have raised ValueError"
    except ValueError as e:
        assert "ENTRY" in str(e) or "bounds" in str(e)
    finally:
        os.unlink(path)


test("ENTRY outside maze bounds raises ValueError", test_entry_outside_bounds)


def test_file_not_found():
    try:
        parse_config("this_file_does_not_exist.txt")
        assert False, "should have raised FileNotFoundError"
    except FileNotFoundError:
        pass


test("missing config file raises FileNotFoundError", test_file_not_found)


def test_perfect_false():
    path = write_config(
        "WIDTH=10\nHEIGHT=10\nENTRY=0,0\nEXIT=9,9\n"
        "OUTPUT_FILE=out.txt\nPERFECT=False\n"
    )
    cfg = parse_config(path)
    assert cfg['PERFECT'] is False
    os.unlink(path)


test("PERFECT=False parses correctly", test_perfect_false)


# ─────────────────────────────────────────────────────────────────────────────
# FILE READER TESTS
# ─────────────────────────────────────────────────────────────────────────────
print(f"\n{SECTION}── file_reader ─────────────────────────────────────────{RESET}")

from file_reader import read_maze_file, decode_cell, process_directions  # noqa: E402

MOCK_MAZE = (
    "9515\n"
    "EBAB\n"
    "96A8\n"
    "\n"
    "0,0\n"
    "3,2\n"
    "SSEE\n"
)


def test_read_maze_file():
    path = write_maze_file(MOCK_MAZE)
    maze, entry, exit_, path_ = read_maze_file(path)
    assert len(maze) == 3
    assert len(maze[0]) == 4
    assert entry == (0, 0)
    assert exit_ == (3, 2)
    assert path_ == ['S', 'S', 'E', 'E']
    os.unlink(path)


test("read_maze_file returns correct structure", test_read_maze_file)


def test_decode_cell_north():
    walls = decode_cell('1')  # binary 0001 = north wall
    assert walls['north'] is True
    assert walls['east'] is False
    assert walls['south'] is False
    assert walls['west'] is False


test("decode_cell '1' = north wall only", test_decode_cell_north)


def test_decode_cell_east():
    walls = decode_cell('2')  # binary 0010 = east wall
    assert walls['north'] is False
    assert walls['east'] is True


test("decode_cell '2' = east wall only", test_decode_cell_east)


def test_decode_cell_all_walls():
    walls = decode_cell('F')  # binary 1111 = all walls
    assert all(walls[d] for d in ['north', 'east', 'south', 'west'])


test("decode_cell 'F' = all walls closed", test_decode_cell_all_walls)


def test_decode_cell_no_walls():
    walls = decode_cell('0')  # binary 0000 = no walls
    assert not any(walls[d] for d in ['north', 'east', 'south', 'west'])


test("decode_cell '0' = no walls", test_decode_cell_no_walls)


def test_decode_cell_9():
    walls = decode_cell('9')  # binary 1001 = north + west
    assert walls['north'] is True
    assert walls['west'] is True
    assert walls['east'] is False
    assert walls['south'] is False


test("decode_cell '9' = north + west", test_decode_cell_9)


def test_process_directions_south():
    coords = process_directions(['S'], (0, 0))
    assert coords == [(0, 1)]


test("process_directions S moves south", test_process_directions_south)


def test_process_directions_east():
    coords = process_directions(['E'], (0, 0))
    assert coords == [(1, 0)]


test("process_directions E moves east", test_process_directions_east)


def test_process_directions_multi():
    coords = process_directions(['S', 'S', 'E', 'E'], (0, 0))
    assert coords[-1] == (2, 2)


test("process_directions SSEE ends at (2,2)", test_process_directions_multi)


def test_process_directions_north():
    coords = process_directions(['N'], (0, 1))
    assert coords == [(0, 0)]


test("process_directions N moves north", test_process_directions_north)


def test_process_directions_west():
    coords = process_directions(['W'], (1, 0))
    assert coords == [(0, 0)]


test("process_directions W moves west", test_process_directions_west)


# ─────────────────────────────────────────────────────────────────────────────
# DISPLAY TESTS
# ─────────────────────────────────────────────────────────────────────────────
print(f"\n{SECTION}── display ─────────────────────────────────────────────{RESET}")

from display import paint_maze, create_grid  # noqa: E402


def test_paint_entry():
    color = paint_maze(0, 0, (0, 0), (3, 2), None, False)
    assert color == '\033[95m'  # MAGENTA


test("paint_maze returns MAGENTA for entry cell", test_paint_entry)


def test_paint_exit():
    color = paint_maze(3, 2, (0, 0), (3, 2), None, False)
    assert color == '\033[91m'  # RED


test("paint_maze returns RED for exit cell", test_paint_exit)


def test_paint_path():
    path = [(1, 0), (2, 0)]
    color = paint_maze(1, 0, (0, 0), (3, 2), path, False)
    assert color == '\033[96m'  # CYAN


test("paint_maze returns CYAN for path cell", test_paint_path)


def test_paint_42():
    color = paint_maze(1, 1, (0, 0), (3, 2), None, True)
    assert color == '\033[94m'  # BLUE


test("paint_maze returns BLUE for 42 cell", test_paint_42)


def test_paint_normal():
    color = paint_maze(1, 1, (0, 0), (3, 2), None, False)
    assert color == '\033[0m'  # RESET


test("paint_maze returns RESET for normal cell", test_paint_normal)


def test_create_grid_runs():
    maze = [['9', '1'], ['C', '5']]
    create_grid(maze, 2, 2, (0, 0), (1, 1))


test("create_grid runs without crashing", test_create_grid_runs)


def test_create_grid_with_path():
    maze = [['9', '1'], ['C', '5']]
    path = [(1, 0), (1, 1)]
    create_grid(maze, 2, 2, (0, 0), (1, 1), path)


test("create_grid runs with path", test_create_grid_with_path)


def test_create_grid_with_color():
    maze = [['9', '1'], ['C', '5']]
    create_grid(maze, 2, 2, (0, 0), (1, 1), None, '\033[32m')


test("create_grid runs with custom wall color", test_create_grid_with_color)


# ─────────────────────────────────────────────────────────────────────────────
# SUMMARY
# ─────────────────────────────────────────────────────────────────────────────
total = passed + failed
print(f"\n{'─' * 52}")
print(f"  {passed}/{total} tests passed", end="")
if failed == 0:
    print(f"  \033[32mall good!\033[0m")
else:
    print(f"  \033[31m{failed} failed\033[0m")
print()
