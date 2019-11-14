# -*- coding: utf-8 -*-
"""
    Finds, given a particular center location in a grid, if adjoining
    elements are a 'target number'
"""

import numpy

# Process for analysing a grid and looking at the ones around it

# Using curses's yx orientation
# that is, first value is y, second is x.

def match_adjacent_elements(grid, center, target_number, default=True):
    grid_shape = numpy.shape(grid)
    
    # Look at each element direction in order
    # This is hardcoded to make it make a bit more sense
    
    center_y = center[0]
    center_x = center[1]
    
    # NORTH
    tgt_y = center_y - 1
    tgt_x = center_x
    # Is tgt_y in the correct position
    if (0 <= tgt_y):
        north = (grid[tgt_y][tgt_x] == target_number)
    else:
        north = default
        
    # EAST
    tgt_y = center_y
    tgt_x = center_x + 1
    # Is tgt_y in the correct position
    if (tgt_x < grid_shape[1]):
        east = (grid[tgt_y][tgt_x] == target_number)
    else:
        east = default
    
    # SOUTH
    tgt_y = center_y + 1
    tgt_x = center_x
    # Is tgt_y in the correct position
    if (tgt_y < grid_shape[0]):
        south = (grid[tgt_y][tgt_x] == target_number)
    else:
        south = default
    
    # WEST
    tgt_y = center_y
    tgt_x = center_x - 1
    # Is tgt_y in the correct position
    if (0 <= tgt_x):
        west = (grid[tgt_y][tgt_x] == target_number)
    else:
        west = default
    
    
    return [north, east, south, west]