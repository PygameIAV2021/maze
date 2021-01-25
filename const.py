#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 08:27:00 2020

@author: jan
"""

import enum

# File including most of the static values
TILE_SIZE = 64
ENEMY_SIZE = TILE_SIZE
PLAYER_SIZE = TILE_SIZE
COLLISION_OFFSET = (10,2,8,4) # Top, Bottom, Left, Right
PLAYER_SPEED = 4 # Tiles per second
ENEMY_SPEED = 3 # Tiles per second
ENEMY_RAND_SPEED = 1 # Tiles per second
ENEMY_COUNT = 6
FPS = 60
WINDOW_SIZE = (1456,1296) # (Width, Height)
MAZE_SIZE = (45,40) # (Width, Height)
WALK_ANIMATION_LENGTH = 9
SLASH_ANIMATION_LENGTH = 6
HURT_ANIMATION_LENGTH = 6
SLASH_ANIMATION_MODIFIER = 10
HURT_ANIMATION_MODIFIER = 10
PLAYER_WALK_ANIMATION_MODIFIER = 5
ENEMY_WALK_ANIMATION_MODIFIER = 5

# The following entries may not be changed

# enum for game state:
class game_state(enum.IntEnum):
    EXIT = 0
    RUNNING = 1
    DEATH = 2
    WIN = 3
    PAUSE = 4

# emum for direction of models
class direction(enum.IntEnum):
    UP = 0
    LEFT = 1
    DOWN = 2
    RIGHT = 3

# enum for the map array during the random walk algorithm
class field_v(enum.IntEnum):
    NOT_VISITED = 0
    EAST = 1
    NORTH = 2
    WEST = 3
    SOUTH = 4    
    START = 5
    CORRIDOR = 6
    C_EAST = 11
    C_NORTH = 12
    C_WEST = 13
    C_SOUTH = 14
    END = 15

# enum for the final returned version of the map array
class draw_v(enum.IntEnum):    
    RS_0 = 0
    RS_U = 1
    RS_R = 2
    RS_RU = 3
    RS_O = 4
    RS_OU = 5
    RS_OR = 6
    RS_ORU = 7
    RS_L = 8
    RS_LU = 9
    RS_LR = 10
    RS_LUR = 11
    RS_OL = 12
    RS_OLU = 13
    RS_OLR = 14
    RS_OLUR = 15 

    START = 16
    END = 17
    SPAWN = 18  

    WS_0 = 20
    WS_U = 21
    WS_R = 22
    WS_RU = 23
    WS_O = 24
    WS_OU = 25
    WS_OR = 26
    WS_ORU = 27
    WS_L = 28
    WS_LU = 29
    WS_LR = 30
    WS_LUR = 31
    WS_OL = 32
    WS_OLU = 33
    WS_OLR = 34
    WS_OLUR = 35  

class base_id(enum.IntEnum):
    ROAD = 0
    WALL = 1  
    END = 2

# return values for the cell checking during the random walk algorithm
class return_v(enum.IntEnum):
    VALID = 0
    OCCUPIED = 1
    OUTOFBOUND = 2
    INVALID = 99

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)