# -*- coding: utf-8 -*-
"""
    Maze creation Algorithms
"""

# Maze manipulation

import numpy

def walls_check(walls_list, cell_loc, horizontal_walls, vertical_walls):
    # What walls exist for cell_loc
    
    ver_wall_shape = numpy.shape(vertical_walls)
    hor_wall_shape = numpy.shape(horizontal_walls)
    
    # Each wall
    # Vertical walls
    ver_wall = []
    ver_wall.append([cell_loc[0]-1, cell_loc[1]])
    ver_wall.append([cell_loc[0], cell_loc[1]])
    
    for i_wall in range(len(ver_wall)):
        # Can you look at wall
        # Assuming here cell_loc is a valid cell loc already
        # Thus, only checking first
        this_wall = ver_wall[i_wall]
        if ((0 <= this_wall[0]) and (this_wall[0] < ver_wall_shape[0]) and vertical_walls[this_wall[0]][this_wall[1]]):
            walls_list.append([0, this_wall[0], this_wall[1]])
            
    # Horizontal Walls
    hor_wall = []
    hor_wall.append([cell_loc[0], cell_loc[1]])
    hor_wall.append([cell_loc[0], cell_loc[1]-1])
    
    for i_wall in range(len(hor_wall)):
        # Can you look at wall
        # Assuming here cell_loc is a valid cell loc already
        # Thus, only checking first
        this_wall = hor_wall[i_wall]
        if ((0 <= this_wall[1]) and (this_wall[1] < hor_wall_shape[1]) and horizontal_walls[this_wall[0]][this_wall[1]]):
            walls_list.append([1, this_wall[0], this_wall[1]])
            
    # Return this
    return(walls_list)
    
    

def maze_create_walls(maze_size):
    # Describe the maze as a set of cells that is maze_size[0] by maze_size[1]
    # in size.
    
    # As per the algorithm on wikipedia
    # https://en.wikipedia.org/wiki/Maze_generation_algorithm#Randomized_Prim's_algorithm
    #
    # 1. Start with a list of cells unconnected, a grid full of walls
    # 2. Pick an initial cell. Mark it in the maze.
    #        add the walls of the cells to a list of walls
    # 3. While still walls in the list
    #       Pick a random wall
    #           If only one of the two cells is visited
    #               Make the wall a passage, mark it's other cells part of maze
    #               Add that cell's walls to the list
    #           Remove the wall from the list (not the grid)
    
    
    # visited_cells locations are true location [a,b]
    # The horizontal walls are [a,b] and [a,b-1]
    # The vertical walls are [a,b] and [a-1,b]
    # Thus, given a vertical wall of [c,d], the cells are
    # [c,d] and [c+1,d]
    # And as appropriate for the horizontal wall
    # [e,f] -> [e,f], [e,f+1]
    
    
    # Settings ~~~~~~~~~~~~~~~~~
    # The starting cell is 0,0
    #   TO note, this is the cell the player always starts in
    initial_cell = [0,0]
    
    # Initialise ~~~~~~~~~~~~~~~
    # Cells visited
    visited_cells = numpy.zeros(maze_size,numpy.bool)
    # Walls that exist
    # Walls between adjacent horizontal cells
    horizontal_walls  = numpy.ones([maze_size[0], maze_size[1]-1],numpy.bool)
    # Walls between adjacent vertical cells
    vertical_walls  = numpy.ones([maze_size[0]-1, maze_size[1]],numpy.bool)
    # Walls list to be handled
    walls_list = []
    
    # Pick an initial cell
    visited_cells[initial_cell[0],initial_cell[1]] = True
    # Evaluate, what walls exist?
    walls_list = walls_check(walls_list, initial_cell, horizontal_walls, vertical_walls)
    
    # While this walls list is not empty
    while(len(walls_list) > 0):
        # Find one of the walls for which the adjacent cells are visited
        random_wall_indx = numpy.random.randint(len(walls_list))
        this_wall = walls_list[random_wall_indx]
        walls_list.remove(this_wall)
        
        # Which wallset is this, and what cells are on either side?
        if this_wall[0] == 0:
            # Vertical Wall
            cell_1 = [this_wall[1],     this_wall[2]]
            cell_2 = [this_wall[1]+1,   this_wall[2]]
        else:
            # Horizontal Wall
            cell_1 = [this_wall[1],   this_wall[2]  ]
            cell_2 = [this_wall[1],   this_wall[2]+1]
            
        # Which of these two are visitied?
        cell_visited = []
        cell_visited.append(visited_cells[cell_1[0],cell_1[1]])
        cell_visited.append(visited_cells[cell_2[0],cell_2[1]])
        num_visited = sum(cell_visited)
        
        # If only one of these is visited
        if num_visited == 1:
            # REMOVE THE WALL!
            if this_wall[0] == 0:
                vertical_walls[this_wall[1]][this_wall[2]] = False
            else:
                horizontal_walls[this_wall[1]][this_wall[2]] = False
            
            # Mark cell visited, and add to walls_list
            if (not cell_visited[0]):
                visited_cells[cell_1[0]][cell_1[1]] = True
                walls_list = walls_check(walls_list, cell_1, horizontal_walls, vertical_walls)
            if (not cell_visited[1]):
                visited_cells[cell_2[0]][cell_2[1]] = True
                walls_list = walls_check(walls_list, cell_2, horizontal_walls, vertical_walls)
            
    return {'horizontal_walls':horizontal_walls, 'vertical_walls':vertical_walls}

def maze_create_links(maze_size):
    # Create maze walls
    walls = maze_create_walls(maze_size)
    
    # Convert to a linktable
    # Link table is:
    # 0 - East
    # 1 - South
    # 2 - West
    # 3 - North
    # Except that only East and South walls are detailed.
    
    # SO look at every cell (except the bottom row and the rightmost column)
    # and find if the walls associated with it exist
    # This turns out to be
    #  Checking cell [a,b]
    #  Checking horizontal wall [a,b] for EAST
    #  Checking vertical wall [a,b] for SOUTH
    
    link_table = []
    for i_cell_y in range(maze_size[0]):
        for i_cell_x in range(maze_size[1]):
            # Check Horizontal Wall
            #   Provided there would be a horizontal wall(i.e. not right at the end of the array)
            # If no wall, it's a link
            if ((i_cell_x < (maze_size[1] - 1)) and (not walls['horizontal_walls'][i_cell_y][i_cell_x])):
                link_table.append([i_cell_y, i_cell_x, 0])
            # Check Vertical Wall
            #   Again, check we're at the end of the array
            # If no wall, it's a link!
            if ((i_cell_y < (maze_size[0] - 1)) and (not walls['vertical_walls'][i_cell_y][i_cell_x])):
                link_table.append([i_cell_y, i_cell_x, 1])
                
    return {'link_table': link_table, 'horizontal_walls':walls['horizontal_walls'], 'vertical_walls':walls['vertical_walls']}