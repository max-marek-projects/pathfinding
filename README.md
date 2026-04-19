# Pathfinding Algorithm Visualizer

[![Python 3.14+](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

Interactive visualization of classic pathfinding algorithms – **Wave (Lee)** and **A\*** – built with **Matplotlib**.  
This project was created to explore the `matplotlib` library and compare different maze‑solving techniques.  
It includes a **randomized maze generator** and a clean GUI to set start/end points, change maze dimensions, and watch the algorithms in action.

## Features

- Random maze generation (recursive backtracker)
- Two pathfinding algorithms:
  - [Wave (Lee) algorithm](https://en.wikipedia.org/wiki/Lee_algorithm)
  - [A\* algorithm](https://en.wikipedia.org/wiki/A*_search_algorithm)
- Interactive GUI built with `matplotlib`:
  - Set start (green) and end (blue) points
  - Adjust maze rows/columns
  - Clear map or regenerate a new one
- Fully typed code with strict static type checking

## Technologies

- **Core**: Python 3.14+, Matplotlib
- **Code quality**:
  - `ruff` – linting, formatting, import sorting
  - `mypy`, `ty` – static type checking

## Getting Started

### Prerequisites

- `python 3.14` or higher
- `git`
- `uv`
- `make`

### Installation

Clone the repository:

```bash
git clone git@github.com:Starkiller2000Turbo/pathfinding.git
cd pathfinding
```

Install dependencies and create virtual environment:

```bash
make req
```

### Running the Visualiser

- **Wave algorithm**:

```bash
make run-wave
```

- **A\* algorithm**:

```bash
make run-a-star
```

## Code Style & Quality

Install style‑checking dependencies:

```bash
make req-style
```

Run all linters and type checker:

```bash
make lint
make lint-fix  # execute linting with autoformatting
```

## Author

- [max-marek](https://github.com/max-marek)

## License

This project is for educational purposes. Feel free to use and modify it under the [MIT license](LICENSE)
