from src.day_4 import solve_first
from src.day_4 import solve_second


def test_solve_first_example() -> None:
    result = solve_first("input/day_4_example.txt")
    print(f"Day 4 Part 1 example answer: {result}")
    assert result == 13


def test_solve_first() -> None:
    result = solve_first("input/day_4.txt")
    print(f"Day 4 Part 1 answer: {result}")
    assert result == 1457


def test_solve_second_example() -> None:
    result = solve_second("input/day_4_example.txt")
    print(f"Day 4 Part 2 example answer: {result}")
    assert result == 43


def test_solve_second() -> None:
    result = solve_second("input/day_4.txt")
    print(f"Day 4 Part 2 answer: {result}")
    assert result == 8310
