import os
from pathlib import Path

DEBUG = os.getenv("DEBUG", "").lower() in ("1", "true", "yes")
DEBUG_LIMIT = 10  # Number of connections to show in debug output


def read_input(filename: str) -> list[str]:
    with Path(filename).open() as file:
        return [line.rstrip("\n") for line in file]


def parse_coordinates(lines: list[str]) -> list[tuple[int, int, int]]:
    coords = []
    for line in lines:
        if line.strip():
            x, y, z = map(int, line.split(","))
            coords.append((x, y, z))

    return coords


def distance_squared(p1: tuple[int, int, int], p2: tuple[int, int, int]) -> int:
    return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2


class UnionFind:
    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])

        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False

        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1

        return True

    def get_component_sizes(self) -> list[int]:
        component_counts = {}
        for i in range(len(self.parent)):
            root = self.find(i)
            component_counts[root] = component_counts.get(root, 0) + 1

        return list(component_counts.values())


def solve_circuits(coords: list[tuple[int, int, int]], num_connections: int) -> int:
    n = len(coords)

    # Calculate all pairwise distances
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            dist_sq = distance_squared(coords[i], coords[j])
            edges.append((dist_sq, i, j))

    edges.sort()

    if DEBUG:
        print(f"Total junction boxes: {n}")
        print(f"Total possible connections: {len(edges)}")
        print(f"Making {num_connections} connections")

    # Use Union-Find to connect shortest edges
    uf = UnionFind(n)

    for attempt_num, (_dist_sq, i, j) in enumerate(edges[:num_connections], 1):
        connected = uf.union(i, j)

        if DEBUG and attempt_num <= DEBUG_LIMIT:
            status = "connected" if connected else "already in same circuit"
            print(f"Attempt {attempt_num}: {coords[i]} - {coords[j]} ({status})")

    circuit_sizes = uf.get_component_sizes()
    circuit_sizes.sort(reverse=True)

    if DEBUG:
        print(f"\nTotal circuits: {len(circuit_sizes)}")
        print(f"Circuit sizes (sorted): {circuit_sizes[:10]}")
        print(f"Three largest: {circuit_sizes[:3]}")

    return circuit_sizes[0] * circuit_sizes[1] * circuit_sizes[2]


def solve_first(file_name: str) -> int:
    lines = read_input(file_name)
    coords = parse_coordinates(lines)

    num_connections = 10 if "example" in file_name else 1000

    return solve_circuits(coords, num_connections)


def solve_all_connected(coords: list[tuple[int, int, int]]) -> int:
    n = len(coords)

    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            dist_sq = distance_squared(coords[i], coords[j])
            edges.append((dist_sq, i, j))

    edges.sort()

    if DEBUG:
        print(f"Total junction boxes: {n}")
        print("Connecting until all in one circuit...")

    uf = UnionFind(n)
    last_connected_pair = None
    connections_made = 0

    for _dist_sq, i, j in edges:
        if uf.union(i, j):
            connections_made += 1
            last_connected_pair = (i, j)

            num_components = len({uf.find(k) for k in range(n)})
            if num_components == 1:
                if DEBUG:
                    print(f"All connected after {connections_made} connections")
                    print(f"Last connection: {coords[i]} - {coords[j]}")
                    print(f"X coordinates: {coords[i][0]} * {coords[j][0]}")
                break

    if last_connected_pair:
        i, j = last_connected_pair

        return coords[i][0] * coords[j][0]

    return 0


def solve_second(file_name: str) -> int:
    lines = read_input(file_name)
    coords = parse_coordinates(lines)

    return solve_all_connected(coords)
