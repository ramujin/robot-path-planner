# Robot Path Planner

A simple robot path planning library

## Description

## Setup

### Python

- Dependencies: Python3, matplotlib, numpy, and pillow

## Usage

- For an example of usage, please see example.py in the `py` folder or simply run the example:

```bash
python3 py/example.py
```

### C++

- Still a W.I.P.

## Improvements Remaining

- Precompute validity mask rather than computing radial distances each time
- Convert binary map to distance-to-nearest-object map for faster computation
- Enable 8-connected traversal by traveling the sam distance per step in all directions
- Store map/obstacles as vector graphics instead of PNG
- Change distance step size proportional to image size, not pixels
- Implement Dijkstra or A* instead of the BFS solution for slight speed up
- Convert to C++ ;)
