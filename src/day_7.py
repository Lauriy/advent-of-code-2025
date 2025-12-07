import os
from collections import deque
from dataclasses import dataclass
from pathlib import Path

SYMBOL_START = "S"
SYMBOL_SPLITTER = "^"
SYMBOL_EMPTY = "."

DEBUG = os.getenv("DEBUG", "").lower() in ("1", "true", "yes")


@dataclass
class BeamState:
    beam_queue: deque
    visited_beams: set
    activated_splitters: set


def read_input(filename: str) -> list[str]:
    with Path(filename).open() as file:
        return [line.rstrip("\n") for line in file]


def find_start(grid: list[str]) -> tuple[int, int]:
    for row_idx, row in enumerate(grid):
        for col_idx, char in enumerate(row):
            if char == SYMBOL_START:
                return row_idx, col_idx

    return -1, -1


def process_splitter(row: int, col: int, grid: list[str], state: BeamState) -> None:
    if (row, col) not in state.activated_splitters:
        state.activated_splitters.add((row, col))
        if DEBUG:
            print(f"  -> Split #{len(state.activated_splitters)} at ({row}, {col})")
    elif DEBUG:
        print(f"  -> Splitter at ({row}, {col}) already activated, skipping")

    left_col = col - 1
    right_col = col + 1

    if left_col >= 0 and (row, left_col) not in state.visited_beams:
        state.beam_queue.append((row, left_col))
        state.visited_beams.add((row, left_col))
        if DEBUG:
            print(f"    Created left beam at ({row}, {left_col})")

    if right_col < len(grid[row]) and (row, right_col) not in state.visited_beams:
        state.beam_queue.append((row, right_col))
        state.visited_beams.add((row, right_col))
        if DEBUG:
            print(f"    Created right beam at ({row}, {right_col})")


def simulate_beam(grid: list[str]) -> int:
    start_row, start_col = find_start(grid)
    if start_row == -1:
        return 0

    state = BeamState(
        beam_queue=deque([(start_row, start_col)]),
        visited_beams={(start_row, start_col)},
        activated_splitters=set(),
    )

    if DEBUG:
        print(f"Starting beam at ({start_row}, {start_col})")

    while state.beam_queue:
        row, col = state.beam_queue.popleft()

        if DEBUG:
            print(f"\nProcessing beam at ({row}, {col})")

        while row < len(grid):
            if DEBUG:
                char = grid[row][col] if col < len(grid[row]) else "?"
                print(f"  Beam at ({row}, {col}): '{char}'")

            if grid[row][col] == SYMBOL_SPLITTER:
                process_splitter(row, col, grid, state)
                break

            row += 1

    return len(state.activated_splitters)


def solve_first(file_name: str) -> int:
    grid = read_input(file_name)

    return simulate_beam(grid)


def process_timeline_position(
    col: int,
    count: int,
    grid_row: str,
    new_timelines: dict,
) -> None:
    if col < len(grid_row) and grid_row[col] == SYMBOL_SPLITTER:
        left_col = col - 1
        right_col = col + 1

        if left_col >= 0:
            new_timelines[left_col] = new_timelines.get(left_col, 0) + count
        if right_col < len(grid_row):
            new_timelines[right_col] = new_timelines.get(right_col, 0) + count

        if DEBUG:
            msg = (
                f"  Position {col} ({count} timelines): splitter, "
                f"creating {count} timelines at {left_col} and {count} at {right_col}"
            )
            print(msg)
    else:
        new_timelines[col] = new_timelines.get(col, 0) + count
        if DEBUG:
            print(f"  Position {col} ({count} timelines): continues")


def count_timelines(grid: list[str]) -> int:
    start_row, start_col = find_start(grid)
    if start_row == -1:
        return 0

    current_timelines = {start_col: 1}

    if DEBUG:
        print(f"Starting quantum particle at ({start_row}, {start_col})")
        print(f"Initial timelines: {current_timelines}")

    for row_idx in range(start_row, len(grid)):
        if not current_timelines:
            break

        if DEBUG:
            print(f"\nRow {row_idx}: timelines = {current_timelines}")

        new_timelines = {}

        for col, count in current_timelines.items():
            process_timeline_position(col, count, grid[row_idx], new_timelines)

        current_timelines = new_timelines

    total_timelines = sum(current_timelines.values())

    if DEBUG:
        print(f"\nFinal timeline distribution: {current_timelines}")
        print(f"Total timelines: {total_timelines}")

    return total_timelines


def solve_second(file_name: str) -> int:
    grid = read_input(file_name)

    return count_timelines(grid)
