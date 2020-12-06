#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 08:27:00 2020

@author: jan
"""

import math 
from enum import Enum

class field_v(Enum):
    NOT_VISITED = 0
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4    
    START = 5
    C_NORTH = 11
    C_EAST = 12
    C_SOUTH = 13
    C_WEST = 14

class return_v(Enum):
    VALID = 0
    OCCUPIED = 1
    OUTOFBOUND = 2


class generator():
    def __init__(self, xSize, ySize):
        self.xSize = xSize
        self.ySize = ySize
        # Two-dimensional list containing current maze
        self.field = [[0] * self.ySize for i in range(self.xSize)]  
        # Two-dimensional list containing current maze including walls
        self.walled_field = [[0] * (self.ySize * 3 - 2) for i in range(self.xSize * 3 - 2)]  
        # Remaining cells
        self.remainingCells = [range(0,self.ySize*self.xSize)]
        
    def generateMaze(self):
        # Get starting cell
        start = self.remainingCells.pop()
        sx = math.floor(start/self.ySize)
        sy = start%self.ySize
        self.fillCell(field_v.START,sx,sy)
        # While there are still unvisited cell do generate new cells
        while len(self.remainingCells) > 0:
            currentCellNr = self.remainingCells.pop()
            cx = math.floor(currentCellNr/self.ySize)
            cy = currentCellNr%self.ySize
            currentPath = self.randomWalk(cx,cy)    
            for dd,dx,dy in currentPath:
                # Fill all cells visited by the current path
                self.fillCell(dd, dx,dy)
                # Remove all visited cells from the list of remaining cells
                self.remainingCells.remove(dx*self.ySize + dy)
    
    def fillCell(self, d, x, y):
        # Set cell as visited
        self.field[x][y] = d     

    def checkCell(self,x,y):
        # Check if cell is empty and inside boundaries
        if x > 0 and y > 0  and y < self.ySize and x < self.xSize:
            if self.field[x][y] > 0:
                return return_v.OCCUPIED
            else:
                return return_v.VALID
        else:
            return return_v.OUTOFBOUND
                        
    def randomWalk(self, startx, starty):
        return [[1,1],[1,2]]