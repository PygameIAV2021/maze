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

# This class just loads all sprites for the enemies and returns one of serveral sets of sprites

class Models():
    def __init__(self):

        self.load_all_images()


    def load_all_images(self):

        walk_path = os.path.join("images","walk")

        slash_path = os.path.join("images","slash")

        walk_x = c.ENEMY_SIZE * c.WALK_ANIMATION_LENGTH
        walk_y = c.ENEMY_SIZE * 4

        slash_x = c.ENEMY_SIZE * c.SLASH_ANIMATION_LENGTH
        slash_y =  c.ENEMY_SIZE * 4

        self.body = pygame.transform.smoothscale(pygame.image.load(os.path.join(walk_path, "BODY_skeleton.png")).convert_alpha(),(walk_x, walk_y))
        
        self.heads = [pygame.transform.smoothscale(pygame.image.load(os.path.join(walk_path, "HEAD_robe_hood.png")).convert_alpha(),(walk_x, walk_y)),
                        pygame.transform.smoothscale(pygame.image.load(os.path.join(walk_path, "HEAD_plate_armor_helmet.png")).convert_alpha(),(walk_x, walk_y)),
                        pygame.transform.smoothscale(pygame.image.load(os.path.join(walk_path, "HEAD_chain_armor_helmet.png")).convert_alpha(),(walk_x, walk_y))]
        
        self.belt = [pygame.transform.smoothscale(pygame.image.load(os.path.join(walk_path, "BELT_rope.png")).convert_alpha(),(walk_x, walk_y)),
                        pygame.transform.smoothscale(pygame.image.load(os.path.join(walk_path, "BELT_leather.png")).convert_alpha(),(walk_x, walk_y))]
                
        self.torso = [pygame.transform.smoothscale(pygame.image.load(os.path.join(walk_path, "TORSO_robe_shirt_brown.png")).convert_alpha(),(walk_x, walk_y)),
                        pygame.transform.smoothscale(pygame.image.load(os.path.join(walk_path, "TORSO_plate_armor_torso.png")).convert_alpha(),(walk_x, walk_y)),
                        pygame.transform.smoothscale(pygame.image.load(os.path.join(walk_path, "TORSO_chain_armor_torso.png")).convert_alpha(),(walk_x, walk_y))]
        
        self.legs = [pygame.transform.smoothscale(pygame.image.load(os.path.join(walk_path, "LEGS_robe_skirt.png")).convert_alpha(),(walk_x, walk_y)),
                        pygame.transform.smoothscale(pygame.image.load(os.path.join(walk_path, "LEGS_plate_armor_pants.png")).convert_alpha(),(walk_x, walk_y))]

        self.feet = pygame.transform.smoothscale(pygame.image.load(os.path.join(walk_path, "FEET_plate_armor_shoes.png")).convert_alpha(),(walk_x, walk_y))

        
        self.s_body = pygame.transform.smoothscale(pygame.image.load(os.path.join(slash_path, "BODY_skeleton.png")).convert_alpha(),(slash_x, slash_y))
        
        self.s_heads = [pygame.transform.smoothscale(pygame.image.load(os.path.join(slash_path, "HEAD_robe_hood.png")).convert_alpha(),(slash_x, slash_y)),
                        pygame.transform.smoothscale(pygame.image.load(os.path.join(slash_path, "HEAD_plate_armor_helmet.png")).convert_alpha(),(slash_x, slash_y)),
                        pygame.transform.smoothscale(pygame.image.load(os.path.join(slash_path, "HEAD_chain_armor_helmet.png")).convert_alpha(),(slash_x, slash_y))]
        
        self.s_belt = [pygame.transform.smoothscale(pygame.image.load(os.path.join(slash_path, "BELT_rope.png")).convert_alpha(),(slash_x, slash_y)),
                        pygame.transform.smoothscale(pygame.image.load(os.path.join(slash_path, "BELT_leather.png")).convert_alpha(),(slash_x, slash_y))]
                
        self.s_torso = [pygame.transform.smoothscale(pygame.image.load(os.path.join(slash_path, "TORSO_robe_shirt_brown.png")).convert_alpha(),(slash_x, slash_y)),
                        pygame.transform.smoothscale(pygame.image.load(os.path.join(slash_path, "TORSO_plate_armor_torso.png")).convert_alpha(),(slash_x, slash_y)),
                        pygame.transform.smoothscale(pygame.image.load(os.path.join(slash_path, "TORSO_chain_armor_torso.png")).convert_alpha(),(slash_x, slash_y))]
        
        self.s_legs = [pygame.transform.smoothscale(pygame.image.load(os.path.join(slash_path, "LEGS_robe_skirt.png")).convert_alpha(),(slash_x, slash_y)),
                        pygame.transform.smoothscale(pygame.image.load(os.path.join(slash_path, "LEGS_plate_armor_pants.png")).convert_alpha(),(slash_x, slash_y))]

        self.s_feet = pygame.transform.smoothscale(pygame.image.load(os.path.join(slash_path, "FEET_plate_armor_shoes.png")).convert_alpha(),(slash_x, slash_y))

        self.s_weapon = [pygame.transform.smoothscale(pygame.image.load(os.path.join(slash_path, "WEAPON_longsword.png")).convert_alpha(),(slash_x, slash_y)),
                        pygame.transform.smoothscale(pygame.image.load(os.path.join(slash_path, "WEAPON_dagger.png")).convert_alpha(),(slash_x, slash_y)),
                        pygame.transform.smoothscale(pygame.image.load(os.path.join(slash_path, "WEAPON_rapier.png")).convert_alpha(),(slash_x, slash_y))]


    def get_random_enemy_images(self):

        walk = []
        slash = []
        #random.randint(0,2)
        armor = random.randint(0,3)
        if armor == 0:
            walk = [self.body, self.heads[0], self.belt[0], self.torso[0], self.legs[0]]
            slash = [self.s_body, self.s_heads[0], self.s_belt[0], self.s_torso[0], self.s_legs[0],self.s_weapon[random.randint(0,2)]]
        elif armor == 1:
            walk = [self.body, self.heads[1], self.belt[1], self.torso[1], self.legs[1], self.feet]
            slash = [self.s_body, self.s_heads[1], self.s_belt[1], self.s_torso[1], self.s_legs[1], self.s_feet,self.s_weapon[random.randint(0,2)]]
        elif armor == 2:
            walk = [self.body, self.heads[2], self.belt[0], self.torso[2], self.legs[1]]
            slash = [self.s_body, self.s_heads[2], self.s_belt[0], self.s_torso[2], self.s_legs[1],self.s_weapon[random.randint(0,2)]]
        elif armor == 3:
            walk = [self.body, self.heads[0], self.belt[0], self.torso[0], self.legs[0]]
            slash = [self.s_body, self.s_heads[0], self.s_belt[0], self.s_torso[0], self.s_legs[0],self.s_weapon[random.randint(0,2)]]        

        return (walk, slash)



    