import os
from pathlib import Path

OPERATOR_ADD = "+"
OPERATOR_MULTIPLY = "*"

DEBUG = os.getenv("DEBUG", "").lower() in ("1", "true", "yes")


def read_input(filename: str) -> list[str]:
    with Path(filename).open() as file:
        return [line.rstrip("\n") for line in file]


def identify_separators(grid: list[str]) -> list[bool]:
    """Identify which columns contain only spaces (separators)."""
    if not grid:
        return []

    num_cols = len(grid[0]) if grid else 0
    is_separator = []

    for col_idx in range(num_cols):
        all_spaces = all(col_idx >= len(row) or row[col_idx] == " " for row in grid)
        is_separator.append(all_spaces)

    return is_separator


def group_problem_columns(is_separator: list[bool]) -> list[list[int]]:
    """Group consecutive non-separator columns into problems."""
    problems = []
    current_problem_cols = []

    for col_idx, is_sep in enumerate(is_separator):
        if not is_sep:
            current_problem_cols.append(col_idx)
        elif current_problem_cols:
            problems.append(current_problem_cols)
            current_problem_cols = []

    if current_problem_cols:
        problems.append(current_problem_cols)

    return problems


def parse_worksheet(lines: list[str]) -> tuple[list[str], list[list[int]]]:
    # Find the maximum line length to create a uniform grid
    max_len = max(len(line) for line in lines) if lines else 0

    # Pad lines to make them all the same length
    grid = [line.ljust(max_len) for line in lines]

    if DEBUG:
        print(f"Grid ({len(grid)} rows x {max_len} cols):")
        for i, row in enumerate(grid):
            print(f"  Row {i}: '{row}'")

    is_separator = identify_separators(grid)

    if DEBUG:
        separator_indices = [i for i, sep in enumerate(is_separator) if sep]
        print(f"\nSeparator columns: {separator_indices}")

    problems = group_problem_columns(is_separator)

    if DEBUG:
        print(f"\nFound {len(problems)} problems:")
        for i, prob in enumerate(problems):
            print(f"  Problem {i}: columns {prob}")

    return grid, problems


def extract_operator(grid: list[str], col_indices: list[int]) -> str | None:
    """Extract the operator from the last row of the problem."""
    last_row_text = "".join(
        grid[-1][col] for col in col_indices if col < len(grid[-1])
    ).strip()

    return last_row_text if last_row_text in [OPERATOR_ADD, OPERATOR_MULTIPLY] else None


def parse_row_numbers(grid: list[str], col_indices: list[int]) -> list[int]:
    numbers = []
    for row_idx in range(len(grid) - 1):
        row_text = "".join(
            grid[row_idx][col] for col in col_indices if col < len(grid[row_idx])
        ).strip()

        if DEBUG:
            print(f"    Row {row_idx}: '{row_text}'")

        if row_text:
            try:
                num = int(row_text)
                numbers.append(num)
                if DEBUG:
                    print(f"      -> Number: {num}")
            except ValueError:
                if DEBUG:
                    print("      -> Not a valid number, skipping")

    return numbers


def solve_problem_part1(grid: list[str], col_indices: list[int]) -> int:
    if DEBUG:
        print(f"\n  Solving problem with columns {col_indices}")

    operator = extract_operator(grid, col_indices)
    if DEBUG and operator:
        print(f"    Operator from last row: {operator}")

    numbers = parse_row_numbers(grid, col_indices)

    result = calculate_result(numbers, operator)
    if DEBUG:
        print(f"    Result: {numbers} {operator} = {result}")

    return result


def parse_column_numbers(grid: list[str], col_indices: list[int]) -> list[int]:
    numbers = []
    for col in reversed(col_indices):
        # Read column top-to-bottom (excluding operator row)
        col_chars = [
            grid[row_idx][col]
            for row_idx in range(len(grid) - 1)
            if col < len(grid[row_idx])
        ]

        col_text = "".join(col_chars).strip()

        if DEBUG:
            print(f"    Column {col}: '{col_text}'")

        if col_text:
            try:
                num = int(col_text)
                numbers.append(num)
                if DEBUG:
                    print(f"      -> Number: {num}")
            except ValueError:
                if DEBUG:
                    print("      -> Not a valid number, skipping")

    return numbers


def solve_problem_part2(grid: list[str], col_indices: list[int]) -> int:
    if DEBUG:
        print(f"\n  Solving problem (Part 2) with columns {col_indices}")

    operator = extract_operator(grid, col_indices)
    if DEBUG and operator:
        print(f"    Operator from last row: {operator}")

    numbers = parse_column_numbers(grid, col_indices)

    result = calculate_result(numbers, operator)
    if DEBUG:
        print(f"    Result: {numbers} {operator} = {result}")

    return result


def calculate_result(numbers: list[int], operator: str | None) -> int:
    if not numbers or not operator:
        return 0

    result = numbers[0]
    for num in numbers[1:]:
        if operator == OPERATOR_ADD:
            result += num
        elif operator == OPERATOR_MULTIPLY:
            result *= num

    return result


def solve_first(file_name: str) -> int:
    lines = read_input(file_name)
    grid, problems = parse_worksheet(lines)

    total = 0
    for problem_cols in problems:
        result = solve_problem_part1(grid, problem_cols)
        total += result

    return total


def solve_second(file_name: str) -> int:
    lines = read_input(file_name)
    grid, problems = parse_worksheet(lines)

    total = 0
    for problem_cols in problems:
        result = solve_problem_part2(grid, problem_cols)
        total += result

    return total
