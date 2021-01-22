#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 08:27:00 2020

@author: jan
"""

import game
import pygame
from pygame import Rect
import random
import generator
import const as c
import os
import math

class Map():
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        
        self.scrolling = False
        
        self.load_basetiles()
        self.load_bordertiles()
        self.load_markertiles()

        self.generator = generator.Generator()

        self.offset = (0, 0)
                
    def scroll(self, rel):
        if not self.scrolling: return

        self.offset = (
            self.offset[0] + rel[0],
            self.offset[1] + rel[1] )
        
    def load_basetiles(self, image="base.png"):
        self.basetiles = pygame.image.load(os.path.join("images", image)).convert_alpha()
        self.rect = self.basetiles.get_rect()

    def load_bordertiles(self, image="borders.png"):
        self.bordertiles = pygame.image.load(os.path.join("images", image)).convert_alpha()

    def load_markertiles(self, image="markers.png"):
        self.markertiles = pygame.image.load(os.path.join("images", image)).convert_alpha()
                    
    def load_map(self, size_x, size_y):

        # Generate new map and get the mapsize in tiles
        self.map = self.generator.generate_maze(size_x,size_y)
        self.tiles_x = self.generator.finalxSize
        self.tiles_y = self.generator.finalySize

        # Create array for player markers
        self.tracker = [[0] * (self.tiles_y) for i in range(self.tiles_x)]

        # Create and fill array with random markers for alternate tile designs 
        self.randomizer = [[0] * (self.tiles_y) for i in range(self.tiles_x)]
        for y in range(self.tiles_y):
            for x in range(self.tiles_x):
                self.randomizer[x][y] = (self.get_weighted_int(),self.get_weighted_int())

        # Get all interesting points and store them        
        self.starting_p, self.ending_p = self.generator.get_player_points()
        self.ending_x, self.ending_y = self.ending_p
        self.starting_x, self.starting_y = self.starting_p
        self.spawn_p = self.generator.get_spawn_points()
        return self.map

    def get_weighted_int(self):

        # Generate random number with weights
        new_int = random.randint(0,99)
        if new_int < 80:
            return 0
        elif new_int < 90:
            return 1
        elif new_int < 100:
            return 2
        else:
            return 0

    def update_tracker(self, rect):
        x = math.floor((rect[0] + (c.PLAYER_X_SIZE / 2)) / c.TILE_SIZE)
        y = math.floor((rect[1] + (c.PLAYER_Y_SIZE / 2))/ c.TILE_SIZE) 
        if self.tracker[x][y] == 0:
            self.tracker[x][y] = 1
            
    def draw(self):
        # loop all tiles, and draw        
        for y in range( self.tiles_y ):
                for x in range( self.tiles_x ):
                    # draw tile at (x,y)
                    id = self.map[x][y]
                    rand_base, rand_border = self.randomizer[x][y]

                    # get rect() to draw only tile from the tileset that we want
                    dest = Rect( x * c.TILE_SIZE, y * c.TILE_SIZE, c.TILE_SIZE, c.TILE_SIZE )

                    if x == self.ending_x and y == self.ending_y:
                        base = Rect( c.base_id.END * c.TILE_SIZE, rand_base * c.TILE_SIZE, c.TILE_SIZE, c.TILE_SIZE )
                        border = Rect( id * c.TILE_SIZE, 0, c.TILE_SIZE, c.TILE_SIZE )
                    elif id >= c.draw_v.RS_0 and id <= c.draw_v.RS_OLUR:
                        base = Rect( c.base_id.ROAD * c.TILE_SIZE, rand_base * c.TILE_SIZE, c.TILE_SIZE, c.TILE_SIZE )
                        border = Rect( id * c.TILE_SIZE, 0, c.TILE_SIZE, c.TILE_SIZE )
                    elif id >= c.draw_v.WS_0 and id <= c.draw_v.WS_OLUR:
                        base = Rect( c.base_id.WALL * c.TILE_SIZE, rand_base * c.TILE_SIZE, c.TILE_SIZE, c.TILE_SIZE )
                        border = Rect( (id - c.draw_v.WS_0) * c.TILE_SIZE, 0, c.TILE_SIZE, c.TILE_SIZE )   
                    else:
                        base = Rect( c.base_id.ROAD * c.TILE_SIZE, rand_base * c.TILE_SIZE, c.TILE_SIZE, c.TILE_SIZE )
                        border = Rect( c.draw_v.RS_0 * c.TILE_SIZE, 0, c.TILE_SIZE, c.TILE_SIZE ) 

                    # note, for scrolling tiles, uncomment:
                    if self.scrolling:
                        dest.left += self.offset[0]
                        dest.top += self.offset[1]                        

                    self.screen.blit( self.basetiles, dest, base)
                    self.screen.blit( self.bordertiles, dest, border)

                    if self.tracker[x][y] != 0 and self.game.show_markers:
                        self.screen.blit(self.markertiles, dest)
