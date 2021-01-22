#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 08:27:00 2020

@author: jan
"""

import pygame
from pygame import Rect
import os
import const as c

class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()

        # load image for player character model
        self.load_images()        
        self.image = pygame.Surface((c.PLAYER_X_SIZE, c.PLAYER_Y_SIZE))
        self.rect = self.image.get_rect()
        self.velocity = [0, 0]

        # set player in pixel per second
        self.speed = c.PLAYER_SPEED

        # player model state
        self.state = 0

        # player starts facing down
        self.direction = c.direction.DOWN

        # get screen for draw-target
        self.screen = game.screen

    def load_images(self):
        images = [pygame.image.load(os.path.join("images", "BODY_male.png")).convert_alpha(),
                        pygame.image.load(os.path.join("images", "HEAD_hair_blonde.png")).convert_alpha(),
                        pygame.image.load(os.path.join("images", "TORSO_leather_armor_shirt_white.png")).convert_alpha(),
                        pygame.image.load(os.path.join("images", "TORSO_leather_armor_torso.png")).convert_alpha(),
                        pygame.image.load(os.path.join("images", "TORSO_leather_armor_shoulders.png")).convert_alpha(),
                        pygame.image.load(os.path.join("images", "TORSO_leather_armor_bracers.png")).convert_alpha(),
                        pygame.image.load(os.path.join("images", "LEGS_pants_greenish.png")).convert_alpha(),                      
                        pygame.image.load(os.path.join("images", "BELT_leather.png")).convert_alpha(),
                        pygame.image.load(os.path.join("images", "FEET_shoes_brown.png")).convert_alpha()
                    ]

        self.model = []
        for sprite in images:
            self.model += [pygame.transform.smoothscale(sprite, (c.PLAYER_X_SIZE * 9, c.PLAYER_Y_SIZE * 4))]


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

        # draw player on map
        src = Rect(self.state * c.PLAYER_X_SIZE, self.direction * c.PLAYER_Y_SIZE, c.PLAYER_X_SIZE, c.PLAYER_Y_SIZE )
        for sprite in self.model:
            self.screen.blit(sprite, self.rect, src)            

            