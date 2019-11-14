# -*- coding: utf-8 -*-
"""
    Primary class that holds all the maze map information
"""

# Visualisation of a maze

# Two ways of doing this
#       Automatically work out what the wall should be based off adjacency
# or    Use pre-built cells

# I think, if we have a map of links we should be good?
# Then, each link is a block of the size 'cell_size'.
# with a corridor width of 3

# Maps are set up by:
#   Making a particular cell 

#linkmap:
import curses
import math
import numpy

import curses_colour
import curses_line_matchup
import match_adjacent_elements
import floor_character

# All dimensions are:
# y , x/

# CONSTANTS
CELLINDX_VOID = -1
CELLINDX_WALL = 0
CELLINDX_FLOOR = 1
CELLINDX_STAIRS = 2
CELLINDX_MONEY = 3

# Default Player Char
OBJ_PLAYER_CHAR = 'P'

OBJ_STAIRS_CHAR = 'S'
OBJ_STAIRS_COLR = curses_colour.S_FEATURE_2

OBJ_MONEY_CHAR = 'D'
OBJ_MONEY_COLR = curses_colour.S_FEATURE_4

COL_P_PRIMARY = 31
COL_P_SECONDR = 32
COL_P_PLAYER = 33
COL_P_STAIRS = 34

# Testmap is 4x4
class maze_map:
    def __init__(self, in_num_cells, in_link_table, in_cell_size, in_corridor_width, in_corridor_length, colour_mode = 0):
        self.num_cells = in_num_cells.copy()
        self.link_table = in_link_table.copy()
        self.cell_size = in_cell_size.copy()
        self.corridor_width = in_corridor_width
        self.corridor_length = in_corridor_length
        self.set_player_character()
        # Init blank objects list
        #  3 columns; y_cell, x_cell, and cellIndx.
        self.objects_list = []
            
        
    def set_player_character(self, character=OBJ_PLAYER_CHAR, colour=curses_colour.S_FEATURE_1):
        self.player_character = character
        self.player_colour = colour
        
    def add_object(self, cell_pos, object_indx):
        # Make a list item, and append to objects_list
        #  contents are y_cell, x_cell and cellIndx
        this_list_bit = [cell_pos, object_indx]
        self.objects_list.append(this_list_bit)
        
    # ~~~~~~~~~~~~~~~~
    # Object list search
    def find_objects(self, cell_pos):
        # Find which items in the objects list are the relavent object
        obj_in_cell = []
        for i_object in range(len(self.objects_list)):
            if (cell_pos == self.objects_list[i_object][0]):
                # This is in the cell in question
                # Thus, return this object.
                obj_in_cell.append(self.objects_list[i_object][1])
        # Sort in priority level
        obj_in_cell.sort()
        return obj_in_cell
    
    def object_placement(self):
        # These are the places that objects go within the layout tables in
        # setup_cell_layout
        
        # This is always the cell center
        placements = [[self.corridor_length + math.floor(self.cell_size[0]/2),
                       self.corridor_length + math.floor(self.cell_size[1]/2)]]
        return placements
    # ~~~~~~~~~~~~~~~~
    # Coordinate Transform
    # Between the 'cell' grid setup, and the 'world' grid setup
    
    def which_cell(self, world_pos):
        # What cell is this particular map position in?
        # Basically, how many cells+corridors can you fit in the positive dimension?
        # For the purposes of this, the corridor is within the top-left of cell
        cell_col = math.floor(world_pos[0] / (self.cell_size[0] + self.corridor_length))
        cell_row = math.floor(world_pos[1] / (self.cell_size[1] + self.corridor_length))
        return [cell_col, cell_row]
    
    def pos_in_cell(self, world_pos):
        # What position in-cell is this particular map position?
        # Find the cell cell_pos is in
        this_cell = self.which_cell(world_pos)
        # Remove offsets
        incell_pos_col = world_pos[0] - this_cell[0]*(self.cell_size[0] + self.corridor_length)
        incell_pos_row = world_pos[1] - this_cell[1]*(self.cell_size[1] + self.corridor_length)
        return [incell_pos_col, incell_pos_row]

    def pos_in_world(self, cell_pos, incell_pos):
        # Convert from cell position to full map position
        # First, work out what the corner position of the cell is
        # Note a special case here, if the cell is 0, there should be
        # no corridor offset (as the corridor offset is the bit between cells.)
        # Thus, use max to limit it to being at least 0.
        cell_corner_row = self.cell_size[0]*cell_pos[0] + max(self.corridor_length*(cell_pos[0] - 1),0)
        cell_corner_col = self.cell_size[1]*cell_pos[1] + max(self.corridor_length*(cell_pos[1] - 1),0)
        
        # Then, the world position is this cell corner + incell_pos
        return [ cell_corner_row + incell_pos[0], cell_corner_col + incell_pos[1] ]
        
    # ~~~~~~~~~~~~~~~~
    # Map interrogation
        
    def find_link_single(self, y_loc, x_loc):
        # Find what directions are matched by this x_loc and y_loc
        # Only finds the rows which are matched by [x_loc y_loc *]
        num_rows = len(self.link_table)
        links = []
        for i_row in range(num_rows):
            if ((self.link_table[i_row][0] == y_loc) and 
                (self.link_table[i_row][1] == x_loc)):
                links.append(self.link_table[i_row][2])
        return links
        
    def find_links(self, y_loc, x_loc):
        # Find what directions are matched by this x_loc and y_loc
        # Get matches for own block
        own_links = self.find_link_single(y_loc, x_loc)
        # Check adjacent (north and west)
        # If this has a link in this particular direction, then append
        # appropriate value to own_links
        if (not (x_loc == 0)):
            west_links = self.find_link_single(y_loc, x_loc - 1)
            if (0 in west_links):
                own_links.append(2)
                
        if (not (y_loc == 0)):
            north_links = self.find_link_single(y_loc - 1, x_loc)
            if (1 in north_links):
                own_links.append(3)
                
        own_links.sort()
        # Output what we found
        return own_links
    
    def max_map_dimensions(self):
        # Map dimensions are taken from cell sizes and it's objects
        # Total height/width is:
        #            Width of all cells        + Width of all corridors
        #  map_dim = cell_size[i]*num_cells[i] + corridor_length*(num_cells[i]-1)
        
        map_height = self.cell_size[0]*self.num_cells[0] + self.corridor_length*(self.num_cells[0] - 1)
        map_width  = self.cell_size[1]*self.num_cells[1] + self.corridor_length*(self.num_cells[1] - 1) 
        return [map_height, map_width]
        
    def setup_cell_layout(self, links, cell_pos = []):
        # Cell layout
        # Make an array that's the size of the cell, plus the extra edging for
        # Making corridors
        # (Corridor elements may not be rendered)
        # Thus, array size is cell_size + corridor_length*2
        array_size = self.cell_size.copy()
        array_size[0] += 2*self.corridor_length
        array_size[1] += 2*self.corridor_length
        
        cell_layout = CELLINDX_VOID * numpy.ones(array_size, numpy.int8)
        
        # Main room extents
        extent_n = self.corridor_length
        extent_s = self.corridor_length + self.cell_size[0] - 1
        extent_w = self.corridor_length
        extent_e = self.corridor_length + self.cell_size[1] - 1
        
        # Corridor extents
        #  NW most Will be half the cell size from the edge
        #  SE will be that + corridor width(minus 1 for the first one)
        corridor_n = math.floor(self.cell_size[0]/2) - 1
        corridor_s = corridor_n + (self.corridor_width-1)
        corridor_w = math.floor(self.cell_size[1]/2) - 1
        corridor_e = corridor_w + (self.corridor_width-1)
        
        # setup layout
        # Do each extent
        # Make valid walking space
        cell_layout = self.set_cell_layout_box(cell_layout,
                                               [extent_n, extent_s], [extent_w, extent_e],
                                               CELLINDX_FLOOR)
        
        # Will overwrite the corridor sections
        cell_layout = self.set_cell_layout_box(cell_layout,
                                               [extent_n, extent_n], [extent_w, extent_e]) # N Wall
        cell_layout = self.set_cell_layout_box(cell_layout,
                                               [extent_s, extent_s], [extent_w, extent_e]) # S Wall
        cell_layout = self.set_cell_layout_box(cell_layout,
                                               [extent_n, extent_s], [extent_w, extent_w]) # W Wall
        cell_layout = self.set_cell_layout_box(cell_layout,
                                               [extent_n, extent_s], [extent_e, extent_e]) # E Wall
        
        # Add corridors if they exist
        # This overrides the existing slot, and then puts the corrior bits
        # North Corridor
        if (0 in links):
            # EAST / LEFT
            # Clear - 0 to extent, in corridor block
            cell_layout = self.set_cell_layout_box(cell_layout,
                                                   [corridor_n, corridor_s], [extent_e, array_size[1]-1],
                                                   CELLINDX_FLOOR)
            # Add walls
            cell_layout = self.set_cell_layout_box(cell_layout,
                                                   [corridor_n, corridor_n], [extent_e, array_size[1]-1])
            cell_layout = self.set_cell_layout_box(cell_layout,
                                                   [corridor_s, corridor_s], [extent_e, array_size[1]-1])
            
        if (1 in links):
            # SOUTH / DOWN
            # Clear - 0 to extent, in corridor block
            cell_layout = self.set_cell_layout_box(cell_layout,
                                                   [extent_s, array_size[0] - 1], [corridor_w, corridor_e],
                                                   CELLINDX_FLOOR)
            # Add walls
            cell_layout = self.set_cell_layout_box(cell_layout,
                                                   [extent_s, array_size[0] - 1], [corridor_w, corridor_w])
            cell_layout = self.set_cell_layout_box(cell_layout,
                                                   [extent_s, array_size[0] - 1], [corridor_e, corridor_e])
            
        if (2 in links):
            # WEST / RIGHT
            # Clear - 0 to extent, in corridor block
            cell_layout = self.set_cell_layout_box(cell_layout,
                                                   [corridor_n, corridor_s], [0, extent_w],
                                                   CELLINDX_FLOOR)
            # Add walls
            cell_layout = self.set_cell_layout_box(cell_layout,
                                                   [corridor_n, corridor_n], [0, extent_w])
            cell_layout = self.set_cell_layout_box(cell_layout,
                                                   [corridor_s, corridor_s], [0, extent_w])
            
        if (3 in links):
            # NORTH / Up
            # Clear - 0 to extent, in corridor block
            cell_layout = self.set_cell_layout_box(cell_layout,
                                                   [0, extent_n], [corridor_w, corridor_e],
                                                   CELLINDX_FLOOR)
            # Add walls
            cell_layout = self.set_cell_layout_box(cell_layout,
                                                   [0, extent_n], [corridor_w, corridor_w])
            cell_layout = self.set_cell_layout_box(cell_layout,
                                                   [0, extent_n], [corridor_e, corridor_e])
        if cell_pos:
            # What objects live in this cell?
            objects_in_cell = self.find_objects(cell_pos)
            # Place these objects in the cell
            # These are arranged in priority order.
            # Place up to 4 items - in the corners
            object_positions = self.object_placement()
            num_objects = len(objects_in_cell)
            for i_object in range(min(num_objects,len(object_positions))):
                # Place
                cell_layout[object_positions[i_object][0],object_positions[i_object][1]] = objects_in_cell[i_object]
        
        return(cell_layout)
        
    def set_cell_layout_box(self, cell_layout, y_range, x_range, set_to=CELLINDX_WALL):
        # Set all elements in cell_layout to be true

        # The values are Inclusive. Thus, range needs to be extended by one
        for x_indx in range(x_range[0],x_range[1]+1):
            for y_indx in range(y_range[0],y_range[1]+1):
                cell_layout[y_indx][x_indx] = set_to
        return cell_layout

    def get_pos_contents(self, world_position):
        # Get The particular cell and return what the cell is
        # What cell are you in?
        this_cell_pos = self.which_cell(world_position)
        # What position in cell
        this_incell_pos = self.pos_in_cell(world_position)
        
        # Get this cell layout
        # Note that this cell layout includes the corridor slot at the North and the west
        this_cell_layout = self.setup_cell_layout(self.find_links(this_cell_pos[0],this_cell_pos[1]),this_cell_pos)
        
        # Find what the item at a particular cell position is
        contents = this_cell_layout[this_incell_pos[0]+self.corridor_length][this_incell_pos[1]+self.corridor_length]
        return contents

    def can_pos_hold_person(self, world_position):
        # Is a position a valid location to have a thing
        # Get the contents
        position_contents = self.get_pos_contents(world_position)
        
        can_hold_person = not((position_contents == CELLINDX_VOID) or
                              (position_contents == CELLINDX_WALL))
        return can_hold_person
        
    def cell_adjacent(self, cell_1, cell_2):
        # Is cell 1 DIRECTLY adjacent to cell 2?
        
        # Safety check, is cell_1 and cell_2 the same?
        if ((cell_1[0] == cell_2[0]) and (cell_1[1] == cell_2[1]) ):
            return False
                
        # Firstly, is the range from cell_2 to cell_1 exactly 1?
        # If it's not one, it'll not be directly adjacent
        # Don't need to square root, as 1^2 = 1
        cell_delta = [0,0]
        cell_delta[0] = cell_2[0] - cell_1[0]
        cell_delta[1] = cell_2[1] - cell_1[1]
        cell_range_sqrd = (math.pow(cell_delta[0],2) + math.pow(cell_delta[1],2))
        if (cell_range_sqrd == 1):
            # Cell 1 adjacencies
            links = self.find_links(cell_1[0],cell_1[1])
            # What direction adjacent is it?
            
            if ((cell_delta[0] == -1) and (3 in links)):
                # North
                return True
            elif ((cell_delta[0] == 1) and (1 in links)):
                # South
                return True
            elif ((cell_delta[1] == -1) and (2 in links)):
                # West
                return True
            elif ((cell_delta[1] == 1) and (0 in links)):
                # East
                return True
            else:
                return False
        else:
            # Not directly adjacent
            return False
    
    # ~~~~~~~~~~~~~~~~~~~~~
    # Rendering
    
    def draw_induvidual_cell(self,
                             curseswindow,
                             cell_loc,
                             cell_corner_in_window,
                             print_colour=curses_colour.S_PRIMARY):
        # Window size for 
        window_size = curseswindow.getmaxyx()
        
        # Write each cell object
        # Create the grid
        # Cell links
        cell_links = self.find_links(cell_loc[0],cell_loc[1])
        # Grid to be output
        grid_to_make = self.setup_cell_layout(cell_links,cell_loc)
        
        # Make walls
        #  Not writing the corridor pieces in the top-left
        #  Don't remove from the array because I need them,
        #  But instead offset the i_y and i_x we're using to write position
        # Iterate over each i_y and i_x we're trying to plot
        #  Thus, the amount of elements to print is self.cell_size[0] for the cell
        #  and self.corridor_length for the corridor
        for i_y_toplot in range(0, self.cell_size[0] + self.corridor_length):
            # Source position
            i_y_fromgrid = i_y_toplot + self.corridor_length
            # Target Position
            i_y_inwindow = i_y_toplot + cell_corner_in_window[0]
            for i_x_toplot in range(0, self.cell_size[1] + self.corridor_length):
                # Source Position
                i_x_fromgrid = i_x_toplot + self.corridor_length
                # Target Position
                i_x_inwindow = i_x_toplot + cell_corner_in_window[1]
                
                # Is this a valid position to output
                # It must be within the window bounds
                # There is also a random error where when adding the character
                # in the bottom-right hand corner causes a crash.
                # Thus, the x-y position also CANNOT be [window_size[0]-1, window_size[1]-1]
                # The last line of this checks if the 
                if ((0 <= i_y_inwindow) and (i_y_inwindow < window_size[0]) and
                    (0 <= i_x_inwindow) and (i_x_inwindow < window_size[1]) and
                    (not ( (i_y_inwindow == (window_size[0]-1)) and (i_x_inwindow == (window_size[1]-1)) ) )):
                    # We can output this position!
                    # What should this look like?
                    this_checkval = grid_to_make[i_y_fromgrid][i_x_fromgrid]
                    if (this_checkval == CELLINDX_WALL):
                        # Going to be a wall
                        # What are the adjoining objects
                        links = match_adjacent_elements.match_adjacent_elements(grid_to_make,
                                                        [i_y_fromgrid, i_x_fromgrid],
                                                        CELLINDX_WALL,
                                                        True)
                        # Find character to make
                        character_to_print = curses_line_matchup.curses_line_matchup_arr(links)
                        # Put character in the window
                        curseswindow.addch(i_y_inwindow, i_x_inwindow,character_to_print,curses.color_pair(print_colour))
                    elif (this_checkval == CELLINDX_FLOOR):
                        # What character will this become?
                        character_to_print = floor_character.floor_character(self.pos_in_world(cell_loc,[i_y_fromgrid,i_x_fromgrid]))
                        # Put character in the window
                        curseswindow.addch(i_y_inwindow, i_x_inwindow,character_to_print,curses.color_pair(print_colour))
                    elif (this_checkval == CELLINDX_STAIRS):
                        # Put character
                        curseswindow.addch(i_y_inwindow, i_x_inwindow,OBJ_STAIRS_CHAR,curses.color_pair(OBJ_STAIRS_COLR))
                    elif (this_checkval == CELLINDX_MONEY):
                        # Put character
                        curseswindow.addch(i_y_inwindow, i_x_inwindow,OBJ_MONEY_CHAR,curses.color_pair(OBJ_MONEY_COLR))
                        
                        
    def draw_induvidual_cell_noncenter(self,
                                       curseswindow,
                                       player_cell,
                                       player_cell_corner_in_window,
                                       this_cell,
                                       print_colour=curses_colour.S_PRIMARY):
        # Plots an induvidual cell that is offset from the normal cell
        # Different to the normal cell becuase it needs to work out the cell
        # corner offset
        
        # What is the cell delta?
        cell_delta = [0, 0]
        cell_delta[0] = this_cell[0] - player_cell[0]
        cell_delta[1] = this_cell[1] - player_cell[1]
        
        # Thus, what is the new cell_corner
        cell_corner_in_window = player_cell_corner_in_window.copy()
        # Offset by amount of cell delta
        cell_corner_in_window[0] += cell_delta[0]*(self.cell_size[0] + self.corridor_length)
        cell_corner_in_window[1] += cell_delta[1]*(self.cell_size[1] + self.corridor_length)
        
        self.draw_induvidual_cell(curseswindow, this_cell, cell_corner_in_window, print_colour)
        
    def draw_map(self, curseswindow, visible_cells, player_loc):
        # Make the map
        
        # Clear the window
        curseswindow.clear()
        #curseswindow.border()
        
        # Find center location
        window_size = curseswindow.getmaxyx()
        mid_location = [math.floor(window_size[0]/2), math.floor(window_size[1]/2)]
        
        
        # Which cell is the player in?
        player_cell = self.which_cell(player_loc)
        player_place_in_cell = self.pos_in_cell(player_loc)
        # Offset of primary cell from center
        player_cell_corner = [
                mid_location[0] - player_place_in_cell[0],
                mid_location[1] - player_place_in_cell[1]]
    
        self.draw_induvidual_cell(curseswindow, player_cell, player_cell_corner)
        # Do each direction
        north_cell = player_cell.copy()
        north_cell[0] -= 1
        make_north = self.cell_adjacent(player_cell, north_cell)
        south_cell = player_cell.copy()
        south_cell[0] += 1
        make_south = self.cell_adjacent(player_cell, south_cell)
        west_cell = player_cell.copy()
        west_cell[1] -= 1
        make_west = self.cell_adjacent(player_cell, west_cell)
        east_cell = player_cell.copy()
        east_cell[1] += 1
        make_east = self.cell_adjacent(player_cell, east_cell)
        # Draw offset cell
        # Check each adjacency
        if make_north:
            self.draw_induvidual_cell_noncenter(curseswindow, player_cell, player_cell_corner, north_cell, curses_colour.S_PRIMARY)
        if make_south:
            self.draw_induvidual_cell_noncenter(curseswindow, player_cell, player_cell_corner, south_cell, curses_colour.S_PRIMARY)
        if make_west:
            self.draw_induvidual_cell_noncenter(curseswindow, player_cell, player_cell_corner, west_cell, curses_colour.S_PRIMARY)
        if make_east:
            self.draw_induvidual_cell_noncenter(curseswindow, player_cell, player_cell_corner, east_cell, curses_colour.S_PRIMARY)
        
        # Draw the cells that are visible, but not directly adjacent
		# To save processing power, what's the furthest cell in each direction that can be rendered?
		# First, how many cells can be fit in the window
        #   This will simply be the window size by the cell size.
        #   Then, increase this by 2 in order to ensure the edge cells are displayed
        max_cells_on_page_y = math.floor(window_size[0]/(self.cell_size[0] + self.corridor_length)) + 2
        max_cells_on_page_x = math.floor(window_size[1]/(self.cell_size[1] + self.corridor_length)) + 2
        y_cells_around = math.floor(max_cells_on_page_y/2)+1
        x_cells_around = math.floor(max_cells_on_page_x/2)+1
        # Thus, the first y cell to be printed will be offset from the zeroth cell
        # Limited to be between 0 and self.num_cells[0]
        frst_y_cell = max(0,min(player_cell[0] - y_cells_around,self.num_cells[0]))
        last_y_cell = max(0,min(player_cell[0] + y_cells_around,self.num_cells[0]))
        frst_x_cell = max(0,min(player_cell[1] - x_cells_around,self.num_cells[1]))
        last_x_cell = max(0,min(player_cell[1] + x_cells_around,self.num_cells[1]))
        
        for i_cell_y in range(frst_y_cell,last_y_cell):
            for i_cell_x in range(frst_x_cell,last_x_cell):
                # Do we make this cell?
                #   First, is this a visible cell
                #   Is this not the center cells
                #   Is this not one of the adjacent cells that was rendered?
                this_cell = [i_cell_y, i_cell_x]
                is_north = this_cell == north_cell
                is_south = this_cell == south_cell
                is_west  = this_cell == west_cell
                is_east  = this_cell == east_cell
                is_center = this_cell == player_cell
                # Want:
                #   If it is NOT a particular cardinal direction, 'ok'.
                #   If it is a particular cardinal direction, draw if DIDN'T Make
                # Thus, it's
                #   (!A OR (A AND !B))
                if ((visible_cells[i_cell_y][i_cell_x]) and
                    (not is_center) and
                    ((not is_north) or (is_north and not make_north)) and
                    ((not is_south) or (is_south and not make_south)) and
                    ((not is_west) or (is_west and not make_west)) and
                    ((not is_east) or (is_east and not make_east))):
                    self.draw_induvidual_cell_noncenter(curseswindow, player_cell, player_cell_corner, this_cell, curses_colour.S_SECONDARY)
        
        # Add player
        curseswindow.addch(mid_location[0], mid_location[1], self.player_character, curses.color_pair(self.player_colour))
        
        
