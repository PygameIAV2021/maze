#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 08:27:00 2020

@author: jan
"""

import math 
import random
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

class return_v(enum.IntEnum):
    VALID = 0
    OCCUPIED = 1
    OUTOFBOUND = 2
    INVALID = 99


class generator():
    def __init__(self):
        random.seed(a=None, version=2)


        
    def generateMaze(self, xSize, ySize):
        self.xSize = xSize
        self.ySize = ySize
        # Two-dimensional list containing current maze including walls
        self.walled_field = [[0] * (self.ySize * 2 + 1) for i in range(self.xSize * 2 + 1)]  
        # Remaining cells
        self.remainingCells = list(range(0,self.ySize*self.xSize))
        # Two-dimensional list containing current maze
        self.field = [[0] * self.ySize for i in range(self.xSize)]  
        # Get starting cell
        start = self.remainingCells.pop()
        sx = math.floor(start/self.ySize)
        sy = start%self.ySize
        print("start: " + str(sx) + ":" + str(sy))
        self.field[sx][sy] = field_v.START
        # While there are still unvisited cell do generate new cells
        while len(self.remainingCells) > 0:
            currentCellNr = self.remainingCells.pop()
            #print("currentCellNr: " + str(currentCellNr))
            cx = math.floor(currentCellNr/self.ySize)
            cy = currentCellNr%self.ySize
            print("currentCell: " + str(cx) + ":" + str(cy))
            currentPath = self.randomWalk(cx,cy)    
            for dd,dx,dy in currentPath:
                # Fill all cells visited by the current path
                self.field[dx][dy] = dd
                # Remove all visited cells from the list of remaining cells
                if dx*self.ySize+dy != currentCellNr:
                    try:     
                        #print(self.remainingCells)
                        #print("x: " + str(dx) + " y: " + str(dy))
                        #print(dx*self.ySize + dy)          
                        #self.printMaze(self.xSize,self.ySize,self.field) 
                        self.remainingCells.remove(dx*self.ySize + dy)
                    except ValueError:                    
                        exit("Value not in range")
        #self.printMaze(self.xSize,self.ySize,self.field)
        self.addWalls()
        self.printMaze(self.xSize * 2 + 1,self.ySize * 2 + 1,self.walled_field)
        return self.walled_field


    def addWalls(self):
        # Extend maze to include spaces for walls
        for x in range(self.xSize):
            for y in range(self.ySize):                
                self.walled_field[1+x*2][1+y*2] = self.field[x][y]
        # Include the corridors between the cells
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

    def getNextCellX(self,p_x,dire):
        if dire == field_v.C_NORTH:
            p_x = p_x - 1
        elif dire == field_v.C_SOUTH:
            p_x = p_x + 1
        return p_x
    
    def getNextCellY(self,p_y,dire):
        if dire == field_v.C_EAST:
            p_y = p_y + 1
        elif dire == field_v.C_WEST:
            p_y = p_y - 1
        return p_y

    def checkCell(self,x,y):
        # Check if cell is empty and inside boundaries
        if x >= 0 and y >= 0  and y < self.ySize and x < self.xSize:
            if self.field[x][y] in [field_v.EAST,field_v.NORTH,field_v.WEST,field_v.SOUTH,field_v.START,field_v.CORRIDOR]:
                return return_v.OCCUPIED
            else:
                return return_v.VALID
        else:
            return return_v.OUTOFBOUND

    def printMaze(self,x,y,pField): 
        f = open("maze.csv", "w")
        for i in range(x):
            s_line = ''
            for j in range(y):
                debug = 0
                if debug == 1:                
                    if pField[i][j] == field_v.EAST:
                        s_line += 'E;'
                    elif pField[i][j] == field_v.C_EAST: 
                        s_line += 'e;'               
                    elif pField[i][j] == field_v.NORTH:
                        s_line += 'N;'
                    elif pField[i][j] == field_v.C_NORTH:
                        s_line += 'n;' 
                    elif pField[i][j] == field_v.WEST:
                        s_line += 'W;' 
                    elif pField[i][j] == field_v.C_WEST:
                        s_line += 'w;' 
                    elif pField[i][j] == field_v.SOUTH:
                        s_line += 'S;'
                    elif pField[i][j] == field_v.C_SOUTH:
                        s_line += 's;'
                    elif pField[i][j] == field_v.START:
                        s_line += 'A;'
                    elif pField[i][j] == field_v.CORRIDOR:
                        s_line += 'C;'    
                    else:
                        s_line += 'X;'
                else:
                    if pField[i][j] in [field_v.EAST,field_v.C_EAST,field_v.NORTH,field_v.C_NORTH,field_v.WEST,field_v.C_WEST,field_v.SOUTH,field_v.C_SOUTH,field_v.START,field_v.CORRIDOR]:
                        s_line += ' '
                    else:
                        s_line += 'X'
            f.write(s_line + '\n')
        f.close()
                        
    def randomWalk(self, startx, starty):
        # Resulting path
        path = []
        direction = -1
        current_field = self.field.copy()
        current_x = startx
        current_y = starty
        stop_x = 0
        stop_y = 0
        new_x = 0
        new_y = 0
        # Walk until occupied cell is found
        while 1:
            result = return_v.INVALID
            # Generate list with possible directions and shuffle it
            dir_list = [field_v.C_EAST,field_v.C_NORTH,field_v.C_WEST,field_v.C_SOUTH]
            random.shuffle(dir_list)
            # Retry until a valid or occupied cell is found
            while result != return_v.VALID and result != return_v.OCCUPIED:
                direction = dir_list.pop()
                new_x = self.getNextCellX(current_x,direction)
                new_y = self.getNextCellY(current_y,direction)
                result = self.checkCell(new_x,new_y)  
            # Found valid cell
            if result == return_v.VALID:                
                # Add direction to current cell
                current_field[current_x][current_y] = direction
                # Set new cell as current cell
                current_x = new_x
                current_y = new_y
            elif result == return_v.OCCUPIED:
                # Found occupied cell
                # Add direction to current cell
                current_field[current_x][current_y] = direction               
                stop_x = new_x
                stop_y = new_y
                break
        # Walk along path and add it to result
        c_x = startx
        c_y = starty
        #print("pathsta: " + str(startx) + ":" + str(starty))
        # Check if endpoint is reached
        while c_x != stop_x or c_y != stop_y:
            # Add current cell to path
            # Convert [EAST,NORTH,WEST,SOUTH] to [C_EAST,C_NORTH,...]
            direct = current_field[c_x][c_y]
            if direct == field_v.C_EAST:
                path.append((field_v.EAST,c_x,c_y))
            if direct == field_v.C_NORTH:
                path.append((field_v.NORTH,c_x,c_y))
            if direct == field_v.C_WEST:
                path.append((field_v.WEST,c_x,c_y))
            if direct == field_v.C_SOUTH:
                path.append((field_v.SOUTH,c_x,c_y))
            # Goto next cell based of direction in current cell
            c_x = self.getNextCellX(c_x,direct)
            c_y = self.getNextCellY(c_y,direct) 
        #print("pathend: " + str(stop_x) + ":" + str(stop_y))  
        #print("path = ",end='')
        #print(path)
        return path

g_maze1 = generator()
maze1 = g_maze1.generateMaze(50,100)
