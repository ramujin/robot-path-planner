#include <iostream>
#include "xtensor/xarray.hpp"
#include "xtensor/xio.hpp"
using namespace std;

class GalaxyMapper {
  private:
    xt::xarray<int> size;          // size of the M, N galaxy map
    xt::xarray<int> map;           // binary map identifying locations of obstacles
    xt::xarray<int> obstacles;     // a list of obstacles, where each tuple defines the x, y, and radius of an obstacle
    int path_radius = 0;           // the radius of the path traversal (size of the BB8 robot)
    xt::xarray<int> shortest_path; // a list containing the points in the shortest found path
    xt::xarray<int>  directions = {         {0,  1},
                                   {-1, 0},          {1, 0},
                                            {0, -1}        }

  public:

}