# -*- coding: utf-8 -*-

"""
    About Window
"""

import curses
import curses_colour

def load_text():
    textlist = []
    # Text is a list that is slowly output on the launch about window
    textlist.append('What is this?')
    textlist.append('  This is a game made for the Desert Bus Game Jam, based off the Mythology    ')
    textlist.append('  of the Minotaur and the Labryinth. To note, the game gives you a maze,      ')
    textlist.append('  not a true labyrith. Look up ''Labyrinth'' on wikipedia for more information')
    textlist.append('')
    textlist.append('  It was created by chat member ExachixKitsune.')
    textlist.append('')
    textlist.append('What is the Desert Bus Game Jam?')
    textlist.append('  See: https://itch.io/jam/dbgj2019                                           ')
    textlist.append('  This is a game jam that ran at the same time as Desert Bus for Hope 2019.   ')
    textlist.append('  The prompt for the game jam was ''Mythology''.')
    textlist.append('')
    textlist.append('What is Desert Bus for Hope?')
    textlist.append('  See: https://desertbus.org')
    textlist.append('  Desert Bus for Hope (DBFH) is a charity fundraiser where people raise money ')
    textlist.append('  For the charity ''Childs Play''. They take a week to play ''Desert Bus'', while')
    textlist.append('  the cast and crew act, chat, and entertain for donations.')
    textlist.append('')
    textlist.append('Creation of the Game')
    textlist.append('  This game was written in python 3.7. It uses the curses library. It was')
    textlist.append('  compiled using the tool pyinstaller version 3.5.')
    textlist.append('')
    textlist.append('References')
    textlist.append('  The colour definitions were taken from the css definition')
    textlist.append('  Maze Generation Algorithm is Randomized Prim''s, sourced from Wikipedia.')
    textlist.append('  https://en.wikipedia.org/wiki/Maze_generation_algorithm#Randomized_Prim''s_algorithm')
    textlist.append('')
    textlist.append('Irregularities')
    textlist.append('  To note, the player always starts at the top-leftmost cell, and the exit')
    textlist.append('  is always in the lower-right corner. The Dubloons are distributed across')
    textlist.append('  the entire map.')
    textlist.append('  In order to get a consistant pattern in the floor tiles, the character ')
    textlist.append('  for the tile is calculated from the position to appear semi-random.')
    
    # Calculate maxwidth
    maxwidth = 0
    for i_row in range(len(textlist)):
        # How big is this row?
        row_size = len(textlist[i_row])
        # Max Width set
        maxwidth = max(maxwidth, row_size)
    
    return {'textlist':textlist, 'maxwidth':maxwidth}

def render_list(stdscr, y_offset, x_offset):
    
    stdscr.clear()
    
    # What is window size?
    window_size = stdscr.getmaxyx()
    lines = window_size[0]
    colms = window_size[1]
    
    # Load text
    text_data = load_text()
    
    # Top row is always instructions
    stdscr.addstr(0, 0, 'Use arrows to scroll. q or enter to return.',curses.color_pair(curses_colour.S_PRIMARY))
    
    # Number of possible columns onscreen
    # Which is always just less than lines (because of the instructions row)
    # Thus, the first text row.
    # First text row 
    first_text_row = 2
    lines_fortext  = lines - first_text_row
    
    
    # What text is being rendered
    # Fundamentally, render as much the text that you can
    
    # Have n lines of text (len(text_data['textlist']))
    # Can only print m lines of text (lines_fortext)
    # The value new_y_offset is the offset from 0 for the first line printed
    # This has a minimum value of 0
    # and a maximum value of (n-m)
    
    new_y_offset = max(0,min(y_offset,len(text_data['textlist'])-lines_fortext))
    new_x_offset = max(0,min(x_offset,text_data['maxwidth'] - colms))
    # These values are returned to enable responsiveness in the main thread
    
    # Thus, now render the text as appropriate
    # Render from new_y_offset for as many lines as possible.
    # And render each line as appropriate
    top_row_position = first_text_row - new_y_offset
    for i_row in range(len(text_data['textlist'])):
        # Which row on page would this be printed on
        row_to_print_on = top_row_position + i_row
        
        # Only print if we can print
        # That is, is this a row we can print, is it between appropriate bounds:
        if ((first_text_row <= row_to_print_on) and (row_to_print_on < lines)):
            # The text to print is from the new_x_offset to the number of renderable columns after that
            # which is colms
            start_print = new_x_offset;
            end_print = start_print + colms
            text_to_make = text_data['textlist'][i_row][start_print:end_print]
            
            # Output text
            stdscr.addstr(row_to_print_on,0,text_to_make,curses.color_pair(curses_colour.S_PRIMARY))
            
    
    return {'y_offset':new_y_offset, 'x_offset':new_x_offset}

def launch_about(stdscr):
    # Setting setup
    exit_about = False
    y_offset = 0
    x_offset = 0

    while(not exit_about):
        # Render window
        # Always do this. It may be expensive to do, but it's not
        # that slow and makes sure nothing gets broken
        newloc = render_list(stdscr,y_offset,x_offset)
        y_offset = newloc['y_offset']
        x_offset = newloc['x_offset']
        
        # Wait for key
        key = stdscr.getch()
        
        # Handle key
        if ((key == ord('w')) or (key == curses.KEY_UP)):
            y_offset -= 1
        elif ((key == ord('s')) or (key == curses.KEY_DOWN)):
            y_offset += 1
        elif ((key == ord('a')) or (key == curses.KEY_LEFT)):
            x_offset -= 1
        elif ((key == ord('d')) or (key == curses.KEY_RIGHT)):
            x_offset += 1
        elif ((key == ord('q')) or (key == curses.KEY_ENTER) or (key == 10) or (key == 459)):
            # ENTER key is either key 10 or 459 (normal or numpad).
            exit_about = True
            break
    
    # Clear
    stdscr.clear()
