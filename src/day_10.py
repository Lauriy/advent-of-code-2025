import os
import re
from pathlib import Path

DEBUG = os.environ.get("DEBUG") == "1"
EPS = 1e-9
LIGHT_ON = 1
LIGHT_OFF = 0


def read_input(
    filename: str,
) -> list[tuple[list[int], list[list[int]], list[int]]]:
    machines = []

    with Path(filename).open() as f:
        for line_raw in f:
            line = line_raw.strip()
            if not line:
                continue

            lights_match = re.search(r"\[([.#]+)\]", line)
            if not lights_match:
                continue

            lights_str = lights_match.group(1)
            target = [LIGHT_ON if c == "#" else LIGHT_OFF for c in lights_str]

            buttons = [
                [int(x) for x in button_match.group(1).split(",")]
                for button_match in re.finditer(r"\(([0-9,]+)\)", line)
            ]

            joltages = []
            joltage_match = re.search(r"\{([0-9,]+)\}", line)
            if joltage_match:
                joltage_str = joltage_match.group(1)
                joltages = [int(x) for x in joltage_str.split(",")]

            machines.append((target, buttons, joltages))

            if DEBUG:
                print(
                    f"Machine: target={target}, buttons={buttons}, joltages={joltages}"
                )

    return machines


def _gauss_elimination_gf2(
    matrix: list[list[int]], num_buttons: int, num_lights: int
) -> tuple[list[list[int]], list[int]]:
    pivot_row = 0
    pivot_cols = []
    for col_idx in range(num_buttons):
        found_pivot = False
        for row_idx in range(pivot_row, num_lights):
            if matrix[row_idx][col_idx] == 1:
                matrix[pivot_row], matrix[row_idx] = matrix[row_idx], matrix[pivot_row]
                found_pivot = True
                break
        if not found_pivot:
            continue
        pivot_cols.append(col_idx)
        for row_idx in range(num_lights):
            if row_idx != pivot_row and matrix[row_idx][col_idx] == 1:
                for c in range(num_buttons + 1):
                    matrix[row_idx][c] ^= matrix[pivot_row][c]
        pivot_row += 1
        if pivot_row >= num_lights:
            break

    return matrix, pivot_cols


def _find_best_solution_gf2(
    matrix: list[list[int]],
    num_buttons: int,
    free_vars: list[int],
    pivot_cols: list[int],
) -> int:
    min_presses = float("inf")
    best_solution = None

    for mask in range(1 << len(free_vars)):
        solution = [0] * num_buttons
        for i, var_idx in enumerate(free_vars):
            solution[var_idx] = (mask >> i) & 1
        for row_idx, col_idx in enumerate(pivot_cols):
            val = matrix[row_idx][-1]
            for c in range(num_buttons):
                if c != col_idx and matrix[row_idx][c] == 1:
                    val ^= solution[c]
            solution[col_idx] = val
        presses = sum(solution)
        if presses < min_presses:
            min_presses = presses
            best_solution = solution

    if DEBUG:
        print(f"Best solution: {best_solution}, presses: {min_presses}")

    return min_presses


def _build_gf2_matrix(
    target: list[int], buttons: list[list[int]], num_lights: int
) -> list[list[int]]:
    return [
        [1 if light_idx in button else 0 for button in buttons] + [target[light_idx]]
        for light_idx in range(num_lights)
    ]


def _check_gf2_inconsistency(matrix: list[list[int]], num_buttons: int) -> bool:
    for row in matrix:
        if all(row[i] == 0 for i in range(num_buttons)) and row[-1] == 1:
            return True

    return False


def _extract_unique_solution_gf2(
    pivot_cols: list[int], matrix: list[list[int]], num_buttons: int
) -> int:
    solution = [0] * num_buttons
    for row_idx, col_idx in enumerate(pivot_cols):
        solution[col_idx] = matrix[row_idx][-1]

    return sum(solution)


def solve_lights_gf2(target: list[int], buttons: list[list[int]]) -> int:
    num_lights = len(target)
    num_buttons = len(buttons)

    if DEBUG:
        print(f"\nSolving: {num_lights} lights, {num_buttons} buttons")
        print(f"Target: {target}")

    matrix = _build_gf2_matrix(target, buttons, num_lights)

    if DEBUG:
        print("Initial matrix:")
        for row in matrix:
            print(row)

    matrix, pivot_cols = _gauss_elimination_gf2(matrix, num_buttons, num_lights)

    if DEBUG:
        print("RREF matrix:")
        for row in matrix:
            print(row)

    if _check_gf2_inconsistency(matrix, num_buttons):
        if DEBUG:
            print("No solution exists!")

        return float("inf")

    free_vars = [i for i in range(num_buttons) if i not in pivot_cols]

    if DEBUG:
        print(f"Pivot columns (basic vars): {pivot_cols}")
        print(f"Free variables: {free_vars}")

    if not free_vars:
        return _extract_unique_solution_gf2(pivot_cols, matrix, num_buttons)

    return _find_best_solution_gf2(matrix, num_buttons, free_vars, pivot_cols)


def solve_first(file_name: str) -> int:
    machines = read_input(file_name)
    total_presses = 0

    for target, buttons, _joltages in machines:
        presses = solve_lights_gf2(target, buttons)
        if presses != float("inf"):
            total_presses += presses

    if DEBUG:
        print(f"\nTotal presses: {total_presses}")

    return total_presses


