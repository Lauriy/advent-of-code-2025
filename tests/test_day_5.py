from src.day_5 import solve_first
from src.day_5 import solve_second


def test_solve_first_example() -> None:
    result = solve_first("input/day_5_example.txt")
    print(f"Day 5 Part 1 example answer: {result}")
    assert result == 3


def test_solve_first() -> None:
    result = solve_first("input/day_5.txt")
    print(f"Day 5 Part 1 answer: {result}")
    assert result == 773


def test_solve_second_example() -> None:
    result = solve_second("input/day_5_example.txt")
    print(f"Day 5 Part 2 example answer: {result}")
    assert result == 14


def test_solve_second() -> None:
    result = solve_second("input/day_5.txt")
    print(f"Day 5 Part 2 answer: {result}")
    assert result == 332067203034711
