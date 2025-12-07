from src.day_7 import solve_first
from src.day_7 import solve_second


def test_solve_first_example() -> None:
    result = solve_first("input/day_7_example.txt")
    print(f"Day 7 Part 1 example answer: {result}")
    assert result == 21


def test_solve_first() -> None:
    result = solve_first("input/day_7.txt")
    print(f"Day 7 Part 1 answer: {result}")
    assert result == 1622


def test_solve_second_example() -> None:
    result = solve_second("input/day_7_example.txt")
    print(f"Day 7 Part 2 example answer: {result}")
    assert result == 40


def test_solve_second() -> None:
    result = solve_second("input/day_7.txt")
    print(f"Day 7 Part 2 answer: {result}")
    assert result == 10357305916520
