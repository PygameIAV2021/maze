#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  20 10:27:00 2021

@author: jan
"""

import pygame
import math
from pygame import Rect
import const as c

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, spawn, models):
        super().__init__()
      
        self.image = pygame.Surface((c.ENEMY_X_SIZE, c.ENEMY_Y_SIZE))
        self.rect = self.image.get_rect()
        spawn_x, spawn_y = spawn
        self.rect[0] = spawn_x * c.TILE_SIZE + math.floor((c.TILE_SIZE - c.ENEMY_X_SIZE) / 2)
        self.rect[1] = spawn_y * c.TILE_SIZE + math.floor((c.TILE_SIZE - c.ENEMY_Y_SIZE) / 2)
        self.target = [spawn_x * c.TILE_SIZE,spawn_y * c.TILE_SIZE]
        self.velocity = [0 , 0]

        # set player in pixel per second
        self.speed = c.ENEMY_SPEED

        # player model state
        self.state = 0

        # player starts facing down
        self.direction = c.direction.DOWN

        # get screen for draw-target
        self.screen = game.screen

        self.model = models.get_random_enemy_images()

    def get_next_pos(self):
        # calculate next position
        new_x = self.rect[0] + self.velocity[0]
        new_y = self.rect[1] + self.velocity[1]
        return (new_x,new_y)

    def update(self):
        # calculate next position
        self.rect.move_ip(*self.velocity) 

        # walking animation
        if self.velocity[0] == 0 and self.velocity[1] == 0:
            self.state = 0
        else:
            self.state += 1
            if self.state >= 9:
                self.state = 1

        # get direction
        if self.velocity[1] > 0:
            self.direction = c.direction.DOWN
        elif self.velocity[1] < 0:
            self.direction = c.direction.UP
        elif self.velocity[0] > 0:
            self.direction = c.direction.RIGHT
        elif self.velocity[0] < 0:
            self.direction = c.direction.LEFT

        src = Rect(self.state * c.ENEMY_X_SIZE, self.direction * c.ENEMY_Y_SIZE, c.ENEMY_X_SIZE, c.ENEMY_Y_SIZE )
        for sprite in self.model:
            self.screen.blit(sprite, self.rect, src) 

    def update_to(self,x,y):
        # calculate next position
        self.rect[0] = x
        self.rect[1] = y 

        # walking animation
        if self.velocity[0] == 0 and self.velocity[1] == 0:
            self.state = 0
        else:
            self.state += 1
            if self.state >= 9:
                self.state = 1

        # get direction
        if self.velocity[1] > 0:
            self.direction = c.direction.DOWN
        elif self.velocity[1] < 0:
            self.direction = c.direction.UP
        elif self.velocity[0] > 0:
            self.direction = c.direction.RIGHT
        elif self.velocity[0] < 0:
            self.direction = c.direction.LEFT

        # draw player on map
        src = Rect(self.state * c.ENEMY_X_SIZE, self.direction * c.ENEMY_Y_SIZE, c.ENEMY_X_SIZE, c.ENEMY_Y_SIZE )
        for sprite in self.model:
            self.screen.blit(sprite, self.rect, src)        