#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 08:27:00 2020

@author: jan
"""
import pygame
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

        logo = pygame.image.load(os.path.join("images", "logo.png"))
        pygame.display.set_icon(logo)
        pygame.display.set_caption('Mazewalker')

        self.screen = pygame.display.set_mode((c.WINDOW_WIDTH, c.WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

        self.map = Map(self)        

    def run_game(self, x_size, y_size):
        self.current_map = self.map.load_map(x_size,y_size) 
        self.starting_p = self.map.starting_p
        self.ending_p = self.map.ending_p


        self.player = pla.Player(self)
        s_p_0, s_p_1 = self.starting_p
        self.player.rect[0] += s_p_0*c.TILE_SIZE + math.floor((c.TILE_SIZE-self.player.size_x)/2)
        self.player.rect[1] += s_p_1*c.TILE_SIZE + math.floor((c.TILE_SIZE-self.player.size_y)/2)
        running = True   

        while running:
            dt = self.clock.tick(c.FPS) / 1000
            self.screen.fill(c.BLACK)

            mouse_cap = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.player.velocity[1] = -self.player.speed * dt  # 200 pixels per second
                    elif event.key == pygame.K_s:
                        self.player.velocity[1] = self.player.speed * dt
                    elif event.key == pygame.K_a:
                        self.player.velocity[0] = -self.player.speed * dt
                    elif event.key == pygame.K_d:
                        self.player.velocity[0] = self.player.speed * dt
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
                    if event.key == pygame.K_w or event.key == pygame.K_s:
                        self.player.velocity[1] = 0
                    elif event.key == pygame.K_a or event.key == pygame.K_d:
                        self.player.velocity[0] = 0  
                    elif event.key == pygame.K_LSHIFT:
                        self.player.speed = self.player.speed / 2   
                        if self.player.velocity[0] != 0:
                            self.player.velocity[0] = self.player.velocity[0] / 2
                        if self.player.velocity[1] != 0:
                            self.player.velocity[1] = self.player.velocity[1] / 2 
                # elif event.type == pygame.MOUSEMOTION:
                #     if mouse_cap: self.map.scroll(event.rel)
                # elif event.type == pygame.MOUSEBUTTONDOWN:
                #     mouse_cap = True
                #     print("m_c:" + str(mouse_cap))
                # elif event.type == pygame.MOUSEBUTTONUP:
                #     mouse_cap = False
                #     print("m_c:" + str(mouse_cap))

            self.map.draw()

            self.player.update()

            pygame.display.flip()
                

if __name__=="__main__":
    new_game = Game()
    new_game.run_game(20,20)
