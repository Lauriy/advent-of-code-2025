from src.day_6 import solve_first
from src.day_6 import solve_second


def test_solve_first_example() -> None:
    result = solve_first("input/day_6_example.txt")
    print(f"Day 6 Part 1 example answer: {result}")
    assert result == 4277556


def test_solve_first() -> None:
    result = solve_first("input/day_6.txt")
    print(f"Day 6 Part 1 answer: {result}")
    assert result == 6635273135233


def test_solve_second_example() -> None:
    result = solve_second("input/day_6_example.txt")
    print(f"Day 6 Part 2 example answer: {result}")
    assert result == 3263827


def test_solve_second() -> None:
    result = solve_second("input/day_6.txt")
    print(f"Day 6 Part 2 answer: {result}")
    assert result == 12542543681221
