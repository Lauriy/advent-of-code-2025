# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an Advent of Code 2025 solutions repository using Python 3.14 with uv for dependency management and pytest for testing.

## Common Commands

### Running Tests
```shell
# Run all tests (this executes the solutions and validates answers)
uv run pytest

# Run a specific day's tests
uv run pytest tests/test_day_1.py

# Run a specific test function
uv run pytest tests/test_day_1.py::test_solve_first_example

# virtualenv can be activated with (commands not prefixed with uv... might use the system Python otherwise)
source .venv/bin/activate
```

## Code Architecture

### File Structure Pattern

Each day follows this pattern:
- `src/day_N.py` - Solution implementation
- `tests/test_day_N.py` - Tests that validate the solution
- `input/day_N.txt` - Actual puzzle input
- `input/day_N_example.txt` - Example input from problem description
- `descriptions/day_N.txt` - Problem description

### Solution Template

Each day's solution file (`src/day_N.py`) follows this structure:
- `read_input(filename)` - Reads and parses input file
- `solve_first(file_name)` - Solves part 1 of the day's puzzle
- `solve_second(file_name)` - Solves part 2 of the day's puzzle

### Test Pattern

Tests are structured to:
1. Test example inputs first (e.g., `test_solve_first_example()`)
2. Test actual puzzle inputs (e.g., `test_solve_first()`)
3. Part 2 tests are often commented out until part 1 is solved

Tests run the actual solution functions and assert the expected results. The test output shows the answers to the puzzles.
