# -*- coding: utf-8 -*-
"""
Menu Window
"""

import curses
import curses_colour
import game_main
import traceback
import math
import setup_map
import about_window

def window_setup(stdscr):
    # Do both starting colour and configure the colours
    curses.start_color()
    curses_colour.configure_curses_colours()
    # Setup default colour for terminal output
    stdscr.bkgd(curses.color_pair(curses_colour.S_BACKGROUND))   

def render_menu(stdscr,option_text,option_at):
    # Render the Menu
    
    # 4 options
    #  1 - Load a default map
    #  2 - Load a map of user-defined size
    #       - Submenu, gives the size of the map
    #  3 - About
    #       - Displays information about the DB Game Jam, Desert Bus, and 
    #         the game itself
    #  4 - Exit
    
    stdscr.clear()
    
    # What is window size?
    window_size = stdscr.getmaxyx()
    lines = window_size[0]
    colms = window_size[1]
    # Middle line
    middle_line = math.floor(lines/2)
    # middle colm
    middle_colm = math.floor(colms/2)
    
    # Arrange text in the middle
    
    
    title_text = []
    title_text.append('Maze Game')
    title_text.append('version 1.0')
    title_text.append('Created by exachixkitsune, for the Desert Bus Game Jam')
        
    # Followon text
    followon_text = []
    followon_colr = []
    followon_text.append(['Press [', 'UP', '] and [', 'DOWN', '] to select.'])
    followon_colr.append([curses_colour.S_PRIMARY, curses_colour.S_KEYMARK, curses_colour.S_PRIMARY, curses_colour.S_KEYMARK, curses_colour.S_PRIMARY])
    followon_text.append(['Then enter to continue.'])
    followon_colr.append([curses_colour.S_PRIMARY])
    
    # Total rows
    # Title rows, 1 spacer of the title, and 2 rows per option
    spacer_size = 1
    total_rows = len(title_text) + spacer_size + len(option_text)*2 + spacer_size + len(followon_text)
    
    # Write titles
    first_row = middle_line - math.floor(total_rows/2)
    for i_title in range(len(title_text)):
        this_text = title_text[i_title]
        # Horizontal offset
        hor_start = middle_colm - math.floor(len(this_text)/2)
        # Write it
        stdscr.addstr(first_row + i_title, hor_start, this_text, curses.color_pair(curses_colour.S_PRIMARY))
    
    # Write Options
    first_row += len(title_text) + spacer_size
    # Find Max Widths
    maxlen = 0
    for i_opt in range(len(option_text)):
        maxlen = max(maxlen,len(option_text[i_opt]))
    # Horizontal offset
    hor_start_opt = middle_colm - math.floor((maxlen+4)/2)
    for i_opt in range(len(option_text)):
        # Put element
        this_text = '[ ] ' + option_text[i_opt]
        this_row = first_row + (i_opt*2) + 1
        # Insert
        stdscr.addstr(this_row, hor_start_opt, this_text, curses.color_pair(curses_colour.S_PRIMARY))
        
    # Add current option count
    if (0 <= option_at) and (option_at < len(option_text)):
        option_row = first_row + (option_at*2) + 1
        stdscr.addstr(option_row, hor_start_opt+1, 'x', curses.color_pair(curses_colour.S_FEATURE_2))    
        
    # Followon
    first_row += len(option_text)*2
    first_row += spacer_size
    # Write Followon
    for i_text in range(len(followon_text)):
        this_row = first_row + i_text
        this_text = followon_text[i_text]
        this_colr = followon_colr[i_text]
        # Horizontal offset
        #   Get size of element
        full_text_size = 0
        for i_element in range(len(this_text)):
            full_text_size += len(this_text[i_element])
        # Make horizontal offset to center text
        hor_start = middle_colm - math.floor(full_text_size/2)
        current_hor = hor_start
        # Write each sub-bit
        for i_element in range(len(this_text)):
            stdscr.addstr(this_row, current_hor, this_text[i_element], curses.color_pair(this_colr[i_element]))
            current_hor += len(this_text[i_element])
    
    curses.curs_set(0)
    
    stdscr.refresh()
    
def launch_game(stdscr, world, settings_dict):
    stdscr.clear()
    try:
        settings_dict = game_main.game_main(stdscr,world, settings_dict)
    except Exception as e:
        curses.reset_shell_mode()
        print('Error occured')
        print(type(e))
        print(e.args)
        tb = traceback.format_exc()
        print(tb)
        print('')
        print('I''m sorry =(. Thank you for playing though.')
        print('')
        print('Typical things that cause this are:')
        print('  > Resizing the window to be too small')
        print('Please don''t do these things')
        input('Press Enter to continue, and the game will return to the main menu.')
        curses.reset_prog_mode()
    finally:
        # Then reboot main setup
        window_setup(stdscr)
        
    # Return the settings dictionary
    return settings_dict
        
