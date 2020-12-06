#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 08:27:00 2020

@author: jan
"""

import math 
import random
from enum import Enum

class field_v(Enum):
    NOT_VISITED = 0
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4    
    START = 5
    CORRIDOR = 6
    C_NORTH = 11
    C_EAST = 12
    C_SOUTH = 13
    C_WEST = 14

class return_v(Enum):
    VALID = 0
    OCCUPIED = 1
    OUTOFBOUND = 2
    INVALID = 99


class generator():
    def __init__(self, xSize, ySize):
        random.seed(a=None, version=2)
        self.xSize = xSize
        self.ySize = ySize
        # Two-dimensional list containing current maze including walls
        self.walled_field = [[0] * (self.ySize * 2 + 1) for i in range(self.xSize * 2 + 1)]  

        
    def generateMaze(self):
        # Remaining cells
        self.remainingCells = [range(0,self.ySize*self.xSize)]
        # Two-dimensional list containing current maze
        self.field = [[0] * self.ySize for i in range(self.xSize)]  
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
                self.fillCell(dd,dx,dy)
                # Remove all visited cells from the list of remaining cells
                self.remainingCells.remove(dx*self.ySize + dy)
        self.add_walls()
        print(self.walled_field)


    def add_walls(self):
        for x in range(self.xSize):
            for y in range(self.ySize):
                # Extend maze to include spaces for walls
                self.walled_field[1+x*2][1+y*2] = self.field[x][y]
        for x in range(self.xSize*2+1):
            for y in range(self.ySize*2+1):
                if self.walled_field[x][y] == field_v.NORTH:
                    self.walled_field[x-1][y] = field_v.CORRIDOR
                elif self.walled_field[x][y] == field_v.EAST:
                    self.walled_field[x][y+1] = field_v.CORRIDOR
                elif self.walled_field[x][y] == field_v.SOUTH:
                    self.walled_field[x+1][y] = field_v.CORRIDOR
                elif self.walled_field[x][y] == field_v.WEST:
                    self.walled_field[x][y-1] = field_v.CORRIDOR    
    
    def fillCell(self, d, x, y):
        # Set cell as visited
        self.field[x][y] = d     

    def checkCell(self,x,y):
        # Check if cell is empty and inside boundaries
        if x > 0 and y > 0  and y < self.ySize and x < self.xSize:
            if self.field[x][y] > 0 and self.field[x][y] < 10:
                return return_v.OCCUPIED
            else:
                return return_v.VALID
        else:
            return return_v.OUTOFBOUND
                        
    def randomWalk(self, startx, starty):
        # Resulting path
        path = []
        direction = -1
        current_field = self.field.copy()
        current_x = startx
        current_y = starty
        stop_x = 0
        stop_y = 0
        # Walk until occupied cell is found
        while 1:
            result = return_v.INVALID
            new_x = current_x
            new_y = current_y
            # Generate list with possible directions and shuffle it
            dir_list = [field_v.C_NORTH,field_v.C_EAST,field_v.C_SOUTH,field_v.C_WEST]
            random.shuffle(dir_list)
            # Retry until a valid or occupied cell is found
            while result != return_v.VALID or result != return_v.OCCUPIED:
                direction = dir_list.pop()
                if direction == field_v.C_NORTH:
                    new_x == new_x - 1
                elif direction == field_v.C_EAST:
                    new_y = new_y + 1
                elif direction == field_v.C_SOUTH:
                    new_x == new_x + 1
                elif direction == field_v.C_WEST:
                    new_y = new_y - 1
                result == self.checkCell(new_x,new_y)   
            # Found valid cell
            if result == return_v.VALID:                
                # Add direction to current cell
                current_field[current_x][current_y] = direction
                # Set new cell as current cell
                current_x = new_x
                current_y = new_y
            elif result == return_v.OCCUPIED:
                # Found occupied cell
                stop_x = current_x
                stop_y = current_y
                break
        # Walk along path and add it to result
        current_x = startx
        current_y = starty
        # Check if endpoint is reached
        while current_x != stop_x and current_y != stop_y:
            # Add current cell to path
            # Substract 10 from field_v to get [NORTH,EAST,SOUTH,WEST] instead of [C_NORTH,C_EAST,...]
            path.append((current_field[current_x][current_y]-10,current_x,current_y))
            # Goto next cell based of direction in current cell
            if current_field == field_v.C_NORTH:
                current_x == current_x - 1
            elif direction == field_v.C_EAST:
                current_y = current_y + 1
            elif direction == field_v.C_SOUTH:
                current_x == current_x + 1
            elif direction == field_v.C_WEST:
                current_y = current_y - 1    
        return path