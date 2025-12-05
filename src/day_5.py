import os
from pathlib import Path

DEBUG = os.getenv("DEBUG", "").lower() in ("1", "true", "yes")


def read_input(filename: str) -> tuple[list[tuple[int, int]], list[int]]:
    with Path(filename).open() as f:
        lines = [line.strip() for line in f]

    separator_idx = lines.index("")

    ranges = []
    for line in lines[:separator_idx]:
        start, end = map(int, line.split("-"))
        ranges.append((start, end))

    ingredient_ids = [int(line) for line in lines[separator_idx + 1 :] if line]

    if DEBUG:
        print(f"Parsed {len(ranges)} ranges: {ranges}")
        print(f"Parsed {len(ingredient_ids)} ingredient IDs: {ingredient_ids}\n")

    return ranges, ingredient_ids


def is_fresh(ingredient_id: int, ranges: list[tuple[int, int]]) -> bool:
    return any(start <= ingredient_id <= end for start, end in ranges)


def solve_first(file_name: str) -> int:
    ranges, ingredient_ids = read_input(file_name)
    fresh_count = 0

    for ingredient_id in ingredient_ids:
        if is_fresh(ingredient_id, ranges):
            fresh_count += 1
            if DEBUG:
                print(f"Ingredient ID {ingredient_id}: FRESH")
        elif DEBUG:
            print(f"Ingredient ID {ingredient_id}: spoiled")

    if DEBUG:
        print(f"\nTotal fresh ingredients: {fresh_count}")

    return fresh_count


def merge_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    if not ranges:
        return []

    sorted_ranges = sorted(ranges)

    merged = [sorted_ranges[0]]

    for start, end in sorted_ranges[1:]:
        last_start, last_end = merged[-1]

        if start <= last_end + 1:
            # Merge by extending the last range
            merged[-1] = (last_start, max(last_end, end))
        else:
            # No overlap, add as new range
            merged.append((start, end))

    if DEBUG:
        print(f"Original ranges: {sorted_ranges}")
        print(f"Merged ranges: {merged}")

    return merged


def solve_second(file_name: str) -> int:
    ranges, _ = read_input(file_name)

    merged_ranges = merge_ranges(ranges)

    total_ids = 0
    for start, end in merged_ranges:
        count = end - start + 1
        total_ids += count
        if DEBUG:
            print(f"Range {start}-{end}: {count} IDs")

    if DEBUG:
        print(f"\nTotal fresh ingredient IDs: {total_ids}")

    return total_ids
