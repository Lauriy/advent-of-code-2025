from src.day_2 import solve_first
from src.day_2 import solve_second


def test_solve_first_example() -> None:
    result = solve_first("input/day_2_example.txt")
    print(f"Day 2 Part 1 example answer: {result}")
    assert result == 1227775554


def test_solve_first() -> None:
    result = solve_first("input/day_2.txt")
    print(f"Day 2 Part 1 answer: {result}")
    assert result == 40055209690


def test_solve_second_example() -> None:
    result = solve_second("input/day_2_example.txt")
    print(f"Day 2 Part 2 example answer: {result}")
    assert result == 4174379265


def test_solve_second() -> None:
    result = solve_second("input/day_2.txt")
    print(f"Day 2 Part 2 answer: {result}")
    assert result == 50857215650
