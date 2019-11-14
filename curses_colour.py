# -*- coding: utf-8 -*-
'''
Configuration of colours for Curses
'''

import curses
import math

P_RED_BLACK = 1
P_GREEN_BLACK = 2
P_BLUE_BLACK = 3
P_CYAN_BLACK = 4
P_MAGENTA_BLACK = 5
P_YELLOW_BLACK = 6
P_WHITE_BLACK = 7

P_LIGHTGRAY_BLACK = 8
P_DARKGRAY_BLACK = 9
P_LIGHTSLATEGRAY_BLACK = 10
P_SLATEGRAY_BLACK = 11
P_DARKSLATEGRAY_BLACK = 12

S_BACKGROUND = 20
S_PRIMARY = 21
S_SECONDARY = 22
S_FEATURE_1 = 23
S_FEATURE_2 = 24
S_FEATURE_3 = 25
S_FEATURE_4 = 26
S_KEYMARK = 27

C_LIGHTGRAY = 8
C_DARKGRAY = 9
C_LIGHTSLATEGRAY = 10
C_SLATEGRAY = 11
C_DARKSLATEGRAY = 12
C_GOLD = 13
C_OLIVE = 14
C_SKYBLUE = 15

NUM_COLOURMODES = 4

def convval(val):
    # Converts number from interval [0:256] to interval [0:1000]
    return math.trunc(val*(1000/256))

def configure_curses_colours():
    # Set up bespoke colours
    curses.init_color(C_LIGHTGRAY, convval(211), convval(211), convval(211))
    curses.init_color(C_DARKGRAY, convval(169), convval(169), convval(169))
    curses.init_color(C_LIGHTSLATEGRAY, convval(119), convval(136), convval(153))
    curses.init_color(C_SLATEGRAY, convval(112), convval(128), convval(144))
    curses.init_color(C_DARKSLATEGRAY, convval(47), convval(79), convval(79))
    curses.init_color(C_GOLD, convval(255), convval(215), convval(0))
    curses.init_color(C_OLIVE, convval(128), convval(128), convval(0))
    curses.init_color(C_SKYBLUE, convval(135), convval(206), convval(235))
    
    # Set up colour pairs
    curses.init_pair(P_RED_BLACK, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(P_GREEN_BLACK, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(P_BLUE_BLACK, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(P_CYAN_BLACK, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(P_MAGENTA_BLACK, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(P_YELLOW_BLACK, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(P_WHITE_BLACK, curses.COLOR_WHITE, curses.COLOR_BLACK)
    
    # Setup some bespoke colour pairs
    curses.init_pair(P_LIGHTGRAY_BLACK, C_LIGHTGRAY, curses.COLOR_BLACK)
    curses.init_pair(P_DARKGRAY_BLACK, C_DARKGRAY, curses.COLOR_BLACK)
    curses.init_pair(P_LIGHTSLATEGRAY_BLACK, C_LIGHTSLATEGRAY, curses.COLOR_BLACK)
    curses.init_pair(P_SLATEGRAY_BLACK, C_SLATEGRAY, curses.COLOR_BLACK)
    curses.init_pair(P_DARKSLATEGRAY_BLACK, C_DARKSLATEGRAY, curses.COLOR_BLACK)
    
	# Default special colours configuration
    configure_curses_colours_special()
    
def configure_curses_colours_special(colour_mode=0):
    # Normal Colour Mode - background stuff
    # When changing this, be sure to change NUM_COLOURMODES
    if (colour_mode == 1):
        # Colour with a dark slate background
        curses.init_pair(S_BACKGROUND,  curses.COLOR_WHITE, C_DARKSLATEGRAY)
        curses.init_pair(S_PRIMARY,     curses.COLOR_WHITE, C_DARKSLATEGRAY)
        curses.init_pair(S_SECONDARY,   C_SLATEGRAY,        C_DARKSLATEGRAY)
        curses.init_pair(S_FEATURE_1,   C_SKYBLUE,          C_DARKSLATEGRAY)
        curses.init_pair(S_FEATURE_2,   curses.COLOR_GREEN, C_DARKSLATEGRAY)
        curses.init_pair(S_FEATURE_3,   curses.COLOR_RED,   C_DARKSLATEGRAY)
        curses.init_pair(S_FEATURE_4,   C_GOLD,             C_DARKSLATEGRAY)
        curses.init_pair(S_KEYMARK,     curses.COLOR_GREEN, C_DARKSLATEGRAY)
    elif (colour_mode == 2):
        # Light Gray background
        curses.init_pair(S_BACKGROUND,  curses.COLOR_BLACK, C_LIGHTGRAY)
        curses.init_pair(S_PRIMARY,     curses.COLOR_BLACK, C_LIGHTGRAY)
        curses.init_pair(S_SECONDARY,   C_SLATEGRAY,        C_LIGHTGRAY)
        curses.init_pair(S_FEATURE_1,   curses.COLOR_BLUE,  C_LIGHTGRAY)
        curses.init_pair(S_FEATURE_2,   curses.COLOR_GREEN, C_LIGHTGRAY)
        curses.init_pair(S_FEATURE_3,   curses.COLOR_RED,   C_LIGHTGRAY)
        #curses.init_pair(S_FEATURE_4,   C_GOLD,             C_LIGHTGRAY)
        curses.init_pair(S_KEYMARK,     curses.COLOR_GREEN, C_LIGHTGRAY)
        # Special; GOLD is not very good in this mode. It will become 
        curses.init_pair(S_FEATURE_4,   C_OLIVE,       C_LIGHTGRAY)
    elif (colour_mode == 3):
        # White background
        curses.init_pair(S_BACKGROUND,  curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(S_PRIMARY,     curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(S_SECONDARY,   C_SLATEGRAY,        curses.COLOR_WHITE)
        curses.init_pair(S_FEATURE_1,   curses.COLOR_BLUE,  curses.COLOR_WHITE)
        curses.init_pair(S_FEATURE_2,   curses.COLOR_GREEN, curses.COLOR_WHITE)
        curses.init_pair(S_FEATURE_3,   curses.COLOR_RED,   curses.COLOR_WHITE)
        #curses.init_pair(S_FEATURE_4,   C_GOLD,             curses.COLOR_WHITE)
        curses.init_pair(S_KEYMARK,     curses.COLOR_GREEN, curses.COLOR_WHITE)
        # Special; GOLD is not very good in this mode. It will become 
        curses.init_pair(S_FEATURE_4,   C_OLIVE,       curses.COLOR_WHITE)
        
    else:
        # This is normal stuff on normal background
        curses.init_pair(S_BACKGROUND,  curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(S_PRIMARY,     curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(S_SECONDARY,   C_SLATEGRAY,        curses.COLOR_BLACK)
        curses.init_pair(S_FEATURE_1,   curses.COLOR_BLUE,  curses.COLOR_BLACK)
        curses.init_pair(S_FEATURE_2,   curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(S_FEATURE_3,   curses.COLOR_RED,   curses.COLOR_BLACK)
        curses.init_pair(S_FEATURE_4,   C_GOLD,             curses.COLOR_BLACK)
        curses.init_pair(S_KEYMARK,     curses.COLOR_GREEN, curses.COLOR_BLACK)