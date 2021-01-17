#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 08:27:00 2020

@author: jan
"""

import pygame
from pygame import Rect
import copy
import const as c

class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()

        # load image for player character model
        self.image = pygame.Surface((c.PLAYER_X_SIZE, c.PLAYER_Y_SIZE))
        self.image.fill(c.WHITE)
        self.rect = self.image.get_rect()
        self.velocity = [0, 0]

        # set player in pixel per second
        self.speed = 150

        # get screen for draw-target
        self.screen = game.screen

    def getNextPos(self):
        # calculate next position
        new_x = self.rect[0] + self.velocity[0]
        new_y = self.rect[1] + self.velocity[1]
        return (new_x,new_y)

    def update(self):
        # calculate next position
        self.rect.move_ip(*self.velocity) 
        # draw player on map
        self.screen.blit(self.image, self.rect)            

            