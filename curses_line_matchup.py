# -*- coding: utf-8 -*-
"""
    Works out what character to use for joining lines up
    in python curses
"""

import curses

def curses_line_matchup(north, east, south, west):
    # Function that works out which line function to use
    # Given lines go from any direction.
    list_of_dir = [north, east, south, west]
    result_char = 0;
    
    # Take action based off the number of dimensions
    if (sum(list_of_dir) <= 1):
        # Not enough for a full direction
        # Resolve into 'pillar' character
        result_char = curses.ACS_DIAMOND
    elif (sum(list_of_dir) == 2):
        # Here, there's the chance there could be a line or a corner
        # Sort it by these 2 groups
        if (north and south):
            result_char = curses.ACS_SBSB
        elif (east and west):
            result_char = curses.ACS_BSBS
        else:
            # Corner set
            if (north and east):
                result_char = curses.ACS_LLCORNER
            elif (east and south):
                result_char = curses.ACS_ULCORNER
            elif (south and west):
                result_char = curses.ACS_URCORNER
            else:
                result_char = curses.ACS_LRCORNER
    elif (sum(list_of_dir) == 3):
        # Which set of 3 is this?
        if not north:
            result_char = curses.ACS_TTEE
        elif not east:
            result_char = curses.ACS_RTEE
        elif not south:
            result_char = curses.ACS_BTEE
        else:
            # note must be west
            result_char = curses.ACS_LTEE
    else:
        # It's 4.
        result_char = curses.ACS_PLUS
        
    return result_char

def curses_line_matchup_arr(array):
    return curses_line_matchup(array[0], array[1], array[2], array[3])

