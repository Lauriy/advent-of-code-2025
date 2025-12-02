import os
from pathlib import Path

DEBUG = os.getenv("DEBUG", "").lower() in ("1", "true", "yes")


def read_input(filename: str) -> list[tuple[int, int]]:
    with Path(filename).open() as f:
        line = f.read().strip()

    ranges = []
    for range_str in line.split(","):
        start, end = map(int, range_str.split("-"))
        ranges.append((start, end))

    if DEBUG:
        print(f"Parsed {len(ranges)} ranges")
        print(f"First few ranges: {ranges[:3]}")

    return ranges


def is_invalid_id(num: int) -> bool:
    s = str(num)
    length = len(s)

    # Must have even length to be split in half
    if length % 2 != 0:
        return False

    # Check if first half equals second half
    half = length // 2
    first_half = s[:half]
    second_half = s[half:]

    # No leading zeroes allowed (e.g., 0101 is not valid)
    if first_half[0] == "0":
        return False

    result = first_half == second_half

    if DEBUG and result:
        print(f"  Found invalid ID: {num} = {first_half} + {second_half}")

    return result


def solve_first(file_name: str) -> int:
    ranges = read_input(file_name)
    total = 0
    invalid_count = 0

    for start, end in ranges:
        if DEBUG:
            print(f"\nChecking range {start}-{end}")

        range_invalids = []
        for num in range(start, end + 1):
            if is_invalid_id(num):
                total += num
                invalid_count += 1
                range_invalids.append(num)

        if DEBUG and range_invalids:
            print(
                f"  Range {start}-{end} has "
                f"{len(range_invalids)} invalid IDs: {range_invalids}"
            )
        elif DEBUG:
            print(f"  Range {start}-{end} has no invalid IDs")

    if DEBUG:
        print(f"\nTotal invalid IDs found: {invalid_count}")
        print(f"Sum of all invalid IDs: {total}")

    return total


def is_invalid_id_v2(num: int) -> bool:
    s = str(num)
    length = len(s)

    # Try all possible pattern lengths from 1 to length//2
    # A pattern of length n can repeat at least twice if n <= length//2
    for pattern_len in range(1, length // 2 + 1):
        # Check if the entire string can be made by repeating the pattern
        pattern = s[:pattern_len]

        # No leading zeroes allowed
        if pattern[0] == "0":
            continue

        # Check if repeating this pattern gives us the full string
        # and that it repeats at least twice (length >= 2 * pattern_len)
        # Also verify it's exact repetition (no partial at the end)
        if (
            length >= 2 * pattern_len
            and length % pattern_len == 0
            and pattern * (length // pattern_len) == s
        ):
            repetitions = length // pattern_len
            if DEBUG:
                print(
                    f"  Found invalid ID: {num} = "
                    f"{pattern} repeated {repetitions} times"
                )

            return True

    return False


def solve_second(file_name: str) -> int:
    """Find and sum all invalid IDs using new rules (repeated at least twice)."""
    ranges = read_input(file_name)
    total = 0
    invalid_count = 0

    for start, end in ranges:
        if DEBUG:
            print(f"\nChecking range {start}-{end}")

        range_invalids = []
        for num in range(start, end + 1):
            if is_invalid_id_v2(num):
                total += num
                invalid_count += 1
                range_invalids.append(num)

        if DEBUG and range_invalids:
            print(
                f"  Range {start}-{end} has "
                f"{len(range_invalids)} invalid IDs: {range_invalids}"
            )
        elif DEBUG:
            print(f"  Range {start}-{end} has no invalid IDs")

    if DEBUG:
        print(f"\nTotal invalid IDs found: {invalid_count}")
        print(f"Sum of all invalid IDs: {total}")

    return total
