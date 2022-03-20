from GalaxyMapper import GalaxyMap
import numpy as np

"""
A demonstration of how to use the GalaxyMap "library" to find the shortest path
"""
if "__main__" ==  __name__:

  # Create an initial map of size (M, N)
  (M, N) = (200, 200)
  galaxy = GalaxyMap(size=(M, N))

  # Generate P obstacles with radii no bigger than 10% of min(M,N), with overlap allowed
  P = 10
  obstacles = []
  for i in range(P):
    r = np.random.randint(1, min(M,N)//10)
    x = np.random.randint(r, M-r-1)
    y = np.random.randint(r, N-r-1)
    obstacles.append((x,y,r))
  galaxy.add_obstacles(obstacles)

  # Save and load the obstacle map to/from file as a binary image
  galaxy.save_map("map.png")
  galaxy.load_map("map.png")

  # Generate a random BB8 no bigger than 10% of min(M,N) with start and end points
  distance = -1
  while distance < 0:
    r = np.random.randint(1, min(M,N)//10)
    start = (np.random.randint(r, M-r-1), np.random.randint(r, N-r-1))
    end = (np.random.randint(r, M-r-1), np.random.randint(r, N-r-1))

    # Find the shortest path if one exists from start to finish
    distance = galaxy.find_shortest_path(start=start, end=end, radius=r)

    if distance < 0:
      print(f"The robot was obstructed by an obstacle. Choosing new points!")

  print(f"The shortest safe path is {distance} steps long as illustrated in the figure.")

  # Visualize the shortest path
  galaxy.show()
