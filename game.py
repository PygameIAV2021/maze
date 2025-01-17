#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 08:27:00 2020

@author: jan
"""
import pygame
from pygame import Rect
import os
import sys
import math
import random

import map
import const as c
import player
import enemy
import models

# This class displays and renders maze and player; react to input; return value if won or lost
# Checks for Collisions between player <-> walls, player <-> enemies, enemies <-> walls
# Provide all game functions like pause, winning, loosing, moving of the NPCs etc.


class Game():
    def __init__(self,screen, clock):

        # display screen and set up clock
        self.window_width, self.window_height = c.WINDOW_SIZE
        self.screen = screen
        self.clock = clock

        # load pause screen
        self.pause_screen = pygame.transform.smoothscale(pygame.image.load(os.path.join("images", "Pause.png")).convert_alpha(),((math.floor(self.window_width/3), math.floor(self.window_height/7))))

        # load classes for the map and the player
        self.map = map.Map(self)   
        self.player = player.Player(self)
        self.models = models.Models()

        

    def pause_game(self):

        old_state = self.game_state
        self.game_state = c.game_state.PAUSE

        # loop while paused
        while self.game_state == c.game_state.PAUSE:
            # get ticks per second
            self.dt = self.clock.tick_busy_loop(c.FPS) / 1000

            # set background
            self.screen.fill(c.BLACK)

            # draw pause screen
            self.screen.blit(self.pause_screen, Rect(math.floor(self.window_width / 3),math.floor(self.window_height/7*3), math.floor(self.window_width/3), math.floor(self.window_height/5) ))

            # update screen
            pygame.display.flip()


            # check if game should exit or pause is ended
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                # exit game directly to desktop   
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # end game loop and go back to menu
                        self.game_state = c.game_state.EXIT
                    elif event.key == pygame.K_p:
                        self.game_state = old_state 


    def handle_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
            # exit game directly to desktop   
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                # end game loop and go back to menu
                    self.game_state = c.game_state.EXIT
                # toggle show markers
                elif event.key == pygame.K_m:
                    self.show_markers = not self.show_markers
                elif event.key == pygame.K_t:
                    self.tracking = not self.tracking
                # pause game
                elif event.key == pygame.K_p:
                    self.pause_game()
                # set player velocity after key press
                elif event.key == pygame.K_w:
                    self.player.velocity[1] = -math.floor(self.player.speed * self.dt)
                elif event.key == pygame.K_s:
                    self.player.velocity[1] = math.floor(self.player.speed * self.dt)
                elif event.key == pygame.K_a:
                    self.player.velocity[0] = -math.floor(self.player.speed * self.dt)
                elif event.key == pygame.K_d:
                    self.player.velocity[0] = math.floor(self.player.speed * self.dt)
                # events for speeding up during pressing of l_shift
                elif event.key == pygame.K_LSHIFT:
                    self.player.speed = self.player.speed * 2
                    if self.player.velocity[0] != 0:
                        self.player.velocity[0] = self.player.velocity[0] * 2
                    if self.player.velocity[1] != 0:
                        self.player.velocity[1] = self.player.velocity[1] * 2
                # toggle the scrolling of the map
                elif event.key == pygame.K_z: 
                    self.auto_scrolling = not self.auto_scrolling
                # center the player on the screen
                elif event.key == pygame.K_r:
                    if self.scrolling and not self.auto_scrolling:
                        self.offset = (
                            math.floor(self.window_width / 2) -  self.player.rect[0],
                            math.floor(self.window_height / 2) - self.player.rect[1] 
                            )
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
            elif event.type == pygame.MOUSEMOTION:
                if self.mouse_cap: self.scroll(event.rel)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_cap = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_cap = False

    def scroll(self, rel):

        # get the mouse movement and scroll by that margin
        if self.auto_scrolling or not self.scrolling: return
        
        self.offset = (
            self.offset[0] + rel[0],
            self.offset[1] + rel[1] 
            )

    def do_auto_scroll(self):
        
        # calculate the scrolling offset, but do not move beyond map borders
        if not (self.scrolling and self.auto_scrolling) : return

        x_offset = math.floor(self.window_width / 2) -  self.player.rect[0]
        y_offset = math.floor(self.window_height / 2) - self.player.rect[1]
        
        if x_offset > 0: 
            x_offset = 0
        if x_offset < -((self.map.tiles_x*c.TILE_SIZE) - self.window_width): 
            x_offset = -((self.map.tiles_x*c.TILE_SIZE) - self.window_width)
        
        if y_offset > 0: 
            y_offset = 0
        if y_offset < -((self.map.tiles_y*c.TILE_SIZE) -  self.window_height): 
            y_offset = -((self.map.tiles_y*c.TILE_SIZE) -  self.window_height)

        self.offset = (
            x_offset,
            y_offset 
            )


    def check_target_completion(self):
        
        tmp_rect = Rect(self.player.rect[0],self.player.rect[1],c.PLAYER_SIZE,c.PLAYER_SIZE)

        # calculate the postition of the player in the map array
        x = math.floor((tmp_rect[0] + (c.PLAYER_SIZE / 2)) / c.TILE_SIZE)
        y = math.floor((tmp_rect[1] + (c.PLAYER_SIZE / 2)) / c.TILE_SIZE) 

        ending_x, ending_y = self.ending_p

        if x == ending_x and y == ending_y:
            self.game_state = c.game_state.WIN


    def check_collision(self, new_x, new_y):

        tmp_rect = Rect(new_x,new_y,c.PLAYER_SIZE,c.PLAYER_SIZE)

        # calculate the postition of the player in the map array and add the offset for smaller collision rectangle
        off_top = math.ceil(c.PLAYER_SIZE/3)
        off_bot = math.ceil(c.PLAYER_SIZE/16)
        off_left = math.ceil(c.PLAYER_SIZE/4)
        off_right = math.ceil(c.PLAYER_SIZE/8)

        x_1 = math.floor((tmp_rect[0] + off_left) / c.TILE_SIZE)
        y_1 = math.floor((tmp_rect[1] + off_top) / c.TILE_SIZE) 
        x_2 = math.floor((tmp_rect[0] + c.PLAYER_SIZE  - (2 * off_right)) / c.TILE_SIZE)
        y_2 = math.floor((tmp_rect[1] + c.PLAYER_SIZE  - (2 * off_bot)) / c.TILE_SIZE)

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

            
    def check_enemy_player_collision(self):
        
        # check of any of the enemies collides with the player     
        for enemy in self.enemies:
            # if a collision is detected, end game loop
            if self.player.rect.colliderect(enemy.rect):
                self.game_state = c.game_state.DEATH
                self.foe = enemy


    def set_next_target(self, enemy, last_direction):
        
        # get current position in the array        
        current_x = math.floor(enemy.target[0] / c.TILE_SIZE)
        current_y = math.floor(enemy.target[1] / c.TILE_SIZE)

        # move enemy to target position
        enemy.update(enemy.target[0],enemy.target[1])

        # get all possible directions
        direction = []

        if self.current_map[current_x-1][current_y] >= 0 and self.current_map[current_x-1][current_y] <= 15:
            direction += [c.direction.LEFT]
        if self.current_map[current_x+1][current_y] >= 0 and self.current_map[current_x+1][current_y] <= 15:
            direction += [c.direction.RIGHT]
        if self.current_map[current_x][current_y-1] >= 0 and self.current_map[current_x][current_y-1] <= 15:
            direction += [c.direction.UP]
        if self.current_map[current_x][current_y+1] >= 0 and self.current_map[current_x][current_y+1] <= 15:
            direction += [c.direction.DOWN]

        # get the direction where the enemy entered the current tile
        last_opposite_direction = -1
        if last_direction == c.direction.UP:
            last_opposite_direction = c.direction.DOWN
        elif last_direction == c.direction.DOWN:
            last_opposite_direction = c.direction.UP  
        elif last_direction == c.direction.RIGHT:
            last_opposite_direction = c.direction.LEFT
        elif last_direction == c.direction.LEFT:
            last_opposite_direction = c.direction.RIGHT

        # remove the last opp direction if the are more to choose from
        if len(direction) > 1 and last_opposite_direction in range(0,4):
            direction.remove(last_opposite_direction)

        # randomize possible directions and get one
        random.shuffle(direction)
        new_direction = direction.pop()

        # set the next target and the corresponding movement speed
        if new_direction == c.direction.UP:
            enemy.velocity[0] = 0
            enemy.velocity[1] = -math.floor(enemy.speed * self.dt)
            enemy.target[1] -= c.TILE_SIZE

        elif new_direction == c.direction.DOWN:
            enemy.velocity[0] = 0
            enemy.velocity[1] = math.floor(enemy.speed * self.dt)
            enemy.target[1] += c.TILE_SIZE

        elif new_direction == c.direction.LEFT:
            enemy.velocity[0] = -math.floor(enemy.speed * self.dt)
            enemy.velocity[1] = 0
            enemy.target[0] -= c.TILE_SIZE

        elif new_direction == c.direction.RIGHT:
            enemy.velocity[0] = math.floor(enemy.speed * self.dt)
            enemy.velocity[1] = 0
            enemy.target[0] += c.TILE_SIZE


    def update_enemies(self):
        
        # update every enemy in the array
        for enemy in self.enemies:  

            # get his next position and check if the target is 
            # if the target is not reached move the enemy with his speed and update him
            # if the target is reached get the next target position
            next_x, next_y= enemy.get_next_pos()
            
            if enemy.velocity[0] > 0: # DOWN
                if next_x < enemy.target[0]:
                    enemy.update(next_x,next_y)
                else:
                    self.set_next_target(enemy, c.direction.RIGHT)
            
            elif enemy.velocity[0] < 0: # UP
                if next_x > enemy.target[0]:
                    enemy.update(next_x,next_y)
                else:
                    self.set_next_target(enemy, c.direction.LEFT)
            
            elif enemy.velocity[1] > 0: # RIGHT
                if next_y < enemy.target[1]:
                    enemy.update(next_x,next_y)
                else:
                    self.set_next_target(enemy, c.direction.DOWN)
            
            elif enemy.velocity[1] < 0: # LEFT
                if next_y > enemy.target[1]:
                    enemy.update(next_x,next_y)
                else:
                    self.set_next_target(enemy, c.direction.UP)
            
            #just here for the beginning, when the enemy stands still and in case something weird happens
            else:
                self.set_next_target(enemy, -1)  


    def render_death(self):

        # remove foe from default render list
        self.enemies.remove(self.foe)
        direction = c.direction.DOWN
        # get direction foe has to face

        if abs(self.player.rect[1] - self.foe.rect[1]) > abs(self.player.rect[0] - self.foe.rect[0]):
            if self.player.rect[1] > self.foe.rect[1]:
                direction = c.direction.DOWN
            elif self.player.rect[1] < self.foe.rect[1]: 
                direction = c.direction.UP
        else:
            if self.player.rect[0] > self.foe.rect[0]:
                direction = c.direction.RIGHT
            elif self.player.rect[0] < self.foe.rect[0]: 
                direction = c.direction.LEFT
        
        # play animation twice
        for x in range(0,c.SLASH_ANIMATION_LENGTH*2*c.SLASH_ANIMATION_MODIFIER):

            # draw map and player death
            self.map.draw()
            self.player.hurt()

            # draw enemies
            for bad_guy in self.enemies:
                bad_guy.draw()

            # draw foe
            self.foe.hit(direction)

            pygame.display.flip()          


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
        self.player.rect[0] = s_p_0*c.TILE_SIZE + math.floor((c.TILE_SIZE-c.PLAYER_SIZE)/2)
        self.player.rect[1] = s_p_1*c.TILE_SIZE + math.floor((c.TILE_SIZE-c.PLAYER_SIZE)/2)
        self.player.velocity = [0,0]

        # variable for state of mouse button
        self.mouse_cap = False

        # variable for scrolling
        if self.window_width <= (c.TILE_SIZE * self.map.tiles_x) or self.window_height <= (c.TILE_SIZE * self.map.tiles_y):
            self.scrolling = True
        else:
            self.scrolling = False    

        # current scrolling offset if the map is smaller than the window
        if self.window_width > (c.TILE_SIZE * self.map.tiles_x) or self.window_height > (c.TILE_SIZE * self.map.tiles_y):
            self.offset = (
                math.floor((self.window_width - (c.TILE_SIZE * self.map.tiles_x)) / 2),
                math.floor((self.window_height - (c.TILE_SIZE * self.map.tiles_y)) / 2)
            )
        else:
            self.offset = (0, 0)

        # variable for auto scrolling
        self.auto_scrolling = True

        # Game ending enemy
        self.foe = None

        # track the visited tiles if true
        self.tracking = False

        # variable for showing of tiles visited by the player
        self.show_markers = False

        # main loop variable
        self.game_state = c.game_state.RUNNING   

        # main game loop
        while self.game_state == c.game_state.RUNNING:
            # get ticks per second
            self.dt = self.clock.tick(c.FPS) / 1000

            # set background
            self.screen.fill(c.BLACK)

            # handle all input events
            self.handle_events()

            # move map if auto_scroll is enabled
            if self.auto_scrolling: self.do_auto_scroll()

            # draw map from array
            self.map.draw()

            # update and draw player
            self.update_player()

            # move, update and draw enemies
            self.update_enemies()

            # check for player <-> enemy collision
            if self.game_state == c.game_state.RUNNING:
                self.check_enemy_player_collision()

            # if the game is running check if the player has reached the target position
            if self.game_state == c.game_state.RUNNING: 
                self.check_target_completion()

            pygame.display.flip()

        if self.game_state == c.game_state.DEATH and self.foe is not None:
            self.render_death()

        
        # Reset arrays to dismiss objects
        self.current_map = []
        self.enemies = []

        return self.game_state

