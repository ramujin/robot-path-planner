# Robot Path Planner

A simple robot path planning library

## Description

## Setup

### Python

- Install Python3
- Install dependencies with PIP:

```bash
python3 -m pip install matplotlib numpy pillow
```

## Usage

- For an example of usage, please see example.py in the `py` folder or simply run the example:

```bash
python3 py/example.py
```

### C++

- Still a W.I.P.

## Improvements Remaining

- Precompute validity mask rather than computing radial distances each time
- Convert binary map to distance-to-nearest-obstacle map for faster computation
- Enable 8-connected traversal by traveling the same distance per step in all directions
- Store map/obstacles as vector graphics instead of PNG
- Change distance step size proportional to image size, not pixels
- Implement Dijkstra or A* instead of the BFS solution for slight speed up
- Convert to C++

## Additional Considerations

1. Performance - What is the bottleneck in your library? How could you go about improving performance in the future?

    Current bottlenecks are the pixel-based traversal, repeat radial checking, and over-searching the space. All can be easily improved with a little more time.

2. Modularity - How would you handle additional planning algorithms and new methods of updating the map?

    The code is very modular. A new planning algorithm would simply replace the existing function call. The same is true of updating the map.

3. Cross-Platform - How would you alter your library to support multiple Operating Systems or multiple processors with different instruction sets?

    The Python version is already cross-platform as I'm using all standard packages. C++ would require a bit more work to compile for specific ISAs, but I don't see it being a major blocker.
