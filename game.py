#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 08:27:00 2020

@author: jan
"""
import pygame
from pygame import Rect
import player as pla
import os
import math
from map import Map
import const as c

# main file and switches between menu and maze
# Display and render maze and player; react to input; return value if won or lost

class Game():
    def __init__(self):
        successes, failures = pygame.init()
        print("Initializing pygame: {0} successes and {1} failures.".format(successes, failures))

        # load and set logo; set window title
        logo = pygame.image.load(os.path.join("images", "logo.png"))
        pygame.display.set_icon(logo)
        pygame.display.set_caption('Mazewalker')

        # display screen and set up clock
        self.screen = pygame.display.set_mode((c.WINDOW_WIDTH, c.WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

        # load classes for the map and the player
        self.map = Map(self)   
        self.player = pla.Player(self)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                # set player velocity after key press
                elif event.key == pygame.K_w:
                    self.player.velocity[1] = -self.player.speed * self.dt
                elif event.key == pygame.K_s:
                    self.player.velocity[1] = self.player.speed * self.dt
                elif event.key == pygame.K_a:
                    self.player.velocity[0] = -self.player.speed * self.dt
                elif event.key == pygame.K_d:
                    self.player.velocity[0] = self.player.speed * self.dt
                # events for speeding up during pressing of l_shift
                elif event.key == pygame.K_LSHIFT:
                    self.player.speed = self.player.speed * 2
                    if self.player.velocity[0] != 0:
                        self.player.velocity[0] = self.player.velocity[0] * 2
                    if self.player.velocity[1] != 0:
                        self.player.velocity[1] = self.player.velocity[1] * 2
                # elif event.key == pygame.K_z: 
                #     self.map.scrolling = not self.map.scrolling
                #     print(self.map.scrolling)
            elif event.type == pygame.KEYUP:
                # reset player velocity after key release
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    self.player.velocity[1] = 0
                elif event.key == pygame.K_a or event.key == pygame.K_d:
                    self.player.velocity[0] = 0  
                # events for slowing down after release of l_shift
                elif event.key == pygame.K_LSHIFT:
                    self.player.speed = self.player.speed / 2   
                    if self.player.velocity[0] != 0:
                        self.player.velocity[0] = self.player.velocity[0] / 2
                    if self.player.velocity[1] != 0:
                        self.player.velocity[1] = self.player.velocity[1] / 2 
            # elif event.type == pygame.MOUSEMOTION:
            #     if self.mouse_cap: self.map.scroll(event.rel)
            # elif event.type == pygame.MOUSEBUTTONDOWN:
            #     self.mouse_cap = True
            #     print("m_c:" + str(mouse_cap))
            # elif event.type == pygame.MOUSEBUTTONUP:
            #     self.mouse_cap = False
            #     print("m_c:" + str(mouse_cap))

    def check_target_completion(self):
        
        tmp_rect = Rect(self.player.rect[0],self.player.rect[1],c.PLAYER_X_SIZE,c.PLAYER_Y_SIZE)
        # if map is offset add offset to player model
        if self.map.scrolling:
            tmp_rect[0] += self.map.offset[0]
            tmp_rect[1] += self.map.offset[1]

        # calculate the postition of the player in the map array
        x_1 = math.floor(tmp_rect[0] / c.TILE_SIZE)
        y_1 = math.floor(tmp_rect[1] / c.TILE_SIZE) 
        x_2 = math.floor((tmp_rect[0] + c.PLAYER_X_SIZE) / c.TILE_SIZE)
        y_2 = math.floor((tmp_rect[1] + c.PLAYER_Y_SIZE) / c.TILE_SIZE)

        # add for collisions
        collision = 0

        # check all for corners of the player for collision
        if self.current_map[x_1][y_1] == c.draw_v.END:
            collision += 1
        if self.current_map[x_1][y_2] == c.draw_v.END :
            collision += 2
        if self.current_map[x_2][y_1] == c.draw_v.END :
            collision += 4
        if self.current_map[x_2][y_2] == c.draw_v.END :
            collision += 8   
        
        # check if all four corners are on the target
        if collision == 15:
            return True
        else:
            return False

    def check_collision(self, new_x, new_y):

        tmp_rect = Rect(new_x,new_y,c.PLAYER_X_SIZE,c.PLAYER_Y_SIZE)
        # if map is offset add offset to player model
        if self.map.scrolling:
            tmp_rect[0] += self.map.offset[0]
            tmp_rect[1] += self.map.offset[1]

        # calculate the postition of the player in the map array
        x_1 = math.floor(tmp_rect[0] / c.TILE_SIZE)
        y_1 = math.floor(tmp_rect[1] / c.TILE_SIZE) 
        x_2 = math.floor((tmp_rect[0] + c.PLAYER_X_SIZE) / c.TILE_SIZE)
        y_2 = math.floor((tmp_rect[1] + c.PLAYER_Y_SIZE) / c.TILE_SIZE)

        # add for collisions
        collision = 0

        # check all for corners of the player for collision
        if self.current_map[x_1][y_1] < 0 or self.current_map[x_1][y_1] >= 20:
            collision += 1
        if self.current_map[x_1][y_2] < 0 or self.current_map[x_1][y_2] >= 20:
            collision += 2
        if self.current_map[x_2][y_1] < 0 or self.current_map[x_2][y_1] >= 20:
            collision += 4
        if self.current_map[x_2][y_2] < 0 or self.current_map[x_2][y_2] >= 20:
            collision += 8   

        # if no corner detects a collision, do nothing
        if collision == 0:
            pass
        # if only one corner detects a collision, only remove the velocity towards that wall
        elif collision == 1:
            if self.player.velocity[1] < 0:
                self.player.velocity[1] = 0
            if self.player.velocity[0] < 0:
                self.player.velocity[0] = 0 
        elif collision == 2:
            if self.player.velocity[1] > 0:
                self.player.velocity[1] = 0
            if self.player.velocity[0] < 0:
                self.player.velocity[0] = 0 
        elif collision == 4:
            if self.player.velocity[1] < 0:
                self.player.velocity[1] = 0
            if self.player.velocity[0] > 0:
                self.player.velocity[0] = 0 
        elif collision == 8:
            if self.player.velocity[1] > 0:
                self.player.velocity[1] = 0
            if self.player.velocity[0] > 0:
                self.player.velocity[0] = 0

        # if two corners detect a collision always remove the x or y velocity   
        elif collision == 3 or collision == 12:
            self.player.velocity[0] = 0
        elif collision == 5 or collision == 10:
            self.player.velocity[1] = 0  

        # if more than two corners detect a collision, remove all velocity   
        else:
            self.player.velocity[0] = 0 
            self.player.velocity[1] = 0                         
        
    def run_game(self, x_size, y_size):

        # load new map from generator
        self.current_map = self.map.load_map(x_size,y_size) 

        # get starting and end point for player
        self.starting_p = self.map.starting_p
        self.ending_p = self.map.ending_p

        # set starting coordinates for player
        s_p_0, s_p_1 = self.starting_p
        self.player.rect[0] += s_p_0*c.TILE_SIZE + math.floor((c.TILE_SIZE-c.PLAYER_X_SIZE)/2)
        self.player.rect[1] += s_p_1*c.TILE_SIZE + math.floor((c.TILE_SIZE-c.PLAYER_Y_SIZE)/2)

        # variable for state of mouse button
        # self.mouse_cap = False

        # main loop variable => false if won or quit
        self.running = True   

        # main game loop
        while self.running:
            # get ticks per second
            self.dt = self.clock.tick(c.FPS) / 1000

            # set background
            self.screen.fill(c.BLACK)

            # handle all input events
            self.handle_events()

            # draw map from array
            self.map.draw()

            # get position for player after next movement
            next_x, next_y= self.player.getNextPos()

            x_velo = self.player.velocity[0]
            y_velo = self.player.velocity[1]

            # check if the player has moved if any collision occurs
            if next_x != self.player.rect[0] or next_y != self.player.rect[1]:
                self.check_collision(next_x,next_y)

            # update player position and draw him on top of map
            self.player.update()

            self.player.velocity[0] = x_velo
            self.player.velocity[1] = y_velo

            # if the game is running check if the player has reached the target position
            if self.running: self.running = not self.check_target_completion()

            pygame.display.flip()
                

if __name__=="__main__":
    new_game = Game()
    new_game.run_game(20,20)
