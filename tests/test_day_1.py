from src.day_1 import solve_first
from src.day_1 import solve_second


def test_solve_first_example() -> None:
    assert solve_first("input/day_1_example.txt") == 3


def test_solve_first() -> None:
    result = solve_first("input/day_1.txt")
    print(f"Day 1 Part 1 answer: {result}")
    assert result == 1154


def test_solve_second_example() -> None:
    assert solve_second("input/day_1_example.txt") == 6


def test_solve_second() -> None:
    result = solve_second("input/day_1.txt")
    print(f"Day 1 Part 2 answer: {result}")
    assert result == 6819
