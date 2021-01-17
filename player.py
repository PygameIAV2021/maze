#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 08:27:00 2020

@author: jan
"""

import pygame
import const as c

class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.size_x = 26
        self.size_y = 26
        self.image = pygame.Surface((self.size_x, self.size_y))
        self.image.fill(c.WHITE)
        self.rect = self.image.get_rect()  # Get rect of some size as 'image'.
        self.velocity = [0, 0]
        self.speed = 150
        self.screen = game.screen

    def update(self):
        self.rect.move_ip(*self.velocity) 
        self.screen.blit(self.image, self.rect) 