# 2x2solver

A GUI tool for generating the shortest solution to any scrambled 2x2x2 Rubik's Cube.

## Files

- **`app.py`** — Tkinter GUI. Click a sticker, pick a color to paint it, then
  hit **SOLVE**. Colors: gray (unset), white, yellow, red, orange, blue, green.
- **`solver.py`** — `Solver` class:
  - `encode(state)` — validates a 24-sticker color list and converts it into
    two `State` objects (scrambled state + solved target), by identifying the
    permutation and orientation of each of the 8 corner pieces.
  - `solve(state, target)` — bidirectional BFS between `state` and `target`,
    returns a list of moves (e.g. `["R", "U2", "F'"]`).
  - `run(state)` — top-level entry point; wraps `encode` + `solve` and returns
    either the move list or an `"Error: ..."` string.
- **`state.py`** — `State` class: wraps a single Python `int` that packs the
  positions (3 bits each) and orientations (2 bits each) of all 8 corners.
  Implements the 9 quarter/half turns (`R`, `R2`, `R'`, `U`, `U2`, `U'`, `F`,
  `F2`, `F'`) as in-place bit operations, plus `decode()` for debugging.

## Usage

```bash
python3 app.py
```

Set all 24 stickers to match your physical cube, then click **SOLVE**. The
move sequence appears at the top of the window.

Or run the solver directly and input your scramble:

```bash
python3 solver.py
```

## How it works

1. **Encoding** — one corner is fixed as a reference frame (using the sticker
   colors on it to establish the target orientation), and each of the other
   corners' position + orientation is read off the sticker layout and packed
   into a single ~40-bit integer.
2. **Search** — a bidirectional BFS starts from both the scrambled state and
   the solved state simultaneously, expanding whichever side hasn't reached
   the other yet, until the two frontiers meet. This is much faster than a
   one-directional search, since the state space (3,674,160 positions) is
   heavily concentrated at depth 9–11 — searching from both ends only needs
   to reach about half that depth from each side.
3. **Reconstruction** — once a meeting point is found, the move sequence is
   rebuilt by walking parent pointers back to each side, inverting the moves
   from the "target" side of the search.

## Known facts used for sanity-checking

With this move set (R/U/F, quarter + half turns, one fixed corner), every
reachable state is solvable in **at most 11 moves** ("God's number" for this
metric), with the state counts by optimal solve length:

| Moves | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Count | 1 | 9 | 54 | 321 | 1,847 | 9,992 | 50,136 | 227,536 | 870,072 | 1,887,748 | 623,800 | 2,644 |

## Notes / caveats

- `State` is mutable and defines `__hash__`/`__eq__` by value — never mutate
  a `State` instance that is currently a dict/set key (used in `visited`
  during BFS); always construct a fresh `State(x.state)` before applying a
  move to a "current" state.
- No move-count optimization (e.g. skipping redundant same-face turns) or
  precomputed pruning tables — see the move functions in `state.py` for
  where a faster, allocation-free table-driven version could replace the
  current per-field `read`/`modify` calls if solve time becomes an issue.
- The program can only handle 2x2x2 Rubik's Cubes with the standard color scheme.
