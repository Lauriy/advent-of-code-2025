from src.day_3 import solve_first
from src.day_3 import solve_second


def test_solve_first_example() -> None:
    result = solve_first("input/day_3_example.txt")
    print(f"Day 3 Part 1 example answer: {result}")
    assert result == 357


def test_solve_first() -> None:
    result = solve_first("input/day_3.txt")
    print(f"Day 3 Part 1 answer: {result}")
    assert result == 17144


def test_solve_second_example() -> None:
    result = solve_second("input/day_3_example.txt")
    print(f"Day 3 Part 2 example answer: {result}")
    assert result == 3121910778619


def test_solve_second() -> None:
    result = solve_second("input/day_3.txt")
    print(f"Day 3 Part 2 answer: {result}")
    assert result == 170371185255900
