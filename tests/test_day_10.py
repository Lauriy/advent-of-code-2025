from src.day_10 import solve_first
from src.day_10 import solve_second


def test_solve_first_example() -> None:
    result = solve_first("input/day_10_example.txt")
    print(f"Day 10 Part 1 example answer: {result}")
    assert result == 7


def test_solve_first() -> None:
    result = solve_first("input/day_10.txt")
    print(f"Day 10 Part 1 answer: {result}")
    assert result == 535


def test_solve_second_example() -> None:
    result = solve_second("input/day_10_example.txt")
    print(f"Day 10 Part 2 example answer: {result}")
    assert result == 33


def test_solve_second() -> None:
    result = solve_second("input/day_10.txt")
    print(f"Day 10 Part 2 answer: {result}")
    assert result > 17373
    assert result > 20995
    assert result > 21007
    assert result != 21008
    assert result != 21010
    assert result != 21013
    assert result == 21021
