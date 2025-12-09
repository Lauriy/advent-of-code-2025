import os
from pathlib import Path

DEBUG = os.getenv("DEBUG", "").lower() in ("1", "true", "yes")

OUTSIDE = "!"
INSIDE = "."
MARKER = "0"


def read_input(filename: str) -> list[tuple[int, int]]:
    with Path(filename).open() as f:
        tiles = []
        for line_raw in f:
            line = line_raw.strip()
            if line:
                x, y = map(int, line.split(","))
                tiles.append((x, y))

    if DEBUG:
        print(f"Parsed {len(tiles)} red tiles: {tiles}\n")

    return tiles


def calculate_rectangle_area(
    pos1: tuple[int, int], pos2: tuple[int, int]
) -> int | None:
    x1, y1 = pos1
    x2, y2 = pos2

    # Check if they can be opposite corners (must have different x AND y)
    if x1 == x2 or y1 == y2:
        return None

    width = abs(x2 - x1) + 1
    height = abs(y2 - y1) + 1
    area = width * height

    if DEBUG:
        print(f"  Rectangle from {pos1} to {pos2}: {width}x{height} = {area}")

    return area


def solve_first(file_name: str) -> int:
    tiles = read_input(file_name)
    max_area = 0
    best_corners = None

    if DEBUG:
        print("Checking all pairs of red tiles:\n")

    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            area = calculate_rectangle_area(tiles[i], tiles[j])
            if area is not None and area > max_area:
                max_area = area
                best_corners = (tiles[i], tiles[j])

    if DEBUG:
        if best_corners:
            print(f"\nLargest rectangle: {best_corners[0]} to {best_corners[1]}")
        print(f"Maximum area: {max_area}")

    return max_area


def get_line_tiles(
    start: tuple[int, int], end: tuple[int, int]
) -> set[tuple[int, int]]:
    x1, y1 = start
    x2, y2 = end
    tiles = set()

    # Horizontal or vertical line
    if x1 == x2:
        # Vertical line
        for y in range(min(y1, y2), max(y1, y2) + 1):
            tiles.add((x1, y))
    elif y1 == y2:
        # Horizontal line
        for x in range(min(x1, x2), max(x1, x2) + 1):
            tiles.add((x, y1))

    return tiles


def point_in_polygon(point: tuple[int, int], polygon: list[tuple[int, int]]) -> bool:
    x, y = point
    n = len(polygon)
    inside = False

    # Walk through each edge of the polygon
    p1x, p1y = polygon[0]
    for i in range(1, n + 1):
        p2x, p2y = polygon[i % n]

        # Check if the horizontal ray at height y could intersect this edge
        # 1. Point's y must be within edge's y range (exclusive min, inclusive max)
        # 2. Point must be to the left of (or on) the rightmost edge vertex
        # 3. Edge must not be horizontal (p1y != p2y)
        if min(p1y, p2y) < y <= max(p1y, p2y) and x <= max(p1x, p2x) and p1y != p2y:
            # Calculate x-coordinate where the ray intersects this edge
            # Using linear interpolation: x = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x

            # If edge is vertical OR intersection is to the right of point, count it
            if p1x == p2x or x <= xinters:
                inside = not inside

        # Move to next edge
        p1x, p1y = p2x, p2y

    return inside


def build_edge_green_tiles(red_tiles: list[tuple[int, int]]) -> set[tuple[int, int]]:
    green_tiles = set()

    for i in range(len(red_tiles)):
        start = red_tiles[i]
        end = red_tiles[(i + 1) % len(red_tiles)]  # Wrap to first tile
        line_tiles = get_line_tiles(start, end)
        green_tiles.update(line_tiles)

    # Remove red tiles from green (they're on the edges but should stay red)
    green_tiles -= set(red_tiles)

    if DEBUG:
        print(f"Built {len(green_tiles)} edge green tiles")

    return green_tiles


def is_tile_valid(
    pos: tuple[int, int],
    red_tiles: set[tuple[int, int]],
    edge_green_tiles: set[tuple[int, int]],
    red_tiles_list: list[tuple[int, int]],
) -> bool:
    if pos in red_tiles or pos in edge_green_tiles:
        return True

    return point_in_polygon(pos, red_tiles_list)