def render_settings_window(stdscr, selected_opt):
    # Tidy
    stdscr.clear()
    
    y_offset = 2
    x_offset = 2
    
    
    # Colour title
    colour_title = 'Set Colour Mode'
    stdscr.addstr(y_offset, x_offset, colour_title,curses.color_pair(curses_colour.S_PRIMARY))    
    
    preview_special_set = [curses.ACS_DIAMOND, curses.ACS_SBSB, curses.ACS_BSBS, curses.ACS_LLCORNER,
                   curses.ACS_ULCORNER, curses.ACS_URCORNER, curses.ACS_LRCORNER, curses.ACS_TTEE,
                   curses.ACS_RTEE, curses.ACS_BTEE, curses.ACS_LTEE, curses.ACS_PLUS,
                   ' ',' ','.',',',183,184,176,96,722,723]
    first_upper_char = 65
    first_lower_char = 97
    first_num_char = 48
    
    colour_titles = []
    colour_titles.append('Default Mode (White-On-Black)')
    colour_titles.append('Slate Background (White-On-Slate)')
    colour_titles.append('Light Background (Black-On-Light Gray)')
    colour_titles.append('White Background (Black-On-White)')
    
    # Which colour is selected
    # Limit to being between 0 and the maximum colour_title.
    selected_opt = max(0,min(selected_opt,len(colour_titles)-1))
    
    
    # Set up Settings options
    y_colourrow_offset = y_offset + 2
    x_colourrow_offset = x_offset + 1
    
    # Write each row
    for i_colour in range(len(colour_titles)):
        stdscr.addstr(y_colourrow_offset + i_colour, x_colourrow_offset, '[ ] '+colour_titles[i_colour], curses.color_pair(curses_colour.S_PRIMARY))
    
    # Return the selected option
    stdscr.addch(y_colourrow_offset + selected_opt, x_colourrow_offset+1, 'x', curses.color_pair(curses_colour.S_FEATURE_2))
    
    
    # Create preview list
    y_preview_offset = y_colourrow_offset + len(colour_titles) + 1
    
    colours_to_use = [curses_colour.S_PRIMARY, curses_colour.S_SECONDARY]
    for i_colour_used in range(len(colours_to_use)):
        current_y = y_preview_offset + i_colour_used*2
        current_x = x_colourrow_offset
        # Do each special character
        for i_char in range(len(preview_special_set)):
            stdscr.addch(current_y, current_x+i_char, preview_special_set[i_char], curses.color_pair(colours_to_use[i_colour_used]))
        # Do each number, on row 2
        for i_num in range(10):
            stdscr.addch(current_y+1, current_x+i_num, first_num_char+i_num, curses.color_pair(colours_to_use[i_colour_used]))
        current_x += max(len(preview_special_set),10)
        # Do each character
        for i_char in range(26):
            stdscr.addch(current_y  , current_x+i_char, first_upper_char+i_char, curses.color_pair(colours_to_use[i_colour_used]))
            stdscr.addch(current_y+1, current_x+i_char, first_lower_char+i_char, curses.color_pair(colours_to_use[i_colour_used]))
            
    # Do only some special in some set.
    stdscr.addch(current_y+2, current_x, game_main.setup_map.game_world.maze_map.OBJ_PLAYER_CHAR, curses.color_pair(curses_colour.S_FEATURE_1)); current_x += 1;
    stdscr.addch(current_y+2, current_x, game_main.setup_map.game_world.maze_map.OBJ_STAIRS_CHAR, curses.color_pair(game_main.setup_map.game_world.maze_map.OBJ_STAIRS_COLR)); current_x += 1;
    stdscr.addch(current_y+2, current_x, game_main.setup_map.game_world.maze_map.OBJ_MONEY_CHAR, curses.color_pair(game_main.setup_map.game_world.maze_map.OBJ_MONEY_COLR)); current_x += 1;
    
    # Instructions
    y_instruction_row = y_preview_offset + len(colours_to_use)*2 + 2
    x_instruction_row = x_offset
    control_row_text = ['Use [', 'UP', '] and [', 'DOWN', '] to select. [', 'ENTER', '] to save. ']
    control_row_colm = [curses_colour.S_PRIMARY, curses_colour.S_KEYMARK,
                        curses_colour.S_PRIMARY, curses_colour.S_KEYMARK,
                        curses_colour.S_PRIMARY, curses_colour.S_KEYMARK, curses_colour.S_PRIMARY]
    current_x = x_instruction_row
    for i_control in range(len(control_row_text)):
        stdscr.addstr(y_instruction_row, current_x, control_row_text[i_control], curses.color_pair(control_row_colm[i_control]))
        current_x += len(control_row_text[i_control])
    
    return selected_opt

