# BattleShip Bot

BattleShip Bot is a graphical simulation of a Battleship-like game where different types of ships can be placed and moved on a grid. This project is built for the CMU 112 class, utilizing the `cmu_112_graphics` library.

## Features

- Multiple ship types with unique attributes
- Grid-based movement system
- Collision avoidance: ships have defined outlines preventing them from overlapping with other ships
- Interactive graphical interface powered by the `cmu_112_graphics` library

## Requirements

- Python 3.x
- `cmu_112_graphics` library (installation instructions below)

### Installing `cmu_112_graphics`

To install the `cmu_112_graphics` package, run the following command:

```
pip install cmu-112-graphics
```

## How to Run

1. Clone the repository or download the code.
2. Ensure that all dependencies are installed (`cmu_112_graphics`).
3. Run the Python script:

```
python GUI.py
```

## File Overview

- **GUI.py**: Main script that implements the ship objects and graphical interface, handling ship movement, grid management, and collision logic.

## Class Overview

- **ship**: A class representing a ship, including its coordinates, outline, and type. The class contains methods for moving the ship, retrieving its coordinates, and ensuring collision boundaries are respected.

## Future Enhancements

- Add more ship types with unique movement patterns.
- Implement AI-controlled ships to play against.
- Expand the game grid and include obstacles or special terrain.
