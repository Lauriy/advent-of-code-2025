from src.day_9 import solve_first
from src.day_9 import solve_second


def test_solve_first_example() -> None:
    result = solve_first("input/day_9_example.txt")
    print(f"Day 9 Part 1 example answer: {result}")
    assert result == 50


def test_solve_first() -> None:
    result = solve_first("input/day_9.txt")
    print(f"Day 9 Part 1 answer: {result}")


def test_solve_second_example() -> None:
    result = solve_second("input/day_9_example.txt")
    print(f"Day 9 Part 2 example answer: {result}")
    assert result == 24


def test_solve_second() -> None:
    result = solve_second("input/day_9.txt")
    print(f"Day 9 Part 2 answer: {result}")
    assert result == 1560475800