def settings_menu(stdscr,settings_dict):
    still_setting = True
    current_option = settings_dict['colour_mode']
    
    while (still_setting):
        curses_colour.configure_curses_colours_special(current_option)
        # Render
        current_option = render_settings_window(stdscr, current_option)
        
        # Await input
        key = stdscr.getch()
        
        # Interpret input
        if ((key == ord('w')) or (key == curses.KEY_UP)):
            current_option -= 1
        elif ((key == ord('s')) or (key == curses.KEY_DOWN)):
            current_option += 1
        elif ((key == curses.KEY_ENTER) or (key == 10) or (key == 459)):
            # Stop
            still_setting = False
            break
        
    settings_dict['colour_mode'] = current_option
    
    return settings_dict

def render_size_select(stdscr,map_size,money_count):
    stdscr.clear()
    
    # Map Cells
    total_cells = map_size[0]*map_size[1]
    max_money = (total_cells-2)
    
    # Render the size selection menu.
    text = []
    text.append(['Select the map size, and the amount of Dubloons in the maze.'])
    text.append(['  Use [', 'UP', '] and [', 'DOWN', '] to select the vertical size. (Minumim 2)'])
    text.append(['  Use [', 'LEFT', '] and [', 'RIGHT', '] to select the horizontal size. (Minimum 2)'])
    text.append(['  Use [', ',', '] and [', '.', '] to select the number of Dubloons. (Maximum {})'.format(max_money)])
    text.append(['  Use [', 'ENTER', '] to accept changes and play.'])
    text.append(['  Use [', 'q', '] to go back to the menu.'])
    text.append([''])
    text.append(['  Size is ', '{}'.format(map_size[0]), ' by ', '{}'.format(map_size[1]), '.'])
    text.append(['  ', '{}'.format(money_count), ' Dubloons'])
    text.append([''])
    
    colours = []
    colours.append([curses_colour.S_PRIMARY])
    colours.append([curses_colour.S_PRIMARY, curses_colour.S_KEYMARK, curses_colour.S_PRIMARY, curses_colour.S_KEYMARK, curses_colour.S_PRIMARY])
    colours.append([curses_colour.S_PRIMARY, curses_colour.S_KEYMARK, curses_colour.S_PRIMARY, curses_colour.S_KEYMARK, curses_colour.S_PRIMARY])
    colours.append([curses_colour.S_PRIMARY, curses_colour.S_KEYMARK, curses_colour.S_PRIMARY, curses_colour.S_KEYMARK, curses_colour.S_PRIMARY])
    colours.append([curses_colour.S_PRIMARY, curses_colour.S_KEYMARK, curses_colour.S_PRIMARY])
    colours.append([curses_colour.S_PRIMARY, curses_colour.S_KEYMARK, curses_colour.S_PRIMARY])
    colours.append([curses_colour.S_PRIMARY])
    colours.append([curses_colour.S_PRIMARY, curses_colour.S_FEATURE_2, curses_colour.S_PRIMARY, curses_colour.S_FEATURE_2, curses_colour.S_PRIMARY])
    colours.append([curses_colour.S_PRIMARY, curses_colour.S_FEATURE_2, curses_colour.S_PRIMARY])
    colours.append([curses_colour.S_PRIMARY])
    
    # Add Warnings
    if (max_money < money_count):
        text.append(['WARNING', ': The number of dubloons ({}) exceeds the maximum number ({}).'.format(money_count,max_money)])
        text.append(['       ', '  There is a maximum of one Dubloon per cell, ignoring the starting cell and'])
        text.append(['       ', '  the exit cell. Only ', '{}'.format(max_money), ' Dubloons will be used.'])
        colours.append([curses_colour.S_FEATURE_3, curses_colour.S_PRIMARY])
        colours.append([curses_colour.S_PRIMARY, curses_colour.S_PRIMARY])
        colours.append([curses_colour.S_PRIMARY, curses_colour.S_PRIMARY, curses_colour.S_FEATURE_3, curses_colour.S_PRIMARY])
    if (total_cells > 25*25):
        text.append(['ALERT  ', ': The current map size will make a map with {} cells'.format(total_cells)])
        text.append(['       ', '  The game will still run. The larger the maze size, the longer the maze will'])
        text.append(['       ', '  take to generate and solve. Large mazes MAY cause problems on some computers.'])
        colours.append([curses_colour.S_FEATURE_4, curses_colour.S_PRIMARY])
        colours.append([curses_colour.S_PRIMARY, curses_colour.S_PRIMARY])
        colours.append([curses_colour.S_PRIMARY, curses_colour.S_PRIMARY])
    
    y_offset = 2
    x_offset = 2
    
    # Write each line
    for i_line in range(len(text)):
        this_line = text[i_line]
        this_colr = colours[i_line]
        current_x = x_offset
        current_y = y_offset + i_line
        for i_part in range(len(this_line)):
            stdscr.addstr(current_y, current_x, this_line[i_part], curses.color_pair(this_colr[i_part]))
            current_x += len(this_line[i_part])
    