def is_valid_rectangle(
    pos1: tuple[int, int],
    pos2: tuple[int, int],
    red_tiles: set[tuple[int, int]],
    edge_green_tiles: set[tuple[int, int]],
    red_tiles_list: list[tuple[int, int]],
) -> bool:
    x1, y1 = pos1
    x2, y2 = pos2

    min_x, max_x = min(x1, x2), max(x1, x2)
    min_y, max_y = min(y1, y2), max(y1, y2)

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            if not is_tile_valid((x, y), red_tiles, edge_green_tiles, red_tiles_list):
                return False

    return True


def compress_coordinates(
    tiles: list[tuple[int, int]],
) -> tuple[list[tuple[int, int, int, int]], dict[int, int], dict[int, int]]:
    # Get unique x and y values
    x_values = sorted({x for x, y in tiles})
    y_values = sorted({y for x, y in tiles})

    x_map = {x: i for i, x in enumerate(x_values)}
    y_map = {y: i for i, y in enumerate(y_values)}

    # Create compressed tiles with both original and compressed coords
    compressed = [(x, y, x_map[x], y_map[y]) for x, y in tiles]

    if DEBUG:
        print(f"Compressed {len(x_values)}x{len(y_values)} grid from large space")

    return compressed, x_map, y_map


def flood_fill_exterior(
    grid: list[list[str]], start_x: int, start_y: int, width: int, height: int
) -> None:
    stack = [(start_x, start_y)]

    while stack:
        x, y = stack.pop()
        if x < 0 or x >= width or y < 0 or y >= height:
            continue
        if grid[y][x] != INSIDE:
            continue

        grid[y][x] = OUTSIDE

        # Add neighbors
        stack.extend([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])


def build_compressed_grid(
    compressed_tiles: list[tuple[int, int, int, int]],
    width: int,
    height: int,
    padding: int,
) -> list[list[str]]:
    grid = [[INSIDE for _ in range(width)] for _ in range(height)]

    # Mark polygon edges (with offset for padding)
    for i in range(len(compressed_tiles)):
        _x1, _y1, cx1, cy1 = compressed_tiles[i]
        _x2, _y2, cx2, cy2 = compressed_tiles[(i + 1) % len(compressed_tiles)]

        min_cx, max_cx = min(cx1, cx2) + padding, max(cx1, cx2) + padding
        min_cy, max_cy = min(cy1, cy2) + padding, max(cy1, cy2) + padding

        for x in range(min_cx, max_cx + 1):
            for y in range(min_cy, max_cy + 1):
                grid[y][x] = MARKER

    return grid


def is_rectangle_valid_compressed(
    grid: list[list[str]],
    corner1: tuple[int, int],
    corner2: tuple[int, int],
    padding: int,
) -> bool:
    """Check if rectangle contains any exterior markers in compressed space."""
    cx1, cy1 = corner1
    cx2, cy2 = corner2
    min_cx = min(cx1, cx2) + padding
    max_cx = max(cx1, cx2) + padding
    min_cy = min(cy1, cy2) + padding
    max_cy = max(cy1, cy2) + padding

    for x in range(min_cx, max_cx + 1):
        for y in range(min_cy, max_cy + 1):
            if grid[y][x] == OUTSIDE:
                return False

    return True


def solve_second(file_name: str) -> int:
    tiles = read_input(file_name)

    compressed_tiles, x_map, y_map = compress_coordinates(tiles)

    # Grid dimensions with padding for exterior space
    padding = 1
    width = len(x_map) + 2 * padding
    height = len(y_map) + 2 * padding

    grid = build_compressed_grid(compressed_tiles, width, height, padding)
    flood_fill_exterior(grid, 0, 0, width, height)

    if DEBUG:
        exterior_count = sum(row.count(OUTSIDE) for row in grid)
        print(f"Marked {exterior_count} exterior tiles\n")

    max_area = 0
    best_corners = None

    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            area = calculate_rectangle_area(tiles[i], tiles[j])
            if area is None or area <= max_area:
                continue

            _, _, cx1, cy1 = compressed_tiles[i]
            _, _, cx2, cy2 = compressed_tiles[j]

            if is_rectangle_valid_compressed(grid, (cx1, cy1), (cx2, cy2), padding):
                max_area = area
                best_corners = (tiles[i], tiles[j])
                if DEBUG:
                    print(f"  Valid rectangle: {tiles[i]} to {tiles[j]} = {area}")

    if DEBUG:
        if best_corners:
            print(f"\nLargest valid rectangle: {best_corners[0]} to {best_corners[1]}")
        print(f"Maximum area: {max_area}")

    return max_area
