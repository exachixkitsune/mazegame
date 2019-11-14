# -*- coding: utf-8 -*-
'''
    Primary section to play the game
'''

import curses
import curses_colour
import setup_map
import traceback
import math

KEY_MOVEUP = 'w'
KEY_MOVELEFT = 'a'
KEY_MOVEDOWN = 's'
KEY_MOVERIGHT = 'd'
KEY_COLOURCHANGE = 'c'
KEY_EXIT = 'q'

def window_setup(stdscr):
    # Empty
    stdscr.clear()
    stdscr.bkgd(curses.color_pair(curses_colour.S_BACKGROUND))
    
    # What is window size?
    window_size = stdscr.getmaxyx()
    lines = window_size[0]
    colms = window_size[1]
    
    window_edging = 1;
    
    curses.curs_set(0)
    
    # 2 windows,
    # on the left and right
    # window2 is at most 50 big.
    # Make it.
    max_window2_size = 50
    divider = colms - max_window2_size
    
    # Make Window
    map_window = curses.newwin(lines - 2*window_edging, divider - 2*window_edging,
                               window_edging, window_edging)
    map_window.refresh()
    map_window.bkgd(curses.color_pair(curses_colour.S_BACKGROUND))
    
    # Make second window, with details on what's going on
    info_window = curses.newwin(lines - 2*window_edging, colms - divider -2*window_edging,
                                window_edging, divider+window_edging)
    info_window.bkgd(curses.color_pair(curses_colour.S_BACKGROUND))
    
    #stdscr.addstr(0, 50, 'Window Sized {}x{}'.format(lines, colms))
    
    return {'map_window':map_window, 'info_window':info_window}

def setup_info_window(info_window, this_world, max_money):    
    # Desired Text
    line_data = []
    line_cols = []
    
    line_data.append(['Maze Game'])
    line_cols.append([curses_colour.S_PRIMARY])
    
    line_data.append([''])
    line_cols.append([curses_colour.S_PRIMARY])
    
    line_data.append(['Primary Objective'])
    line_cols.append([curses_colour.S_PRIMARY])
    
    line_data.append(['  Move your marker to the exit marker.'])
    line_cols.append([curses_colour.S_PRIMARY])
    
    line_data.append(['Secondary Objective'])
    line_cols.append([curses_colour.S_PRIMARY])
    
    line_data.append(['  Collect the Dubloons'])
    line_cols.append([curses_colour.S_PRIMARY])
    
    line_data.append(['  Currently got {} / {}'.format(this_world.score,max_money)])
    line_cols.append([curses_colour.S_PRIMARY])
    
    line_data.append([''])
    line_cols.append([curses_colour.S_PRIMARY])
    
    line_data.append(['Controls'])
    line_cols.append([curses_colour.S_PRIMARY])
    
    line_data.append(['  [', KEY_MOVEUP, '] or [', 'UP', ']    - Up'])
    line_cols.append([curses_colour.S_PRIMARY, curses_colour.S_KEYMARK, curses_colour.S_PRIMARY, curses_colour.S_KEYMARK, curses_colour.S_PRIMARY])

    line_data.append(['  [', KEY_MOVELEFT, '] or [', 'LEFT', ']  - Left'])
    line_cols.append([curses_colour.S_PRIMARY, curses_colour.S_KEYMARK, curses_colour.S_PRIMARY, curses_colour.S_KEYMARK, curses_colour.S_PRIMARY])

    line_data.append(['  [', KEY_MOVEDOWN, '] or [', 'DOWN', ']  - Down'])
    line_cols.append([curses_colour.S_PRIMARY, curses_colour.S_KEYMARK, curses_colour.S_PRIMARY, curses_colour.S_KEYMARK, curses_colour.S_PRIMARY])

    line_data.append(['  [', KEY_MOVERIGHT, '] or [', 'RIGHT', '] - Right'])
    line_cols.append([curses_colour.S_PRIMARY, curses_colour.S_KEYMARK, curses_colour.S_PRIMARY, curses_colour.S_KEYMARK, curses_colour.S_PRIMARY])

    line_data.append(['  [', KEY_COLOURCHANGE, ']            - Change Colour Mode'])
    line_cols.append([curses_colour.S_PRIMARY, curses_colour.S_KEYMARK, curses_colour.S_PRIMARY])

    line_data.append(['  [', KEY_EXIT, '] or [', 'ESC', ']   - Exit'])
    line_cols.append([curses_colour.S_PRIMARY, curses_colour.S_KEYMARK, curses_colour.S_PRIMARY, curses_colour.S_KEYMARK, curses_colour.S_PRIMARY])

    line_data.append([''])
    line_cols.append([curses_colour.S_PRIMARY])
    
    line_data.append(['Points of Interest'])
    line_cols.append([curses_colour.S_PRIMARY])
    
    line_data.append(['  ', this_world.maze.player_character, ' - Player Marker'])
    line_cols.append([curses_colour.S_PRIMARY, this_world.maze.player_colour, curses_colour.S_PRIMARY])
    
    line_data.append(['  ', setup_map.game_world.maze_map.OBJ_STAIRS_CHAR, ' - Exit'])
    line_cols.append([curses_colour.S_PRIMARY, setup_map.game_world.maze_map.OBJ_STAIRS_COLR, curses_colour.S_PRIMARY])
    
    line_data.append(['  ', setup_map.game_world.maze_map.OBJ_MONEY_CHAR, ' - Dubloon'])
    line_cols.append([curses_colour.S_PRIMARY, setup_map.game_world.maze_map.OBJ_MONEY_COLR, curses_colour.S_PRIMARY])
    
    # Add window border
    info_window.border()
    
    # Print out!
    initial_x = 2
    initial_y = 2
    for i_line in range(len(line_data)):
        current_y = initial_y + i_line
        current_x = initial_x
        for i_part in range(len(line_data[i_line])):
            # Make
            info_window.addstr(current_y, current_x, line_data[i_line][i_part], curses.color_pair(line_cols[i_line][i_part]))
            current_x += len(line_data[i_line][i_part])
    
    info_window.refresh()
    
