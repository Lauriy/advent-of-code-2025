import os
from pathlib import Path

DEBUG = os.getenv("DEBUG", "").lower() in ("1", "true", "yes")


def read_input(filename: str) -> list[str]:
    with Path(filename).open() as f:
        return [line.strip() for line in f if line.strip()]


def find_max_joltage(bank: str) -> int:
    max_joltage = 0
    best_positions = (0, 0)

    for i in range(len(bank)):
        for j in range(i + 1, len(bank)):
            joltage = int(bank[i] + bank[j])
            if joltage > max_joltage:
                max_joltage = joltage
                best_positions = (i, j)

    if DEBUG:
        i, j = best_positions
        print(f"  Max joltage: {max_joltage} (positions {i},{j}: {bank[i]}{bank[j]})")

    return max_joltage


def solve_first(file_name: str) -> int:
    banks = read_input(file_name)
    total = 0

    if DEBUG:
        print(f"Processing {len(banks)} banks\n")

    for bank in banks:
        if DEBUG:
            print(f"Bank: {bank}")

        max_joltage = find_max_joltage(bank)
        total += max_joltage

        if DEBUG:
            print(f"Running total: {total}\n")

    if DEBUG:
        print(f"Total output joltage: {total}")

    return total


def find_max_joltage_n_batteries(bank: str, n: int) -> int:
    bank_len = len(bank)
    if n > bank_len:
        msg = f"Cannot select {n} batteries from bank of length {bank_len}"  # noqa: S608
        raise ValueError(msg)

    selected_positions = []
    start_pos = 0

    for result_pos in range(n):
        remaining_needed = n - result_pos - 1

        max_end_pos = bank_len - remaining_needed

        best_digit = -1
        best_pos = start_pos

        for pos in range(start_pos, max_end_pos):
            digit = int(bank[pos])
            if digit > best_digit:
                best_digit = digit
                best_pos = pos

        selected_positions.append(best_pos)
        start_pos = best_pos + 1

    result_str = "".join(bank[pos] for pos in selected_positions)
    result = int(result_str)

    if DEBUG:
        print(f"  Selected positions: {selected_positions}")
        print(f"  Result: {result_str}")

    return result


def solve_second(file_name: str) -> int:
    banks = read_input(file_name)
    total = 0

    if DEBUG:
        print(f"Processing {len(banks)} banks (selecting 12 batteries each)\n")

    for bank in banks:
        if DEBUG:
            print(f"Bank: {bank}")

        max_joltage = find_max_joltage_n_batteries(bank, 12)
        total += max_joltage

        if DEBUG:
            print(f"Running total: {total}\n")

    if DEBUG:
        print(f"Total output joltage: {total}")

    return total
