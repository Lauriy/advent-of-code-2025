from pathlib import Path

START_NODE_P1 = "you"
END_NODE_P1 = "out"
START_NODE_P2 = "svr"
END_NODE_P2 = "out"
WAYPOINT_DAC = "dac"
WAYPOINT_FFT = "fft"


def read_input(filename: str) -> dict[str, list[str]]:
    graph: dict[str, list[str]] = {}
    with Path(filename).open() as f:
        for line in f:
            stripped_line = line.strip()
            if not stripped_line:
                continue
            device, outputs = stripped_line.split(": ")
            graph[device] = outputs.split()

    return graph


def count_paths_memoized(
    graph: dict[str, list[str]], current: str, target: str, memo: dict[str, int]
) -> int:
    if current == target:
        return 1
    if current in memo:
        return memo[current]
    if current not in graph:
        return 0

    total_paths = sum(
        count_paths_memoized(graph, neighbor, target, memo)
        for neighbor in graph[current]
    )
    memo[current] = total_paths

    return total_paths


def solve_first(file_name: str) -> int:
    graph = read_input(file_name)

    return count_paths_memoized(graph, START_NODE_P1, END_NODE_P1, {})


def count_paths_with_waypoints_unordered(
    graph: dict[str, list[str]],
    current: str,
    waypoints_to_visit: frozenset[str],
    memo: dict[tuple[str, frozenset[str]], int],
) -> int:
    state = (current, waypoints_to_visit)
    if state in memo:
        return memo[state]

    remaining_waypoints = waypoints_to_visit - {current}

    if current == END_NODE_P2:
        return 1 if not remaining_waypoints else 0

    count = 0
    if current in graph:
        for neighbor in graph[current]:
            count += count_paths_with_waypoints_unordered(
                graph, neighbor, remaining_waypoints, memo
            )

    memo[state] = count

    return count


def solve_second(file_name: str) -> int:
    graph = read_input(file_name)

    return count_paths_with_waypoints_unordered(
        graph, START_NODE_P2, frozenset([WAYPOINT_DAC, WAYPOINT_FFT]), {}
    )
