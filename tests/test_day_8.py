from src.day_8 import solve_first
from src.day_8 import solve_second


def test_solve_first_example() -> None:
    result = solve_first("input/day_8_example.txt")
    print(f"Day 8 Part 1 example answer: {result}")
    assert result == 40


def test_solve_first() -> None:
    result = solve_first("input/day_8.txt")
    print(f"Day 8 Part 1 answer: {result}")
    assert result == 112230


def test_solve_second_example() -> None:
    result = solve_second("input/day_8_example.txt")
    print(f"Day 8 Part 2 example answer: {result}")
    assert result == 25272


def test_solve_second() -> None:
    result = solve_second("input/day_8.txt")
    print(f"Day 8 Part 2 answer: {result}")
    assert result == 2573952864