def setup_curses(stdscr):
    # window setup
    windows = window_setup(stdscr)
    
    return {'map_window':windows['map_window'], 'info_window':windows['info_window']}

def victory_screen(stdscr,this_world,max_score):
    stdscr.clear()
    # What is window size?
    window_size = stdscr.getmaxyx()
    lines = window_size[0]
    colms = window_size[1]
    # Middle line
    middle_line = math.floor(lines/2)
    # middle colm
    middle_colm = math.floor(colms/2)
    # Text
    text_1 = 'Congratulations, you have completed the maze!'
    text_2 = 'You collected {} out of {} Dubloons.'.format(this_world.score,max_score)
    text_3 = 'Press any key to return to menu.'
    # Offset
    text_1_offset = math.floor(len(text_1)/2)
    text_2_offset = math.floor(len(text_2)/2)
    text_3_offset = math.floor(len(text_3)/2)
    # Output
    stdscr.addstr(middle_line  , middle_colm - text_1_offset, text_1, curses.color_pair(curses_colour.S_PRIMARY))
    stdscr.addstr(middle_line+1, middle_colm - text_2_offset, text_2, curses.color_pair(curses_colour.S_PRIMARY))
    stdscr.addstr(middle_line+2, middle_colm - text_3_offset, text_3, curses.color_pair(curses_colour.S_PRIMARY))
    # Refresh
    stdscr.refresh()
    # Wait for key
    key = stdscr.getch()
    while (key == curses.KEY_RESIZE):
        key = stdscr.getch()

def game_main(stdscr, this_world, settings_dict):
    # Maximum score is the number of money objects in the list
    max_score = 0
    for i_obj in range(len(this_world.maze.objects_list)):
        if (this_world.maze.objects_list[i_obj][1] == setup_map.game_world.maze_map.CELLINDX_MONEY):
            max_score += 1
    # Run main setup
    curses_objects = setup_curses(stdscr)
    setup_info_window(curses_objects['info_window'], this_world, max_score)
    
    # Refresh here in this order
    stdscr.refresh()
    curses_objects['map_window'].refresh()
    curses_objects['info_window'].refresh()
    
    #stdscr.addstr(0, 0, 'Playing     ')
    
    # Run Main Game loop
    while (True):
        # Render Image
        this_world.render(curses_objects['map_window'])
        setup_info_window(curses_objects['info_window'], this_world, max_score)
        stdscr.refresh()
        curses_objects['map_window'].refresh()
        
        # Await key input
        key = stdscr.getch()
        
        # Interpret key input -> Operation
        if ((key == ord(KEY_MOVEUP)) or (key == curses.KEY_UP)):
            this_world.move_player(3)
        elif ((key == ord(KEY_MOVELEFT)) or (key == curses.KEY_LEFT)):
            this_world.move_player(2)
        elif ((key == ord(KEY_MOVEDOWN)) or (key == curses.KEY_DOWN)):
            this_world.move_player(1)
        elif ((key == ord(KEY_MOVERIGHT)) or (key == curses.KEY_RIGHT)):
            this_world.move_player(0)
        elif ((key == ord(KEY_EXIT)) or (key == 27)):
            break
        elif (key == ord(KEY_COLOURCHANGE)):
            # Change colour setting!
            # Rotate the colour setting
            settings_dict['colour_mode'] = (settings_dict['colour_mode'] + 1) % curses_colour.NUM_COLOURMODES
            # Set colourmode
            curses_colour.configure_curses_colours_special(settings_dict['colour_mode'])
            # Reload curses object
            curses_objects = window_setup(stdscr)
            setup_info_window(curses_objects['info_window'], this_world, max_score)
            
        elif (key == curses.KEY_RESIZE):
            # Resized window. Regenerate windows
            # Remove previous window
            curses_objects['map_window'] = []
            # Make a new window
            curses_objects = window_setup(stdscr)
            setup_info_window(curses_objects['info_window'], this_world, max_score)
            
        # Do World update
        this_world.world_check()
        
        if this_world.victory:
            stdscr.refresh()
            victory_screen(stdscr,this_world,max_score)
            break
        
        stdscr.refresh()
    
    # Re-give settings dictionary to source
    return settings_dict

if (__name__ == '__main__'):
    
    def run_testmode(stdscr, this_world):
        # Cleanup
        stdscr.clear()
        curses.start_color()
        curses_colour.configure_curses_colours()
        stdscr.clear()
        
        game_main(stdscr, this_world)

    try:
        this_world = setup_map.fixed_map()
        curses.wrapper(run_testmode, this_world)
    except Exception as e:
        print('Error occured')
        print(type(e))
        print(e.args)
        tb = traceback.format_exc()
        print(tb)
        input('Press Enter to continue...')