# -*- coding: utf-8 -*-
"""
    Game World Class
    Contains elements such as:
        Player location
        Game Map
        Player Cells
"""

import maze_map
import numpy
import math

# Notation
#   Row-Col, (0-3 - direction. 0 is east/left, 1 is south/down)
#   Internallly, 2 is west/left, 3 is north/up

class game_world:
    def __init__(self, in_num_cells, in_link_table, in_cell_size, in_corridor_width, in_corridor_length):
        # Set up world map
        self.maze = maze_map.maze_map(in_num_cells,
                                      in_link_table,
                                      in_cell_size,
                                      in_corridor_width,
                                      in_corridor_length)
        
        # Initialise player location
        # Middle of the 0-0 cell.
        self.player_loc = [math.floor(in_cell_size[0]/2),
                           math.floor(in_cell_size[1]/2)]
        
        # How many coins have been found?
        self.score = 0
        
        # what cells have been visited?
        # currently none
        self.visited_cells = numpy.zeros(in_num_cells,
                                         dtype=numpy.bool)
        self.update_visited()
        
        self.victory = False
        
    def render(self, map_window):
        self.maze.draw_map(map_window, self.visited_cells, self.player_loc)

    def move_player(self, direction):
        # Which way is the player moving?
        new_position = self.player_loc.copy()
        if (direction == 0):
            # East / Left
            new_position[1] += 1
        elif (direction == 1):
            # South / Down
            new_position[0] += 1
        elif (direction == 2):
            # West / left
            new_position[1] -= 1
        elif (direction == 3):
            # North / Up
            new_position[0] -= 1
        
        # Is the new position a valid position
        can_hold_person = self.maze.can_pos_hold_person(new_position)
        if can_hold_person:
            # Move player item to new slot
            self.player_loc = new_position.copy()
            # Update if this is a new visited location
            self.update_visited()
        # Otherwise don't move
        
    def world_check(self):
        # Check things in the world and update stuff as appropriate
        current_tile = self.maze.get_pos_contents(self.player_loc)
        # What is the current tile?
        if current_tile == maze_map.CELLINDX_STAIRS:
            self.victory = True
        elif current_tile == maze_map.CELLINDX_MONEY:
            # On a money slot
            # Thus, remove this money slot,
            # And add a score point
            # Current cell
            current_cell = self.maze.which_cell(self.player_loc)
            # Remove element from object array
            self.maze.objects_list.remove([current_cell, maze_map.CELLINDX_MONEY])
            # Increment score
            self.score += 1
        
    def update_visited(self):
        # Which cell is the player in
        current_cell = self.maze.which_cell(self.player_loc)
        # Set this cell to be visited
        self.visited_cells[current_cell[0]][current_cell[1]] = True
        
        shape = numpy.shape(self.visited_cells)
        # Also update all adjacent as visible
        # but only if the adjacent cell is valid
        north_cell = current_cell.copy()
        north_cell[0] -= 1
        south_cell = current_cell.copy()
        south_cell[0] += 1
        east_cell = current_cell.copy()
        east_cell[1] += 1
        west_cell = current_cell.copy()
        west_cell[1] -= 1
        # Check if each cell is applicable, and also, if it's visible/adjacent
        if (0 <= north_cell[0]):
            self.visited_cells[north_cell[0]][north_cell[1]] = self.visited_cells[north_cell[0]][north_cell[1]] or self.maze.cell_adjacent(current_cell,north_cell)
        if (south_cell[0] < shape[0]):
            self.visited_cells[south_cell[0]][south_cell[1]] = self.visited_cells[south_cell[0]][south_cell[1]] or self.maze.cell_adjacent(current_cell,south_cell)
        if (east_cell[1] < shape[1]):
            self.visited_cells[east_cell[0]][east_cell[1]] = self.visited_cells[east_cell[0]][east_cell[1]] or self.maze.cell_adjacent(current_cell,east_cell)
        if (0 <= west_cell[1]):
            self.visited_cells[west_cell[0]][west_cell[1]] = self.visited_cells[west_cell[0]][west_cell[1]] or self.maze.cell_adjacent(current_cell,west_cell)