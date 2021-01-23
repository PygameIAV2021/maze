#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 08:27:00 2020

@author: jan
"""

import math 
import random
import enum
from const import field_v, return_v, draw_v


class Generator():
    def __init__(self):
        random.seed(a=None, version=2)
        
    def generate_maze(self, xSize, ySize):
        self.xSize = xSize
        self.ySize = ySize
        self.finalxSize = self.xSize * 2 + 1
        self.finalySize = self.ySize * 2 + 1
        self.starting_point = (0,0)
        self.ending_point = (0,0)
        # Two-dimensional list containing current maze including walls
        self.walled_field = [([field_v.NOT_VISITED] * (self.finalySize)) for i in range(self.finalxSize)]  
        # Remaining cells
        self.remainingCells = list(range(0,self.ySize*self.xSize))
        # Two-dimensional list containing current maze
        self.field = [[0] * self.ySize for i in range(self.xSize)]  
        # Get starting cell
        start = self.remainingCells.pop()
        sx = math.floor(start/self.ySize)
        sy = start%self.ySize
        # print("start: " + str(sx) + ":" + str(sy))
        self.field[sx][sy] = field_v.START
        # While there are still unvisited cell do generate new cells
        while len(self.remainingCells) > 0:
            currentCellNr = self.remainingCells.pop()
            #print("currentCellNr: " + str(currentCellNr))
            cx = math.floor(currentCellNr/self.ySize)
            cy = currentCellNr%self.ySize
            # print("currentCell: " + str(cx) + ":" + str(cy))
            currentPath = self.random_walk(cx,cy)    
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
        # expand maze and fit walls
        self.add_walls()
        # set each wall-field to correct type regarding its neighbours
        self.set_wall_type()
        # set each road-field to correct type regarding its neighbours
        self.set_road_type()
        # set random starting point and ending point for player
        self.set_player_points()

        self.set_spawns()
        # just print the maze into a *.csv for debugging
        self.print_maze(self.xSize * 2 + 1,self.ySize * 2 + 1,self.walled_field)
        return self.walled_field

    def return_maze_size(self):
        return (self.finalxSize, self.finalySize)


    def add_walls(self):
        # Extend maze to include spaces for walls
        for x in range(self.xSize):
            for y in range(self.ySize):                
                self.walled_field[1+x*2][1+y*2] = self.field[x][y]
        # Include the corridors between the cells
        for x in range(self.finalxSize):
            for y in range(self.finalySize):
                if self.walled_field[x][y] == field_v.NORTH:
                    self.walled_field[x-1][y] = field_v.CORRIDOR
                elif self.walled_field[x][y] == field_v.EAST:
                    self.walled_field[x][y+1] = field_v.CORRIDOR
                elif self.walled_field[x][y] == field_v.SOUTH:
                    self.walled_field[x+1][y] = field_v.CORRIDOR
                elif self.walled_field[x][y] == field_v.WEST:
                    self.walled_field[x][y-1] = field_v.CORRIDOR   
                elif self.walled_field[x][y] == field_v.START:
                    self.walled_field[x][y] = field_v.CORRIDOR 

    def set_wall_type(self):
        # set each wall-field to correct type regarding its neighbours
        for x in range(self.finalxSize):
            for y in range(self.finalySize):
                if self.walled_field[x][y] == field_v.NOT_VISITED:
                    count_neigh = 0
                    if (x+1) < (self.finalxSize):
                        # print("x+1",end="")
                        if self.walled_field[x+1][y] >= 20 or self.walled_field[x+1][y] == field_v.NOT_VISITED:
                            count_neigh = count_neigh + 1
                    if (y+1) < (self.finalySize):
                        # print("y+1",end="")
                        if self.walled_field[x][y+1] >= 20 or self.walled_field[x][y+1] == field_v.NOT_VISITED:
                            count_neigh = count_neigh + 2                         
                    if (x-1) >= 0:
                        # print("x-1",end="")
                        if self.walled_field[x-1][y] >= 20 or self.walled_field[x-1][y] == field_v.NOT_VISITED:
                            count_neigh = count_neigh + 4    
                    if (y-1) >= 0:
                        # print("y-1",end="")
                        if self.walled_field[x][y-1] >= 20 or self.walled_field[x][y-1] == field_v.NOT_VISITED:
                            count_neigh = count_neigh + 8
                    self.walled_field[x][y] = 20 + count_neigh
                    # print()
                    # print("currentWall: " + str(x) + ":" + str(y) + " = " + str(count_neigh))

    def set_road_type(self):
        # set each road-field to correct type regarding its neighbours
        for x in range(self.finalxSize):
            for y in range(self.finalySize):
                if self.walled_field[x][y] > 0 and self.walled_field[x][y] < 20:
                    count_neigh = 0
                    if (x+1) < (self.finalxSize):
                        # print("x+1",end="")
                        if self.walled_field[x+1][y] > 0 and self.walled_field[x+1][y] < 20:
                            count_neigh = count_neigh + 1
                    if (y+1) < (self.finalySize):
                        # print("y+1",end="")
                        if self.walled_field[x][y+1] > 0 and self.walled_field[x][y+1] < 20:
                            count_neigh = count_neigh + 2                         
                    if (x-1) >= 0:
                        # print("x-1",end="")
                        if self.walled_field[x-1][y] > 0 and self.walled_field[x-1][y] < 20:
                            count_neigh = count_neigh + 4    
                    if (y-1) >= 0:
                        # print("y-1",end="")
                        if self.walled_field[x][y-1] > 0 and self.walled_field[x][y-1] < 20:
                            count_neigh = count_neigh + 8
                    self.walled_field[x][y] = count_neigh
                    # print()
                    # print("currentWall: " + str(x) + ":" + str(y) + " = " + str(count_neigh))
                                                   
    def set_player_points(self):
        # set random starting point and ending point for player

        # print(self.xSize*2+1) 
        # print(self.ySize*2+1)
        # print(math.floor((self.ySize*2+1)*0.1)) 
        # print(math.floor((self.ySize*2+1)*0.9))

        list_of_ends = []      
        for x in range(math.floor((self.finalxSize)*0.9),self.finalxSize):
            for y in range(math.floor((self.finalySize)*0.9),self.finalySize):
                if self.walled_field[x][y] < 20 and self.walled_field[x][y] > 0:
                    list_of_ends.append((x,y))
        random.shuffle(list_of_ends)
        e_x,e_y = list_of_ends.pop()
        # print("end = " + str(e_x) + ":" + str(e_y))
        # self.walled_field[e_x][e_y] = draw_v.END
        self.ending_point = (e_x,e_y)

        list_of_starts = [] 
        for x in range(math.floor((self.finalxSize)*0.1)):
            for y in range(math.floor((self.finalySize)*0.1)):
                if self.walled_field[x][y] < 20 and self.walled_field[x][y] > 0:     
                    list_of_starts.append((x,y))
        random.shuffle(list_of_starts)
        s_x,s_y = list_of_starts.pop()
        # print("start = " + str(s_x) + ":" + str(s_y))
        # self.walled_field[s_x][s_y] = draw_v.START
        self.starting_point = (s_x,s_y)

    def get_player_points(self):
        return (self.starting_point,self.ending_point)

        
    def set_spawns(self):
        list_of_spawns = []      
        for x in range(math.floor((self.finalxSize)*0.5),self.finalxSize):
            for y in range(math.floor((self.finalySize)*0.5),self.finalySize):
                if self.walled_field[x][y] < 20 and self.walled_field[x][y] > 0:
                    list_of_spawns.append((x,y))

        random.shuffle(list_of_spawns)

        self.enemy_spawns = []

        for n in range(0,4):
            if len(list_of_spawns) > 0:
                self.enemy_spawns += [list_of_spawns.pop()]
        

    def get_spawn_points(self):
        return self.enemy_spawns


    def get_next_cell_x(self,p_x,dire):
        # calculate the x coordinate of the next targeted field
        if dire == field_v.C_NORTH:
            p_x = p_x - 1
        elif dire == field_v.C_SOUTH:
            p_x = p_x + 1
        return p_x
    
    def get_next_cell_y(self,p_y,dire):
        # calculate the y coordinate of the next targeted field
        if dire == field_v.C_EAST:
            p_y = p_y + 1
        elif dire == field_v.C_WEST:
            p_y = p_y - 1
        return p_y

    def check_cell(self,x,y):
        # Check if cell is empty and inside boundaries
        if x >= 0 and y >= 0  and y < self.ySize and x < self.xSize:
            if self.field[x][y] in [field_v.EAST,field_v.NORTH,field_v.WEST,field_v.SOUTH,field_v.START,field_v.CORRIDOR]:
                return return_v.OCCUPIED
            else:
                return return_v.VALID
        else:
            return return_v.OUTOFBOUND

    def print_maze(self,x,y,pField): 
        # just print the maze into a *.csv for debugging
        f = open("maze.csv", "w")
        for i in range(x):
            s_line = ''
            for j in range(y):
                debug = 1
                if debug == 1:                
                    if pField[i][j] == draw_v.RS_0:
                        s_line += 'rX;'
                    elif pField[i][j] == draw_v.RS_R:
                        s_line += 'rR;'        
                    elif pField[i][j] == draw_v.RS_U:
                        s_line += 'rU;'                       
                    elif pField[i][j] == draw_v.RS_RU:
                        s_line += 'rRU;'    
                    elif pField[i][j] == draw_v.RS_L:
                        s_line += 'rL;'    
                    elif pField[i][j] == draw_v.RS_LR:
                        s_line += 'rLR;'    
                    elif pField[i][j] == draw_v.RS_LU:
                        s_line += 'rLU;'    
                    elif pField[i][j] == draw_v.RS_LUR:
                        s_line += 'rLUR;'   
                    elif pField[i][j] == draw_v.RS_O:
                        s_line += 'rO;'   
                    elif pField[i][j] == draw_v.RS_OR:
                        s_line += 'rOR;'    
                    elif pField[i][j] == draw_v.RS_OU:
                        s_line += 'rOU;'    
                    elif pField[i][j] == draw_v.RS_ORU:
                        s_line += 'rOUR;'    
                    elif pField[i][j] == draw_v.RS_OL:
                        s_line += 'rOL;'    
                    elif pField[i][j] == draw_v.RS_OLR:
                        s_line += 'rOLR;'    
                    elif pField[i][j] == draw_v.RS_OLU:
                        s_line += 'rOLU;'    
                    elif pField[i][j] == draw_v.RS_OLUR:
                        s_line += 'rOULR;' 
                    elif pField[i][j] == draw_v.WS_0:
                        s_line += 'wX;'
                    elif pField[i][j] == draw_v.WS_R:
                        s_line += 'wR;'        
                    elif pField[i][j] == draw_v.WS_U:
                        s_line += 'wU;'                       
                    elif pField[i][j] == draw_v.WS_RU:
                        s_line += 'wRU;'    
                    elif pField[i][j] == draw_v.WS_L:
                        s_line += 'wL;'    
                    elif pField[i][j] == draw_v.WS_LR:
                        s_line += 'wLR;'    
                    elif pField[i][j] == draw_v.WS_LU:
                        s_line += 'wLU;'    
                    elif pField[i][j] == draw_v.WS_LUR:
                        s_line += 'wLUR;'   
                    elif pField[i][j] == draw_v.WS_O:
                        s_line += 'wO;'   
                    elif pField[i][j] == draw_v.WS_OR:
                        s_line += 'wOR;'    
                    elif pField[i][j] == draw_v.WS_OU:
                        s_line += 'wOU;'    
                    elif pField[i][j] == draw_v.WS_ORU:
                        s_line += 'wOUR;'    
                    elif pField[i][j] == draw_v.WS_OL:
                        s_line += 'wOL;'    
                    elif pField[i][j] == draw_v.WS_OLR:
                        s_line += 'wOLR;'    
                    elif pField[i][j] == draw_v.WS_OLU:
                        s_line += 'wOLU;'    
                    elif pField[i][j] == draw_v.WS_OLUR:
                        s_line += 'wOULR;' 
                    elif pField[i][j] == draw_v.START:
                        s_line += 'START;'    
                    elif pField[i][j] == draw_v.END:
                        s_line += 'END;'                       
                    else:
                        s_line += '?;'
                else:
                    if pField[i][j] in [field_v.EAST,field_v.C_EAST,field_v.NORTH,field_v.C_NORTH,field_v.WEST,field_v.C_WEST,field_v.SOUTH,field_v.C_SOUTH,field_v.START,field_v.CORRIDOR]:
                        s_line += ' '
                    else:
                        s_line += 'X'
            f.write(s_line + '\n')
        f.close()
                        
    def random_walk(self, startx, starty):
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
                new_x = self.get_next_cell_x(current_x,direction)
                new_y = self.get_next_cell_y(current_y,direction)
                result = self.check_cell(new_x,new_y)  
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
            c_x = self.get_next_cell_x(c_x,direct)
            c_y = self.get_next_cell_y(c_y,direct) 
        #print("pathend: " + str(stop_x) + ":" + str(stop_y))  
        #print("path = ",end='')
        #print(path)
        return path

if __name__=="__main__":
    new_generator = Generator()
    new_generator.generateMaze(10,10)
