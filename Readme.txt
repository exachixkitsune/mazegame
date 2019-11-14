README And Details

This software is provided without guarantee that the code is proper and will not break your computer. It is provided as-is, with no provision of support or aid if it's broken. Use of the software is at your own risk.

The source code requires curses and numpy to run in Python. The compiled executable should not require anything.

It is provided using the MIT Licence, which is detailed in Licence.txt


This is a game made for the Desert Bus Game Jam, based off the Mythology of the Minotaur and the Labryinth. To note, the game gives you a maze, not a true labyrith. Look up Labyrinth on wikipedia for more information
It was created by chat member ExachixKitsune.

What is the Desert Bus Game Jam?
See: https://itch.io/jam/dbgj2019
This is a game jam that ran at the same time as Desert Bus for Hope 2019.
The prompt for the game jam was Mythology.

What is Desert Bus for Hope?
  See: https://desertbus.org
  Desert Bus for Hope (DBFH) is a charity fundraiser where people raise money 
  For the charity ''Childs Play''. They take a week to play ''Desert Bus'', while
  the cast and crew act, chat, and entertain for donations.

Creation of the Game
  This game was written in python 3.7. It uses the curses library. It was
  compiled using the tool pyinstaller version 3.5.

References
  The colour definitions were taken from the css definition
  Maze Generation Algorithm is Randomized Prim''s, sourced from Wikipedia.
  https://en.wikipedia.org/wiki/Maze_generation_algorithm#Randomized_Prim''s_algorithm

Irregularities
  To note, the player always starts at the top-leftmost cell, and the exit
  is always in the lower-right corner. The Dubloons are distributed across
  the entire map.
  In order to get a consistant pattern in the floor tiles, the character 
  for the tile is calculated from the position to appear semi-random.