from pathlib import Path

FILLED_CHAR = "#"
EMPTY_CELL = 0
PARITY_EVEN = 0
MAX_ITERATIONS_BASE = 10000
MAX_ITERATIONS_CAP = 500000
SHAPE_DELIMITER = ":"
REGION_DELIMITER = "x"


def parse_input(
    filename: str,
) -> tuple[list[set[tuple[int, int]]], list[tuple[int, int, list[int]]]]:
    with Path(filename).open() as f:
        lines = [line.rstrip("\n") for line in f]

    shapes: list[set[tuple[int, int]]] = []
    regions: list[tuple[int, int, list[int]]] = []

    i = 0
    while i < len(lines):
        line = lines[i]

        if line and SHAPE_DELIMITER in line and REGION_DELIMITER not in line:
            shape_lines = []
            i += 1
            while (
                i < len(lines)
                and lines[i]
                and REGION_DELIMITER not in lines[i]
                and SHAPE_DELIMITER not in lines[i]
            ):
                shape_lines.append(lines[i])
                i += 1

            coords = set()
            for r, row in enumerate(shape_lines):
                for c, ch in enumerate(row):
                    if ch == FILLED_CHAR:
                        coords.add((r, c))
            shapes.append(coords)

        elif line and REGION_DELIMITER in line:
            parts = line.split(f"{SHAPE_DELIMITER} ")
            dims = parts[0].split(REGION_DELIMITER)
            width, height = int(dims[0]), int(dims[1])
            quantities = list(map(int, parts[1].split()))
            regions.append((width, height, quantities))
            i += 1
        else:
            i += 1

    return shapes, regions


def normalize_shape(shape: set[tuple[int, int]]) -> set[tuple[int, int]]:
    """Normalize shape to start at (0, 0)."""
    if not shape:
        return shape

    min_r = min(r for r, c in shape)
    min_c = min(c for r, c in shape)

    return {(r - min_r, c - min_c) for r, c in shape}


def rotate_90(shape: set[tuple[int, int]]) -> set[tuple[int, int]]:
    rotated = {(c, -r) for r, c in shape}

    return normalize_shape(rotated)


def flip_horizontal(shape: set[tuple[int, int]]) -> set[tuple[int, int]]:
    max_c = max(c for r, c in shape) if shape else 0
    flipped = {(r, max_c - c) for r, c in shape}

    return normalize_shape(flipped)


def get_orientations(shape: set[tuple[int, int]]) -> list[set[tuple[int, int]]]:
    """Get all unique rotations and flips of a shape."""
    orientations = []
    seen = set()

    for do_flip in [False, True]:
        current = normalize_shape(shape)
        if do_flip:
            current = flip_horizontal(current)

        for _ in range(4):
            frozen = frozenset(current)
            if frozen not in seen:
                seen.add(frozen)
                orientations.append(current)

            current = rotate_90(current)

    return orientations


def can_place(
    grid: list[list[int]], shape: set[tuple[int, int]], row: int, col: int
) -> bool:
    for dr, dc in shape:
        r, c = row + dr, col + dc
        if r < 0 or r >= len(grid) or c < 0 or c >= len(grid[0]):
            return False
        if grid[r][c] != EMPTY_CELL:
            return False

    return True


def place(
    grid: list[list[int]],
    shape: set[tuple[int, int]],
    row: int,
    col: int,
    label: int,
) -> None:
    for dr, dc in shape:
        r, c = row + dr, col + dc
        grid[r][c] = label


def unplace(
    grid: list[list[int]], shape: set[tuple[int, int]], row: int, col: int
) -> None:
    for dr, dc in shape:
        r, c = row + dr, col + dc
        grid[r][c] = EMPTY_CELL


def find_first_empty(grid: list[list[int]]) -> tuple[int, int] | None:
    """Find the first empty cell (top-left to bottom-right)."""
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == EMPTY_CELL:
                return row, col

    return None


def solve_region(
    width: int,
    height: int,
    presents: list[tuple[int, list[set[tuple[int, int]]]]],
    max_iterations: int = 50000,
) -> bool:
    """Try to fit all presents using backtracking with iteration limit."""
    total_area = sum(len(orientations[0]) for _, orientations in presents)
    if total_area > width * height:
        return False

    grid = [[EMPTY_CELL] * width for _ in range(height)]
    iterations = [0]

    def backtrack(present_idx: int) -> bool:
        iterations[0] += 1
        if iterations[0] > max_iterations:
            return False

        if present_idx == len(presents):
            return True

        _shape_id, orientations = presents[present_idx]

        for shape in orientations:
            for row in range(height):
                for col in range(width):
                    if can_place(grid, shape, row, col):
                        place(grid, shape, row, col, present_idx + 1)
                        if backtrack(present_idx + 1):
                            return True
                        unplace(grid, shape, row, col)

        return False

    return backtrack(0)


def get_parity(shape: set[tuple[int, int]]) -> tuple[int, int]:
    """Get (black_count, white_count) using checkerboard coloring.

    Cell (r, c) is black if (r + c) is even, white if odd.
    """
    black = sum(1 for r, c in shape if (r + c) % 2 == PARITY_EVEN)
    white = len(shape) - black

    return black, white


def solve_first(file_name: str) -> int:
    shapes, regions = parse_input(file_name)
    all_orientations = [get_orientations(shape) for shape in shapes]
    shape_parities = [get_parity(shape) for shape in shapes]

    count = 0
    for width, height, quantities in regions:
        total_area = sum(qty * len(shapes[i]) for i, qty in enumerate(quantities))
        region_area = width * height

        if total_area > region_area:
            continue

        total_black = sum(
            qty * shape_parities[i][0] for i, qty in enumerate(quantities)
        )
        total_white = sum(
            qty * shape_parities[i][1] for i, qty in enumerate(quantities)
        )

        region_black = sum(
            1 for r in range(height) for c in range(width) if (r + c) % 2 == PARITY_EVEN
        )
        region_white = region_area - region_black

        if total_black > region_black or total_white > region_white:
            continue

        presents = [
            (shape_id, all_orientations[shape_id])
            for shape_id, qty in enumerate(quantities)
            for _ in range(qty)
        ]
        presents.sort(key=lambda p: -len(p[1][0]))
        max_iter = min(MAX_ITERATIONS_CAP, MAX_ITERATIONS_BASE * len(presents))

        if solve_region(width, height, presents, max_iterations=max_iter):
            count += 1

    return count
