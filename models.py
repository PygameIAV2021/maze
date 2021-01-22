#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  20 10:27:00 2021

@author: jan
"""

import pygame
import random
import os
import const as c

class Models():
    def __init__(self):
        self.load_all_images()

    def load_all_images(self):
        self.body = pygame.transform.smoothscale(pygame.image.load(os.path.join("images", "BODY_skeleton.png")).convert_alpha(),(c.ENEMY_X_SIZE * 9, c.ENEMY_Y_SIZE * 4))
        
        self.heads = [pygame.transform.smoothscale(pygame.image.load(os.path.join("images", "HEAD_robe_hood.png")).convert_alpha(),(c.ENEMY_X_SIZE * 9, c.ENEMY_Y_SIZE * 4)),
                        pygame.transform.smoothscale(pygame.image.load(os.path.join("images", "HEAD_plate_armor_helmet.png")).convert_alpha(),(c.ENEMY_X_SIZE * 9, c.ENEMY_Y_SIZE * 4)),
                        pygame.transform.smoothscale(pygame.image.load(os.path.join("images", "HEAD_chain_armor_helmet.png")).convert_alpha(),(c.ENEMY_X_SIZE * 9, c.ENEMY_Y_SIZE * 4))]
        
        self.belt = [pygame.transform.smoothscale(pygame.image.load(os.path.join("images", "BELT_rope.png")).convert_alpha(),(c.ENEMY_X_SIZE * 9, c.ENEMY_Y_SIZE * 4)),
                        pygame.transform.smoothscale(pygame.image.load(os.path.join("images", "BELT_leather.png")).convert_alpha(),(c.ENEMY_X_SIZE * 9, c.ENEMY_Y_SIZE * 4))]
                
        self.torso = [pygame.transform.smoothscale(pygame.image.load(os.path.join("images", "TORSO_robe_shirt_brown.png")).convert_alpha(),(c.ENEMY_X_SIZE * 9, c.ENEMY_Y_SIZE * 4)),
                        pygame.transform.smoothscale(pygame.image.load(os.path.join("images", "TORSO_plate_armor_torso.png")).convert_alpha(),(c.ENEMY_X_SIZE * 9, c.ENEMY_Y_SIZE * 4)),
                        pygame.transform.smoothscale(pygame.image.load(os.path.join("images", "TORSO_chain_armor_torso.png")).convert_alpha(),(c.ENEMY_X_SIZE * 9, c.ENEMY_Y_SIZE * 4))]
        
        self.legs = [pygame.transform.smoothscale(pygame.image.load(os.path.join("images", "LEGS_robe_skirt.png")).convert_alpha(),(c.ENEMY_X_SIZE * 9, c.ENEMY_Y_SIZE * 4)),
                        pygame.transform.smoothscale(pygame.image.load(os.path.join("images", "LEGS_plate_armor_pants.png")).convert_alpha(),(c.ENEMY_X_SIZE * 9, c.ENEMY_Y_SIZE * 4))]

        self.feet = pygame.transform.smoothscale(pygame.image.load(os.path.join("images", "FEET_plate_armor_shoes.png")).convert_alpha(),(c.ENEMY_X_SIZE * 9, c.ENEMY_Y_SIZE * 4))

    def get_random_enemy_images(self):
        images = []
        
        armor = random.randint(0,3)
        if armor == 0:
            images = [self.body, self.heads[0], self.belt[0], self.torso[0], self.legs[0]]
        elif armor == 1:
            images = [self.body, self.heads[1], self.belt[1], self.torso[1], self.legs[1], self.feet]
        elif armor == 2:
            images = [self.body, self.heads[2], self.belt[0], self.torso[2], self.legs[1]]
        elif armor == 3:
            images = [self.body, self.heads[0], self.belt[0], self.torso[0], self.legs[0]]
        

        return images



    