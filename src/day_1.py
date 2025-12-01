from pathlib import Path

LEFT = "L"
RIGHT = "R"


def read_input(filename: str) -> list[str]:
    with Path(filename).open() as f:
        return [line.strip() for line in f]


def solve_first(file_name: str) -> int:
    rotations = read_input(file_name)
    position = 50
    zero_count = 0

    for rotation in rotations:
        direction = rotation[0]
        distance = int(rotation[1:])

        if direction == LEFT:
            position = (position - distance) % 100
        else:
            position = (position + distance) % 100

        if position == 0:
            zero_count += 1

    return zero_count


def solve_second(file_name: str) -> int:
    rotations = read_input(file_name)
    position = 50
    zero_count = 0

    for rotation in rotations:
        direction = rotation[0]
        distance = int(rotation[1:])

        if direction == RIGHT:
            zero_count += (position + distance) // 100 - position // 100
        # Moving left by 'distance' clicks from 'position'
        # We hit 0 when (position - k) mod 100 == 0 for k in [1, distance]
        # This happens at k = position, position+100, position+200, ...
        # BUT: if position == 0, we start at 0, so first hit is at k=100
        elif position == 0:
            zero_count += distance // 100
        elif distance >= position:
            zero_count += (distance - position) // 100 + 1

        # Update position
        position = (
            position + distance if direction == RIGHT else position - distance
        ) % 100

    return zero_count
