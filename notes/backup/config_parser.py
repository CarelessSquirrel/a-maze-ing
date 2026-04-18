from __future__ import annotations

from typing import Any, Dict


# All keys the config file must contain (case-insensitive on read)
_REQUIRED_KEYS = {'WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'OUTPUT_FILE', 'PERFECT'}

# Accepted string values that map to boolean True / False
_TRUE_VALUES = {'true',  '1', 'yes'}
_FALSE_VALUES = {'false', '0', 'no'}


def parse_config(filename: str) -> Dict[str, Any]:
    """
    Read and validate *filename* (KEY=VALUE format).

    Accepted comment lines start with '#'.  Blank lines are ignored.

    Returns a dict with validated, typed values:
        {
            'WIDTH':       int,
            'HEIGHT':      int,
            'ENTRY':       (int, int),
            'EXIT':        (int, int),
            'OUTPUT_FILE': str,
            'PERFECT':     bool,
        }

    Raises ValueError with a descriptive message for every kind of bad input
    so that the caller can print the error instead of letting the program crash
    """
    raw: Dict[str, str] = {}

    with open(filename, 'r') as fh:
        for line_num, line in enumerate(fh, start=1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' not in line:
                raise ValueError(
                    f"Line {line_num}: expected KEY=VALUE format, got:"
                    f"{line!r}"
                )
            key, _, value = line.partition('=')
            raw[key.strip().upper()] = value.strip()

    # ------------------------------------------------------------------ #
    # 1. Check all required keys are present                              #
    # ------------------------------------------------------------------ #
    missing = _REQUIRED_KEYS - raw.keys()
    if missing:
        raise ValueError(
            f"Missing required key(s): {', '.join(sorted(missing))}"
        )

    result: Dict[str, Any] = {}

    # ------------------------------------------------------------------ #
    # 2. WIDTH and HEIGHT — positive integers                             #
    # ------------------------------------------------------------------ #
    for key in ('WIDTH', 'HEIGHT'):
        try:
            val = int(raw[key])
        except ValueError:
            raise ValueError(
                f"{key} must be an integer, got: {raw[key]!r}"
            )
        if val <= 0:
            raise ValueError(f"{key} must be greater than 0, got: {val}")
        result[key] = val

    # ------------------------------------------------------------------ #
    # 3. ENTRY and EXIT — "x,y" pairs of non-negative integers           #
    # ------------------------------------------------------------------ #
    for key in ('ENTRY', 'EXIT'):
        parts = raw[key].split(',')
        if len(parts) != 2:
            raise ValueError(
                f"{key} must be in 'x,y' format, got: {raw[key]!r}"
            )
        try:
            x, y = int(parts[0]), int(parts[1])
        except ValueError:
            raise ValueError(
                f"{key} coordinates must be integers, got: {raw[key]!r}"
            )
        result[key] = (x, y)

    # ------------------------------------------------------------------ #
    # 4. PERFECT — boolean                                                #
    # ------------------------------------------------------------------ #
    perfect_raw = raw['PERFECT'].lower()
    if perfect_raw in _TRUE_VALUES:
        result['PERFECT'] = True
    elif perfect_raw in _FALSE_VALUES:
        result['PERFECT'] = False
    else:
        raise ValueError(
            f"PERFECT must be a boolean (True/False), got: {raw['PERFECT']!r}"
        )

    # ------------------------------------------------------------------ #
    # 5. OUTPUT_FILE — plain string (no further validation needed)        #
    # ------------------------------------------------------------------ #
    result['OUTPUT_FILE'] = raw['OUTPUT_FILE']

    # ------------------------------------------------------------------ #
    # 6. Cross-field validation: entry and exit must lie inside the maze  #
    # ------------------------------------------------------------------ #
    width, height = result['WIDTH'], result['HEIGHT']
    for key in ('ENTRY', 'EXIT'):
        x, y = result[key]
        if not (0 <= x < width and 0 <= y < height):
            raise ValueError(
                f"{key} ({x},{y}) is outside the maze bounds "
                f"({width}x{height})"
            )

    return result
