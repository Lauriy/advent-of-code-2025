# AoC 2025

# Setup
```shell
uv venv
uv sync --dev
source .venv/bin/activate  # . .\.venv\Scripts\activate on Windows
```

# Tests (get answers)

```shell
DEBUG=1 uv run pytest
```

# Linting
```shell
ruff check --fix --unsafe-fixes .
ruff format .
```

# Previous years

- https://github.com/Lauriy/advent-of-code-2018
- https://github.com/Lauriy/advent-of-code-2020
- https://github.com/Lauriy/advent-of-code-2021
- https://github.com/Lauriy/advent-of-code-2022
- https://github.com/Lauriy/advent-of-code-2024