#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 08:27:00 2020

@author: jan
"""

import enum

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

class draw_v(enum.IntEnum):
    RS_0 = 0
    RS_R = 1
    RS_U = 2
    RS_RU = 3
    RS_L = 4
    RS_LR = 5
    RS_LU = 6
    RS_LUR = 7
    RS_O = 8
    RS_OR = 9
    RS_OU = 10
    RS_ORU = 11
    RS_OL = 12
    RS_OLR = 13
    RS_OLU = 14
    RS_OLUR = 15    

    START = 16
    END = 17
    SPAWN = 18  

    WS_0 = 20
    WS_R = 21
    WS_U = 22
    WS_RU = 23
    WS_L = 24
    WS_LR = 25
    WS_LU = 26
    WS_LUR = 27
    WS_O = 28
    WS_OR = 29
    WS_OU = 30
    WS_ORU = 31
    WS_OL = 32
    WS_OLR = 33
    WS_OLU = 34
    WS_OLUR = 35    

class return_v(enum.IntEnum):
    VALID = 0
    OCCUPIED = 1
    OUTOFBOUND = 2
    INVALID = 99

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
TILE_SIZE = 32
FPS = 60
WINDOW_HEIGHT = 1312
WINDOW_WIDTH = 1312