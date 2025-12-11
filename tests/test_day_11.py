from src.day_11 import solve_first
from src.day_11 import solve_second


def test_solve_first_example() -> None:
    result = solve_first("input/day_11_example.txt")
    assert result == 5


def test_solve_first() -> None:
    result = solve_first("input/day_11.txt")
    assert result == 523


def test_solve_second_example() -> None:
    result = solve_second("input/day_11_example_part2.txt")
    assert result == 2


def test_solve_second() -> None:
    result = solve_second("input/day_11.txt")
    assert result == 517315308154944
