#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 08:27:00 2020

@author: jan
"""

import pygame
from pygame import Rect
import math
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

        # player hurt state
        self.hurt_state = 0

        # player starts facing down
        self.direction = c.direction.DOWN

        # get screen for draw-target
        self.screen = game.screen
        

    def load_images(self):

        walk_path = os.path.join("images","player")

        hurt_path = os.path.join("images","hurt")

        images = [pygame.image.load(os.path.join(walk_path, "BODY_male.png")).convert_alpha(),
                        pygame.image.load(os.path.join(walk_path, "HEAD_hair_blonde.png")).convert_alpha(),
                        pygame.image.load(os.path.join(walk_path, "TORSO_leather_armor_shirt_white.png")).convert_alpha(),
                        pygame.image.load(os.path.join(walk_path, "TORSO_leather_armor_torso.png")).convert_alpha(),
                        pygame.image.load(os.path.join(walk_path, "TORSO_leather_armor_shoulders.png")).convert_alpha(),
                        pygame.image.load(os.path.join(walk_path, "TORSO_leather_armor_bracers.png")).convert_alpha(),
                        pygame.image.load(os.path.join(walk_path, "LEGS_pants_greenish.png")).convert_alpha(),                      
                        pygame.image.load(os.path.join(walk_path, "BELT_leather.png")).convert_alpha(),
                        pygame.image.load(os.path.join(walk_path, "FEET_shoes_brown.png")).convert_alpha()
                    ]

        self.model = []
        for sprite in images:
            self.model += [pygame.transform.smoothscale(sprite, (c.PLAYER_X_SIZE * c.WALK_ANIMATION_LENGTH, c.PLAYER_Y_SIZE * 4))]

        images = [pygame.image.load(os.path.join(hurt_path, "BODY_male.png")).convert_alpha(),
                        pygame.image.load(os.path.join(hurt_path, "HEAD_hair_blonde.png")).convert_alpha(),
                        pygame.image.load(os.path.join(hurt_path, "TORSO_leather_armor_shirt_white.png")).convert_alpha(),
                        pygame.image.load(os.path.join(hurt_path, "TORSO_leather_armor_torso.png")).convert_alpha(),
                        pygame.image.load(os.path.join(hurt_path, "TORSO_leather_armor_shoulders.png")).convert_alpha(),
                        pygame.image.load(os.path.join(hurt_path, "TORSO_leather_armor_bracers.png")).convert_alpha(),
                        pygame.image.load(os.path.join(hurt_path, "LEGS_pants_greenish.png")).convert_alpha(),                      
                        pygame.image.load(os.path.join(hurt_path, "BELT_leather.png")).convert_alpha(),
                        pygame.image.load(os.path.join(hurt_path, "FEET_shoes_brown.png")).convert_alpha()
                    ]

        self.hurt_model = []
        for sprite in images:
            self.hurt_model += [pygame.transform.smoothscale(sprite, (c.PLAYER_X_SIZE * c.HURT_ANIMATION_LENGTH, c.PLAYER_Y_SIZE))]          

    def get_next_pos(self):

        # calculate next position
        new_x = self.rect[0] + self.velocity[0]
        new_y = self.rect[1] + self.velocity[1]
        return (new_x,new_y)


    def update(self):

        # calculate next position
        self.rect.move_ip(*self.velocity) 

        self.draw()

    def hurt(self):

        self.hurt_state += 1
        if self.hurt_state >= c.HURT_ANIMATION_LENGTH*c.HURT_ANIMATION_MODIFIER:
            self.hurt_state = (c.HURT_ANIMATION_LENGTH*c.HURT_ANIMATION_MODIFIER)-1

        state = math.floor(self.hurt_state/c.HURT_ANIMATION_MODIFIER)   

        # draw player on map
        src = Rect(state * c.PLAYER_X_SIZE, 0, c.PLAYER_X_SIZE, c.PLAYER_Y_SIZE )
        for sprite in self.hurt_model:
            self.screen.blit(sprite, self.rect, src) 
    
    def draw(self):

        # walking animation
        if self.velocity[0] == 0 and self.velocity[1] == 0:
            self.state = 0
        else:
            self.state += 1
            if self.state >= c.WALK_ANIMATION_LENGTH*c.PLAYER_WALK_ANIMATION_MODIFIER:
                self.state = 1   

        state = math.floor(self.state/c.PLAYER_WALK_ANIMATION_MODIFIER) 

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
        src = Rect(state * c.PLAYER_X_SIZE, self.direction * c.PLAYER_Y_SIZE, c.PLAYER_X_SIZE, c.PLAYER_Y_SIZE )
        for sprite in self.model:
            self.screen.blit(sprite, self.rect, src)            

            