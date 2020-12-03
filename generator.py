#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 08:27:00 2020

@author: jan
"""

import math 
from enum import Enum

class f_value(Enum):
    NOT_VISITED = 0
    VISITED = 1
    NEIGHBOUR = 2
    C_NORTH = 11
    C_EAST = 12
    C_SOUTH = 13
    C_WEST = 14
    C_NEIGHBOUR = 15

class generator():
    def __init__(self, xSize, ySize):
        self.xSize = xSize
        self.ySize = ySize
        # Two-dimensional list containing current maze
        self.field = [[0] * self.ySize for i in range(self.xSize)]  
        # Remaining cells
        self.remainingCells = range(0,self.ySize*self.xSize)
        
    def generateMaze(self):
        start = self.remainingCells.pop()
        sx = math.floor(start/self.ySize)
        sy = start%self.ySize# 03 = indirect neighbour (NE,SE,NW,SW)
        self.fillCell(sx,sy)
        while len(self.remainingCells) > 0:
            currentCellNr = self.remainingCells.pop()
            cx = math.floor(currentCellNr/self.ySize)
            cy = currentCellNr%self.ySize
            currentPath = self.randomWalk(cx,cy)    
            for dx,dy in currentPath:
                # Fill all cells visited by the current path
                self.fillCell(dx,dy)
                # Remove all visited cells from the list of remaining cells
                self.remainingCells.remove(dx*self.ySize + dy)
    
    def fillPathCell(self, d, x, y):
        # Set cell as visited
        self.field[x][y] = d
        # Set all neighbours as adjacent (2 for N, E, S, W; 3 for NE, SE, NW, SW) if they haven't visited before
        if x+1 < self.xSize:
            if self.field[x+1][y] == f_value.NOT_VISITED:
                self.field[x+1][y] = f_value.C_NEIGHBOUR
            if y+1 < self.ySize:
                if self.field[x+1][y+1] == f_value.NOT_VISITED:
                    self.field[x+1][y+1] == f_value.C_NEIGHBOUR    
            if y-1 < self.ySize:
                if self.field[x+1][y-1] == f_value.NOT_VISITED:
                    self.field[x+1][y-1] == f_value.C_NEIGHBOUR 
        if y+1 < self.ySize:
            if self.field[x][y+1] == f_value.NOT_VISITED:
                self.field[x][y+1] = f_value.C_NEIGHBOUR            
        if x-1 >= 0:
            if self.field[x-1][y] == f_value.NOT_VISITED:
                self.field[x-1][y] == f_value.C_NEIGHBOUR
            if y+1 < self.ySize:
                if self.field[x-1][y+1] == f_value.NOT_VISITED:
                    self.field[x-1][y+1] == f_value.C_NEIGHBOUR    
            if y-1 < self.ySize:
                if self.field[x-1][y-1] == f_value.NOT_VISITED:
                    self.field[x-1][y-1] == f_value.C_NEIGHBOUR
        if y-1 >= 0:
            if self.field[x][y-1] == f_value.NOT_VISITED:
                self.field[x][y-1] = f_value.C_NEIGHBOUR        
            
    def fillCell(self, x, y):
        # Set cell as visited
        self.field[x][y] = f_value.VISITED
        # Set all neighbours as adjacent (2 for N, E, S, W; 3 for NE, SE, NW, SW) if they haven't visited before
        if x+1 < self.xSize:
            if self.field[x+1][y] == f_value.NOT_VISITED:
                self.field[x+1][y] = f_value.NEIGHBOUR
            if y+1 < self.ySize:
                if self.field[x+1][y+1] == f_value.NOT_VISITED:
                    self.field[x+1][y+1] == f_value.NEIGHBOUR    
            if y-1 < self.ySize:
                if self.field[x+1][y-1] == f_value.NOT_VISITED:
                    self.field[x+1][y-1] == f_value.NEIGHBOUR 
        if y+1 < self.ySize:
            if self.field[x][y+1] == f_value.NOT_VISITED:
                self.field[x][y+1] = f_value.NEIGHBOUR            
        if x-1 >= 0:
            if self.field[x-1][y] == f_value.NOT_VISITED:
                self.field[x-1][y] == f_value.NEIGHBOUR
            if y+1 < self.ySize:
                if self.field[x-1][y+1] == f_value.NOT_VISITED:
                    self.field[x-1][y+1] == f_value.NEIGHBOUR    
            if y-1 < self.ySize:
                if self.field[x-1][y-1] == f_value.NOT_VISITED:
                    self.field[x-1][y-1] == f_value.NEIGHBOUR 
        if y-1 >= 0:
            if self.field[x][y-1] == f_value.NOT_VISITED:
                self.field[x][y-1] = f_value.NEIGHBOUR  
                        
    def randomWalk(self, startx, starty):
        return [[1,1],[1,2]]