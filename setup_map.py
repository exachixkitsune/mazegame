# -*- coding: utf-8 -*-
"""
Functions to configure the map
"""

import game_world
import maze_creation
import numpy

def fixed_map():
    # Currently using test map
    # Test configuration
    num_cells = [4, 4]
    
    # link table is 4-column table,
    #   Row-Col, (0-3 - direction. 0 is east/left, 1 is south/down)
    #   Internallly, 2 is west/left, 3 is north/up
    # Endmap will autogenerate this
    link_table = [  [0, 0, 1],
                    [0, 1, 0],
                    [0, 2, 1],
                    [0, 2, 0],
                    [1, 0, 0],
                    [1, 1, 0],
                    [1, 1, 1],
                    [1, 2, 0],
                    [1, 2, 1],
                    [1, 3, 1],
                    [2, 0, 0],
                    [2, 0, 1],
                    [2, 2, 1],
                    [2, 3, 1],
                    [3, 1, 0]]
    
    # Size of elements
    # These are INCLUSIVE of the border elements
    cell_size = [9, 9]
    corridor_width = 5
    # Length of the corridor - this is NOT inclusive of the edges
    corridor_length = 1
    
    # Configure Map
    this_world = game_world.game_world(num_cells, link_table, cell_size, corridor_width, corridor_length)
    
    # Add money locations
    money_locs = [[0,1],
                  [0,3],
                  [1,1],
                  [1,2],
                  [1,3],# 5
                  [2,1],
                  [2,2],
                  [2,3],
                  [3,0],
                  [3,2]]#10
    for i_money in range(len(money_locs)):
        this_world.maze.add_object([money_locs[i_money][0],money_locs[i_money][1]],game_world.maze_map.CELLINDX_MONEY)
    
    this_world.maze.add_object([num_cells[0]-1,num_cells[1]-1],game_world.maze_map.CELLINDX_STAIRS)
    
    return this_world

def random_map(map_size, num_money):
    # Make a random Map
    num_cells = map_size
    
    # Defined map elements
    # Size of elements
    # These are INCLUSIVE of the border elements
    cell_size = [7, 7]
    corridor_width = 5
    # Length of the corridor - this is NOT inclusive of the edges
    corridor_length = 1
    
    # Now need to randomly create the link table
    maze_details = maze_creation.maze_create_links(map_size)
    
    # Configure Map
    this_world = game_world.game_world(num_cells, maze_details['link_table'], cell_size, corridor_width, corridor_length)
    
    # Place stairs
    stairs_loc = [num_cells[0]-1,num_cells[1]-1]
    this_world.maze.add_object(stairs_loc,game_world.maze_map.CELLINDX_STAIRS)
    
    
    # Add in the dubloons~~~~~~~~~~~~~~~~~~~~~~
    
    # Cap the amount of money you can have
    max_num_money = cell_size[0]*cell_size[1] - 2
    num_money = min(max_num_money,num_money)
    
    # List the valid slots that you can have 
    valid_slots = []
    for i_y_slot in range(map_size[0]):
        for i_x_slot in range(map_size[1]):
            valid_slots.append([i_y_slot, i_x_slot])
    # Remove the start slot
    valid_slots.remove([0,0])
    # Remove the stairs slot
    valid_slots.remove(stairs_loc)
    
    for i_money in range(num_money):
        # Safety Check, if we've ran out of slots, stop
        if (len(valid_slots) < 1):
            break
        # Get a random slot
        slot_indx = numpy.random.randint(len(valid_slots))
        this_location = valid_slots[slot_indx]
        valid_slots.remove(this_location)
        
        # Add the money
        this_world.maze.add_object(this_location, game_world.maze_map.CELLINDX_MONEY)

    
    return this_world