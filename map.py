#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 08:27:00 2020

@author: jan
"""

import pygame
from pygame import Rect
import generator
import const as c
import os

class Map():
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        
        self.scrolling = False
        
        self.load_tileset("tileset.bmp")

        self.generator = generator.Generator()

        self.offset = (0, 0)
                
    def scroll(self, rel):
        if not self.scrolling: return

        self.offset = (
            self.offset[0] + rel[0],
            self.offset[1] + rel[1] )
        
    def load_tileset(self, image="tileset.bmp"):         
        self.tileset = pygame.image.load(os.path.join("images", image)).convert()
        self.rect = self.tileset.get_rect()
                    
    def load_map(self, size_x, size_y):
        self.map = self.generator.generateMaze(size_x,size_y)
        self.tiles_x = size_x * 2 + 1
        self.tiles_y = size_y * 2 + 1
        self.starting_p, self.ending_p = self.generator.getPlayerPoints()
        return self.map
            
    def draw(self):
        # loop all tiles, and draw        
        for y in range( self.tiles_y ):
                for x in range( self.tiles_x ):
                    # draw tile at (x,y)
                    id = self.map[x][y]

                    # get rect() to draw only tile from the tileset that we want
                    dest = Rect( x * c.TILE_SIZE, y * c.TILE_SIZE, c.TILE_SIZE, c.TILE_SIZE )
                    src = Rect( id * c.TILE_SIZE, 0, c.TILE_SIZE, c.TILE_SIZE )

                    # note, for scrolling tiles, uncomment:
                    if self.scrolling:
                        dest.left += self.offset[0]
                        dest.top += self.offset[1]                        

                    self.screen.blit( self.tileset, dest, src )