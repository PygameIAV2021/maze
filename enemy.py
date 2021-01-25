#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  20 10:27:00 2021

@author: jan
"""

import pygame
from pygame import Rect
import math
import random

import const as c

# Class for displaying and moving of the enemy sprites

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, spawn, models):
        super().__init__()
      
        self.image = pygame.Surface((c.ENEMY_SIZE, c.ENEMY_SIZE))
        self.rect = self.image.get_rect()
        spawn_x, spawn_y = spawn
        self.rect[0] = spawn_x * c.TILE_SIZE + math.floor((c.TILE_SIZE - c.ENEMY_SIZE) / 2)
        self.rect[1] = spawn_y * c.TILE_SIZE + math.floor((c.TILE_SIZE - c.ENEMY_SIZE) / 2)
        self.target = [spawn_x * c.TILE_SIZE,spawn_y * c.TILE_SIZE]
        self.velocity = [0 , 0]

        # set player in pixel per second
        self.speed = math.ceil(c.ENEMY_SPEED + random.randint(0,c.ENEMY_RAND_SPEED)) * c.TILE_SIZE

        # player model state
        self.state = 0

        # counter for slash animation
        self.slash_state = 0

        # player starts facing down
        self.direction = c.direction.DOWN

        # get screen for draw-target
        self.screen = game.screen
        self.game = game

        self.model, self.slash = models.get_random_enemy_images()
        

    def get_next_pos(self):

        # calculate next position
        new_x = self.rect[0] + self.velocity[0]
        new_y = self.rect[1] + self.velocity[1]
        return (new_x,new_y)

    def hit(self, direction):
        self.slash_state += 1
        if self.slash_state >= c.SLASH_ANIMATION_LENGTH*c.SLASH_ANIMATION_MODIFIER:
            self.slash_state = 1        
        
        state = math.floor(self.slash_state/c.SLASH_ANIMATION_MODIFIER)

        dest = Rect(self.rect.left,self.rect.top,self.rect.width,self.rect.height)

        # note, for scrolling tiles, uncomment:
        if self.game.scrolling:
            dest.left += self.game.offset[0]
            dest.top += self.game.offset[1] 

        src = Rect(state * c.ENEMY_SIZE, direction * c.ENEMY_SIZE, c.ENEMY_SIZE, c.ENEMY_SIZE )
        for sprite in self.slash:
            self.screen.blit(sprite, dest, src) 


    def update(self, x=None, y=None):

        # calculate next position
        if x is None or y is None:    
            self.rect.move_ip(*self.velocity) 
        else:
            self.rect[0] = x
            self.rect[1] = y 

        self.draw()


    def draw(self, stop = None):

        if stop is None:
            # walking animation
            if self.velocity[0] == 0 and self.velocity[1] == 0:
                self.state = 0
            else:
                self.state += 1
                if self.state >= c.WALK_ANIMATION_LENGTH*c.ENEMY_WALK_ANIMATION_MODIFIER:
                    self.state = 1
        else:
            self.state = 0

        state = math.floor(self.state/c.ENEMY_WALK_ANIMATION_MODIFIER)

        # get direction
        if self.velocity[1] > 0:
            self.direction = c.direction.DOWN
        elif self.velocity[1] < 0:
            self.direction = c.direction.UP
        elif self.velocity[0] > 0:
            self.direction = c.direction.RIGHT
        elif self.velocity[0] < 0:
            self.direction = c.direction.LEFT

        dest = Rect(self.rect.left,self.rect.top,self.rect.width,self.rect.height)

        # note, for scrolling tiles, uncomment:
        if self.game.scrolling:
            dest.left += self.game.offset[0]
            dest.top += self.game.offset[1]  

        src = Rect(state * c.ENEMY_SIZE, self.direction * c.ENEMY_SIZE, c.ENEMY_SIZE, c.ENEMY_SIZE )
        for sprite in self.model:
            self.screen.blit(sprite, dest, src)  