#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 08:27:00 2020

@author: jan
"""
import pygame
from pygame import Rect
import player as pla
import enemy
import models
import os
import math
import map
import random
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
        self.map = map.Map(self)   
        self.player = pla.Player(self)
        self.models = models.Models()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                # toggle show markers
                elif event.key == pygame.K_m:
                    self.show_markers = not self.show_markers
                elif event.key == pygame.K_t:
                    self.tracking = not self.tracking
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
        x = math.floor((tmp_rect[0] + (c.PLAYER_X_SIZE / 2)) / c.TILE_SIZE)
        y = math.floor((tmp_rect[1] + (c.PLAYER_Y_SIZE / 2)) / c.TILE_SIZE) 

        ending_x, ending_y = self.ending_p

        if x == ending_x and y == ending_y:
            return True
        else:
            return False

    def check_collision(self, new_x, new_y):

        tmp_rect = Rect(new_x,new_y,c.PLAYER_X_SIZE,c.PLAYER_Y_SIZE)
        # if map is offset add offset to player model
        if self.map.scrolling:
            tmp_rect[0] += self.map.offset[0]
            tmp_rect[1] += self.map.offset[1]

        # calculate the postition of the player in the map array and add the offset for smaller collision rectangle
        x_1 = math.floor((tmp_rect[0] + c.COLLISION_OFFSET_LEFT) / c.TILE_SIZE)
        y_1 = math.floor((tmp_rect[1] + c.COLLISION_OFFSET_TOP) / c.TILE_SIZE) 
        x_2 = math.floor((tmp_rect[0] + c.PLAYER_X_SIZE  - (2 * c.COLLISION_OFFSET_RIGHT)) / c.TILE_SIZE)
        y_2 = math.floor((tmp_rect[1] + c.PLAYER_Y_SIZE  - (2 * c.COLLISION_OFFSET_BOTTOM)) / c.TILE_SIZE)

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

    def update_player(self):

            # get position for player after next movement
            next_x, next_y= self.player.get_next_pos()

            x_velo = self.player.velocity[0]
            y_velo = self.player.velocity[1]

            # check if the player has moved if any collision occurs
            if next_x != self.player.rect[0] or next_y != self.player.rect[1]:
                self.check_collision(next_x,next_y)

            # update player position and draw him on top of map
            self.player.update()

            if self.tracking: self.map.update_tracker(self.player.rect)

            self.player.velocity[0] = x_velo
            self.player.velocity[1] = y_velo   

    def set_next_target(self, enemy, last_direction):
        current_x = math.floor(enemy.target[0] / c.TILE_SIZE)
        current_y = math.floor(enemy.target[1] / c.TILE_SIZE)

        enemy.update_to(enemy.target[0],enemy.target[1])

        direction = []

        if self.current_map[current_x-1][current_y] >= 0 and self.current_map[current_x-1][current_y] <= 15:
            direction += [c.direction.LEFT]
        if self.current_map[current_x+1][current_y] >= 0 and self.current_map[current_x+1][current_y] <= 15:
            direction += [c.direction.RIGHT]
        if self.current_map[current_x][current_y-1] >= 0 and self.current_map[current_x][current_y-1] <= 15:
            direction += [c.direction.UP]
        if self.current_map[current_x][current_y+1] >= 0 and self.current_map[current_x][current_y+1] <= 15:
            direction += [c.direction.DOWN]


        last_opposite_direction = -1
        if last_direction == c.direction.UP:
            last_opposite_direction = c.direction.DOWN
        elif last_direction == c.direction.DOWN:
            last_opposite_direction = c.direction.UP  
        elif last_direction == c.direction.RIGHT:
            last_opposite_direction = c.direction.LEFT
        elif last_direction == c.direction.LEFT:
            last_opposite_direction = c.direction.RIGHT

        if len(direction) > 1 and last_opposite_direction in range(0,4):
            direction.remove(last_opposite_direction)

        random.shuffle(direction)

        new_direction = direction.pop()

        if new_direction == c.direction.UP:
            enemy.velocity[0] = 0
            enemy.velocity[1] = -enemy.speed * self.dt
            enemy.target[1] -= c.TILE_SIZE

        elif new_direction == c.direction.DOWN:
            enemy.velocity[0] = 0
            enemy.velocity[1] = enemy.speed * self.dt
            enemy.target[1] += c.TILE_SIZE

        elif new_direction == c.direction.LEFT:
            enemy.velocity[0] = -enemy.speed * self.dt
            enemy.velocity[1] = 0
            enemy.target[0] -= c.TILE_SIZE

        elif new_direction == c.direction.RIGHT:
            enemy.velocity[0] = enemy.speed * self.dt
            enemy.velocity[1] = 0
            enemy.target[0] += c.TILE_SIZE

    def update_enemies(self):
        for enemy in self.enemies:  
            next_x, next_y= enemy.get_next_pos()

            if enemy.velocity[0] > 0: # DOWN
                if next_x < enemy.target[0]:
                    enemy.update()
                else:
                    self.set_next_target(enemy, c.direction.RIGHT)
            
            elif enemy.velocity[0] < 0: # UP
                if next_x > enemy.target[0]:
                    enemy.update()
                else:
                    self.set_next_target(enemy, c.direction.LEFT)
            
            elif enemy.velocity[1] > 0: # RIGHT
                if next_y < enemy.target[1]:
                    enemy.update()
                else:
                    self.set_next_target(enemy, c.direction.DOWN)
            
            elif enemy.velocity[1] < 0: # LEFT
                if next_y > enemy.target[1]:
                    enemy.update()
                else:
                    self.set_next_target(enemy, c.direction.UP)
            
            else:
                self.set_next_target(enemy, -1)            


    def run_game(self, x_size, y_size):

        # load new map from generator
        self.current_map = self.map.load_map(x_size,y_size) 

        # get starting and end point for player
        self.starting_p = self.map.starting_p
        self.ending_p = self.map.ending_p

        # get amount and position of enemies
        self.enemies = []
        for spawn in self.map.spawn_p:
            self.enemies += [enemy.Enemy(self,spawn,self.models)]

        # set starting coordinates for player
        s_p_0, s_p_1 = self.starting_p
        self.player.rect[0] += s_p_0*c.TILE_SIZE + math.floor((c.TILE_SIZE-c.PLAYER_X_SIZE)/2)
        self.player.rect[1] += s_p_1*c.TILE_SIZE + math.floor((c.TILE_SIZE-c.PLAYER_Y_SIZE)/2)

        # variable for state of mouse button
        # self.mouse_cap = False

        # track the visited tiles if true
        self.tracking = False

        # variable for showing of tiles visited by the player
        self.show_markers = False

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

            # update and draw player
            self.update_player()

            # move, update and draw enemies
            self.update_enemies()

            # if the game is running check if the player has reached the target position
            if self.running: self.running = not self.check_target_completion()

            pygame.display.flip()
                

if __name__=="__main__":
    new_game = Game()
    new_game.run_game(20,20)
