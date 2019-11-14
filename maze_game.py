# -*- coding: utf-8 -*-

"""
	Primary Running Script
	Run this script to go
"""

# Maze Game Primary script
import menu_windows
import curses
import traceback

try:
    curses.wrapper(menu_windows.main)
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