def solve_second(file_name: str) -> int:
    machines = read_input(file_name)
    total_presses = 0

    for _target, buttons, joltages in machines:
        presses = solve_joltage(joltages, buttons)
        total_presses += presses

    if DEBUG:
        print(f"\nTotal joltage presses: {total_presses}")

    return total_presses


def _create_joltage_matrix(
    joltage: list[int], buttons: list[list[int]], num_counters: int
) -> list[list[float]]:
    return [
        [(1.0 if i in btn else 0.0) for btn in buttons] + [float(joltage[i])]
        for i in range(num_counters)
    ]


def _back_substitute(
    num_buttons: int,
    pivot_map: dict[int, int],
    matrix: list[list[float]],
    free_vars_map: dict[int, float],
) -> list[float]:
    solution = [0.0] * num_buttons
    for free_var_idx, value in free_vars_map.items():
        solution[free_var_idx] = value
    for pivot_col in sorted(pivot_map.keys(), key=lambda x: pivot_map[x], reverse=True):
        pivot_row_idx = pivot_map[pivot_col]
        solution[pivot_col] = matrix[pivot_row_idx][num_buttons] - sum(
            matrix[pivot_row_idx][col_idx] * solution[col_idx]
            for col_idx in range(num_buttons)
            if col_idx != pivot_col
        )

    return solution


def _is_valid_solution(solution: list[float]) -> bool:
    return all(x >= -EPS and abs(x - round(x)) < EPS for x in solution)


def _total_presses(solution: list[float]) -> int:
    return sum(round(x) for x in solution)


def _recursive_search(
    free_vars: list[int],
    matrix_data: tuple[list[list[float]], dict[int, int], list[int], int],
    joltage: list[int],
) -> int:
    """Perform a recursive search to find the optimal solution.

    Args:
        free_vars: List of free variable indices
        matrix_data: Tuple of (matrix, pivot_map, pivots, num_buttons)
        joltage: List of joltage values
    """
    matrix, pivot_map, pivots, num_buttons = matrix_data
    num_free_vars = len(free_vars)
    max_joltage, sum_joltage = max(joltage) if joltage else 0, sum(joltage)
    memo_feasible: dict[tuple[int, tuple[int, ...]], bool] = {}

    def feasible(free_var_idx: int, free_var_values_tuple: tuple[int, ...]) -> bool:
        state = (free_var_idx, free_var_values_tuple)
        if state in memo_feasible:
            return memo_feasible[state]

        free_var_values = list(free_var_values_tuple)
        res = all(
            (
                matrix[pivot_row_idx][num_buttons]
                - sum(
                    matrix[pivot_row_idx][free_vars[k]] * float(free_var_values[k])
                    for k in range(free_var_idx)
                )
            )
            >= -EPS
            or any(
                matrix[pivot_row_idx][free_vars[k]] < -EPS
                for k in range(free_var_idx, num_free_vars)
            )
            for pivot_row_idx in range(len(pivots))
        )
        memo_feasible[state] = res

        return res

    best = float("inf")
    stack = [(0, [0] * num_free_vars, 0)]  # (index, values, current_sum)

    while stack:
        i, v, s = stack.pop(0)

        if s >= best or s > sum_joltage or not feasible(i, tuple(v)):
            continue

        if i == num_free_vars:
            fm = {fv: float(val) for fv, val in zip(free_vars, v, strict=True)}
            sol = _back_substitute(num_buttons, pivot_map, matrix, fm)
            if _is_valid_solution(sol):
                best = min(best, _total_presses(sol))
            continue

        for x in range(min(max_joltage, sum_joltage - s), -1, -1):
            v[i] = x
            stack.insert(0, (i + 1, v[:], s + x))

    return best


def solve_joltage(joltage: list[int], buttons: list[list[int]]) -> int:
    num_counters, num_buttons = len(joltage), len(buttons)
    mat = _create_joltage_matrix(joltage, buttons, num_counters)
    pivots, mat = gauss_real(num_counters, num_buttons, mat)
    free = free_vars(num_buttons, pivots)
    n_free = len(free)
    p_map = {p: i for i, p in enumerate(pivots)}

    if n_free == 0:
        sol = _back_substitute(num_buttons, p_map, mat, {})

        return _total_presses(sol) if _is_valid_solution(sol) else float("inf")

    return _recursive_search(free, (mat, p_map, pivots, num_buttons), joltage)


def gauss_real(
    num_rows: int, num_cols: int, matrix: list[list[float]]
) -> tuple[list[int], list[list[float]]]:
    pivots = []
    pivot_row = 0
    for col_idx in range(num_cols):
        if pivot_row >= num_rows:
            break
        best = max(range(pivot_row, num_rows), key=lambda r: abs(matrix[r][col_idx]))
        matrix[pivot_row], matrix[best] = matrix[best], matrix[pivot_row]
        if abs(matrix[pivot_row][col_idx]) <= EPS:
            continue

        pivot_val = matrix[pivot_row][col_idx]
        for j in range(col_idx, num_cols + 1):
            matrix[pivot_row][j] /= pivot_val

        for row_idx in range(num_rows):
            if row_idx != pivot_row:
                factor = matrix[row_idx][col_idx]
                for j in range(col_idx, num_cols + 1):
                    matrix[row_idx][j] -= factor * matrix[pivot_row][j]
        pivots.append(col_idx)
        pivot_row += 1

    return pivots, matrix


def free_vars(num_buttons: int, pivots: list[int]) -> list[int]:
    return sorted(set(range(num_buttons)) - set(pivots))