if __name__ == "__main__":
    def test_function(stdscr):
        # Cleanup
        stdscr.clear()
        curses.start_color()
        curses_colour.configure_curses_colours()
        stdscr.clear()
    
        stdscr.addstr(0, 0, 'Configuring')
        
        # What is window size?
        lines = curses.LINES
        colms = curses.COLS
        
        edging = 1;
        
        # Make Window
        map_window = curses.newwin(lines - 2*edging, colms - 2*edging,
                                   edging, edging)
        map_window.border()
        
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
        this_map = maze_map(num_cells, link_table, cell_size, corridor_width, corridor_length)
        
        # Write to window
        # Player position is in (5,5)
        this_map.draw_map(map_window, [5, 5])
        
        # Wait
        stdscr.refresh()
        map_window.refresh()
        key = stdscr.getch()
        
        this_map.draw_map(map_window, [5, 6])
        
        # Wait
        stdscr.refresh()
        map_window.refresh()
        key = stdscr.getch()
        
        this_map.draw_map(map_window, [6, 6])
        
        # Wait
        stdscr.refresh()
        map_window.refresh()
        key = stdscr.getch()
        
        this_map.draw_map(map_window, [6, 5])
        
        # Wait
        stdscr.refresh()
        map_window.refresh()
        key = stdscr.getch()
        
        this_map.draw_map(map_window, [7, 5])
        
        # Wait
        stdscr.refresh()
        map_window.refresh()
        key = stdscr.getch()
        this_map.draw_map(map_window, [8, 5])
        
        # Wait
        stdscr.refresh()
        map_window.refresh()
        key = stdscr.getch()
        
        this_map.draw_map(map_window, [9, 5])
        
        # Wait
        stdscr.refresh()
        map_window.refresh()
        key = stdscr.getch()
        
        this_map.draw_map(map_window, [10, 5])
        
        # Wait
        stdscr.refresh()
        map_window.refresh()
        key = stdscr.getch()
        
        this_map.draw_map(map_window, [11, 5])
        
        # Wait
        stdscr.refresh()
        map_window.refresh()
        key = stdscr.getch()
        this_map.draw_map(map_window, [12, 5])
        
        # Wait
        stdscr.refresh()
        map_window.refresh()
        key = stdscr.getch()
        
    curses.wrapper(test_function)
        