def size_select(stdscr,map_size,money_count):
    keep_selecting = True
    
    this_map_size = map_size.copy()
    this_money_count = money_count
    play_game = False
    
    while(keep_selecting):
        # Define minimums
        this_map_size[0] = max(this_map_size[0],2)
        this_map_size[1] = max(this_map_size[1],2)
        this_money_count = max(this_money_count,0)
        
        # Render
        render_size_select(stdscr,this_map_size,this_money_count)
        # Wait for Key
        key = stdscr.getch()
        # Select option
        
        # Interpret key input -> Operation
        if ((key == ord('w')) or (key == curses.KEY_UP)):
            this_map_size[0] += 1
        elif ((key == ord('s')) or (key == curses.KEY_DOWN)):
            this_map_size[0] -= 1
        elif ((key == ord('a')) or (key == curses.KEY_LEFT)):
            this_map_size[1] -= 1
        elif ((key == ord('d')) or (key == curses.KEY_RIGHT)):
            this_map_size[1] += 1
        elif ((key == ord(','))):
            this_money_count -= 1
        elif ((key == ord('.'))):
            this_money_count += 1
        elif ((key == ord('q')) or (key == 27)):
            keep_selecting = False
            break
        elif ((key == curses.KEY_ENTER) or (key == 10) or (key == 459)):
            play_game = True
            keep_selecting = False
            break
    
    return {'new_map_size':this_map_size,
            'this_money_count':this_money_count,
            'play_game':play_game}
        
    
    
def main(stdscr):
    # Startup
    window_setup(stdscr)
    # Configure for the first time
    option_at = 0
    continue_menu = True
    
    settings_dict = {'colour_mode':0}
    
    fixed_map_size = [10,10]
    default_money = 10
    
    # Text Setup
    # All text rows are '[x] - Option Name'
    option_text = []
    option_text.append('Make Random map of default size ({}x{}, {} dubloons)'.format(fixed_map_size[0],fixed_map_size[1],default_money))
    option_text.append('Make fixed test map (4x4)')
    option_text.append('Make Random map of user defined size.')
    option_text.append('Settings')
    option_text.append('About')
    option_text.append('Exit')
    
    key = 0
    
    while(continue_menu):
        # Render window for the first time
        render_menu(stdscr,option_text,option_at)
        # Renew colour settings
        curses_colour.configure_curses_colours_special(settings_dict['colour_mode'])
        
        # Await key input
        key = stdscr.getch()
        
        # Interpret input
        if ((key == ord('w')) or (key == curses.KEY_UP)):
            option_at -= 1
        elif ((key == ord('s')) or (key == curses.KEY_DOWN)):
            option_at += 1
        elif ((key == curses.KEY_ENTER) or (key == 10) or (key == 459)):
            # ENTER key is either key 10 or 459 (normal or numpad).
            # Depending on the current option, do a different thing
            if option_at == 0:
                # Use default map size
                this_world = setup_map.random_map(fixed_map_size,default_money)
                settings_dict = launch_game(stdscr,this_world,settings_dict)
            elif option_at == 1:
                # Use Test Map
                this_world = setup_map.fixed_map()
                settings_dict = launch_game(stdscr,this_world,settings_dict)
            elif option_at == 2:
                # Open window to make the new map
                # Select the size
                size_options = size_select(stdscr,fixed_map_size,default_money)
                # If playing game, play
                if size_options['play_game']:
                    this_world = setup_map.random_map(size_options['new_map_size'],size_options['this_money_count'])
                    settings_dict = launch_game(stdscr,this_world,settings_dict)
            elif option_at == 3:
                # Load settings menu
                settings_dict = settings_menu(stdscr,settings_dict)
            elif option_at == 4:
                # Launch about window
                about_window.launch_about(stdscr)
                
            elif option_at == 5:
                # End
                continue_menu = False
                break
            
        
        # Reset option value
        # Limit to between 0 and len(option_text)-1
        option_at = max(0,min(option_at,len(option_text)-1))
        
    
    
    
if (__name__ == '__main__'):
    try:
        curses.wrapper(main)
    except Exception as e:
        print('Error occured')
        print(type(e))
        print(e.args)
        tb = traceback.format_exc()
        print(tb)
        print('')
        print('I''m sorry =(. Thank you for playing though.')
        print('')
        print('Typical things that cause this are:')
        print('  > Resizing the window to be too small')
        print('      This may suddenly occur as it changes windows, as certain windows need to be certain sizes.')
        input('Press Enter to continue, and the game will end.')