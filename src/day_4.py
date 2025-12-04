import os
from pathlib import Path

DEBUG = os.getenv("DEBUG", "").lower() in ("1", "true", "yes")

PAPER_ROLL = "@"
EMPTY_SPACE = "."

MAX_NEIGHBORS_FOR_ACCESS = 4

DIRECTIONS = [
    (-1, -1),
    (-1, 0),
    (-1, 1),  # top row
    (0, -1),
    (0, 1),  # left and right
    (1, -1),
    (1, 0),
    (1, 1),  # bottom row
]


def read_input(filename: str) -> list[str]:
    with Path(filename).open() as f:
        return [line.strip() for line in f if line.strip()]


def count_neighbors(grid: list[str], row: int, col: int) -> int:
    rows = len(grid)
    cols = len(grid[0])
    count = 0

    for dr, dc in DIRECTIONS:
        new_row = row + dr
        new_col = col + dc

        in_bounds = 0 <= new_row < rows and 0 <= new_col < cols
        if in_bounds and grid[new_row][new_col] == PAPER_ROLL:
            count += 1

    return count


def solve_first(file_name: str) -> int:
    grid = read_input(file_name)
    accessible_count = 0

    if DEBUG:
        print(f"Grid size: {len(grid)}x{len(grid[0])}\n")

    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == PAPER_ROLL:
                neighbors = count_neighbors(grid, row, col)

                if neighbors < MAX_NEIGHBORS_FOR_ACCESS:
                    accessible_count += 1
                    if DEBUG:
                        print(
                            f"Row {row}, Col {col}: @ with {neighbors} "
                            f"neighbors - ACCESSIBLE"
                        )
                elif DEBUG:
                    print(
                        f"Row {row}, Col {col}: @ with {neighbors} "
                        f"neighbors - not accessible"
                    )

    if DEBUG:
        print(f"\nTotal accessible rolls: {accessible_count}")

    return accessible_count


def find_accessible_rolls_mutable(
    grid: list[list[str]], rows: int, cols: int
) -> list[tuple[int, int]]:
    to_remove = []
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == PAPER_ROLL:
                neighbors = 0
                for dr, dc in DIRECTIONS:
                    nr, nc = row + dr, col + dc
                    in_bounds = 0 <= nr < rows and 0 <= nc < cols
                    if in_bounds and grid[nr][nc] == PAPER_ROLL:
                        neighbors += 1

                if neighbors < MAX_NEIGHBORS_FOR_ACCESS:
                    to_remove.append((row, col))

    return to_remove


def solve_second(file_name: str) -> int:
    lines = read_input(file_name)
    # Convert to mutable grid (list of lists)
    grid = [list(line) for line in lines]
    rows = len(grid)
    cols = len(grid[0])

    total_removed = 0
    iteration = 0

    if DEBUG:
        print(f"Initial grid size: {rows}x{cols}")
        print("Initial state:")
        for row in grid:
            print("".join(row))
        print()

    while True:
        iteration += 1

        to_remove = find_accessible_rolls_mutable(grid, rows, cols)

        if not to_remove:
            if DEBUG:
                print(
                    f"No more accessible rolls. "
                    f"Stopping after {iteration - 1} iterations."
                )
            break

        for row, col in to_remove:
            grid[row][col] = EMPTY_SPACE

        removed_count = len(to_remove)
        total_removed += removed_count

        if DEBUG:
            print(f"Iteration {iteration}: Removed {removed_count} rolls")
            print(f"Total removed so far: {total_removed}")
            for row in grid:
                print("".join(row))
            print()

    if DEBUG:
        print(f"Final total removed: {total_removed}")

    return total_removed
