# -*- coding: utf-8 -*-

import math

def make_value(world_pos, val_limit):
    # Seperated function to do testing
    
    a = world_pos[0] - 9
    b = world_pos[1] - 9
    
    c = math.pow(a*b + val_limit*(val_limit-5),3)
    d = math.pow(b + a*(val_limit+2),5)
    e = c*d + abs(d - c)*(val_limit+1)
    char_indx = math.floor(e) % val_limit
    return char_indx

def floor_character(world_pos):
    # What character should be used for the floor.
    # This is a function based off the position of the position in the world.
    # Would like it to be a random function, but that means that the 
    # map would change as you move.
    # And that'd be awful
    # Possible floor characters:
    #  These are Space, Space, period, comma, small comma, degree sign, Apostrophe, small c, small c
    # It is weighted against having the degree sign up as it's quite popular
    # Space is the most common character
    # Degree sign should be 1/4 popular.
    possible_characters=[' ',' ',' ',' ',' ',
                         '.','.',
                         ',',',',',',
                         183,183,183,
                         184,
                         176,176,176,
                         96,96,96,96,
                         722,722,722,
                         723,723,723,]
    # Convert world position into a derived number
    char_indx = make_value(world_pos,len(possible_characters))
    return (possible_characters[char_indx])