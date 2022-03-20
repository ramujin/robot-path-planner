import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

"""
A simple class to create an obstacle map, find an approximate shortest path in it, and visualize the found path
"""
class GalaxyMap():

  """
  Class attributes
  """
  size = None        # tuple: size of the M,N galaxy map
  map = None         # np.ndarray: binary map identifying locations of obstacles
  obstacles = []     # list[tuple]: a list of obstacles, where each tuple defines the x, y, and radius of an obstacle
  path_radius = 0    # int: the radius of the path traversal (size of the BB8 robot)
  shortest_path = [] # list[tuple]: a list containing the points in the shortest found path

  # # 8-connected grid
  # # Not using this because results would be misleading unless we travel the same unit distance in all directions
  # directions = [(-1,  1), (0,  1), (1,  1),
  #               (-1,  0),          (1,  0),
  #               (-1, -1), (0, -1), (1, -1)]
  # 4-connected grid
  directions = [         (0,  1),
                (-1, 0),          (1, 0),
                         (0, -1)        ]

  """
  Take the initial parameters of map size (M x N) to initialize the map
  """
  def __init__(self, size: tuple) -> None:
    self.size = size
    self.map = np.zeros(self.size)
    return


  """
  Add obstacles to the current map using as a parameter a list of circular obstacles
  """
  def add_obstacles(self, obstacles: list) -> None:
    self.obstacles = obstacles

    # Mark the map for each obstacle by measuring Euclidian distance from object center to radius
    for (x,y,r) in obstacles:
      pts = [(x+i, y+j) for i in range(-r,r+1) for j in range(-r,r+1) if i**2 + j**2 <= r**2]
      idx = list(map(lambda x:x[0], pts))
      idy = list(map(lambda x:x[1], pts))
      self.map[idx,idy] = 1
    return


  """
  Create the best safe path given a start and end location on the current map, taking into consideration the robot radius
  Note: the solution is a simple BFS where we keep track of visited nodes to avoid recalculation
  """
  def find_shortest_path(self, start: tuple, end: tuple, radius: int) -> int:

    self.path_radius = radius

    if not self.is_valid(start) or not self.is_valid(end):
      return -1

    # Start by queueing up the starting point as the first vertex and single point in the path
    queue = [(start, [start])]
    visited = set(start)

    # Until we have exhausted all paths or found the destination, keep searching
    while queue:
      # Grab the most recent point and its associated path
      vertex, path = queue.pop(0)

      # Attempt to go in all grid directions that are valid
      for (dx,dy) in self.directions:
        node = vertex[0]+dx, vertex[1]+dy

        # If the destination is found, we terminate the search, otherwise append to the queue and continue if valid
        if node == end:
          self.shortest_path = path + [end]
          return len(self.shortest_path)
        elif node not in visited and self.is_valid(node):
          visited.add(node)
          queue.append((node, path + [node]))

    return -1


  """
  Check to see if the given node is valid (in the map grid and also not colliding with an obstacle)
  """
  def is_valid(self, node: tuple) -> bool:
    (x,y) = node
    (m,n) = self.size

    # Boundary conditions
    if x<0 or x>=m or y<0 or y>=m:
      return False

    r = self.path_radius
    collisions = 0

    # Look for collisions with obstacles
    # TODO: major speedup can be achieved here!
    for i in range(x-r, x+r):
      for j in range(y-r, y+r):
        if i>=0 and i<m and j>=0 and j<n:
          collisions += self.map[i][j]

    return collisions == 0


  """
  Save the current map to a file
  """
  def save_map(self, filepath: str) -> None:
    Image.fromarray(np.uint8(np.flipud(self.map.T*255))).save(filepath)
    return


  """
  Load a map from a file
  """
  def load_map(self, filepath: str) -> None:
    self.map = np.flipud(np.asarray(Image.open(filepath))//255).T
    return


  """
  Visualize a map and path to the screen
  """
  def show(self) -> None:

    # Create the figure amd axes
    fig, ax = plt.subplots()
    fig.set_size_inches(10, 8)
    fig.set_tight_layout('tight')
    ax.set_aspect(True)
    ax.grid(True, linestyle='--')
    ax.set_facecolor('black')
    ax.set_xlim(-self.path_radius, self.size[0]+self.path_radius)
    ax.set_ylim(-self.path_radius, self.size[1]+self.path_radius)

    # Draw the map boundaries
    (x1, y1, x2, y2) = (0, 0, self.size[0], self.size[1])
    ax.plot([x1, x2], [y1, y1], '-g', lw=3)
    ax.plot([x1, x2], [y2, y2], '-g', lw=3)
    ax.plot([x1, x1], [y1, y2], '-g', lw=3)
    ax.plot([x2, x2], [y1, y2], '-g', lw=3)

    # Draw the base obstacle map
    base = np.zeros( (self.size[1],self.size[0],3) )
    base[:,:,0] = np.uint8(self.map.T)
    ax.imshow(base, origin='lower', interpolation="bicubic")

    # Draw the obstacles (if any)
    for (x,y,r) in self.obstacles:
      obstacle = plt.Circle((x,y), r, alpha=0.9, lw=4, facecolor='r', edgecolor='white')
      ax.add_patch(obstacle)

    # Draw the shortest path (if one is found)
    for pt in self.shortest_path:
      pt_circle = plt.Circle(pt, self.path_radius, alpha=0.1, lw=2, facecolor='gray', edgecolor='orange')
      ax.add_patch(pt_circle)

    # Draw robot start and end points (if there was a path found)
    if len(self.shortest_path) > 0:
      start = self.shortest_path[0]
      end = self.shortest_path[-1]
      start_circle = plt.Circle(start, self.path_radius, alpha=0.9, lw=4, facecolor='w', edgecolor='orange')
      end_circle = plt.Circle(end, self.path_radius, alpha=0.9, lw=4, facecolor='w', edgecolor='orange')
      ax.add_patch(start_circle)
      ax.add_patch(end_circle)
      ax.text(start[0]-5, start[1], "start", {'color':'green', 'fontsize':'large', 'weight':'bold'})
      ax.text(end[0]-5, end[1], "end", {'color':'green', 'fontsize':'large', 'weight':'bold'})

    # Show the plot of everything together
    ax.set_title("Welcome to the New Republic, BB8!", {'color':'red', 'fontsize':'xx-large', 'weight':'bold'})
    plt.show()
