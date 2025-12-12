from src.day_12 import solve_first


def test_solve_first_example() -> None:
    result = solve_first("input/day_12_example.txt")
    print(f"Day 12 Part 1 example answer: {result}")
    assert result == 2


def test_solve_first() -> None:
    result = solve_first("input/day_12.txt")
    print(f"Day 12 Part 1 answer: {result}")
    assert result == 555
