#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  24 13:18:00 2021

@author: jan
"""
import pygame
from pygame import Rect
import os
import math

import const as c
import game

# This class manages the menu and starts the game after the corresponding player input

class Main():
    def __init__(self):
        
        successes, failures = pygame.init()
        print("Initializing pygame: {0} successes and {1} failures.".format(successes, failures))

        # load and set logo; set window title
        logo = pygame.transform.smoothscale(pygame.image.load(os.path.join("images", "logo.png")),(16,16))
        pygame.display.set_icon(logo)
        pygame.display.set_caption('Mazewalker')

        # display screen and set up clock
        self.window_w, self.window_h = c.WINDOW_SIZE
        self.screen = pygame.display.set_mode((self.window_w, self.window_h))
        self.clock = pygame.time.Clock()

        # load WIN, DEATH and STARTING screen
        self.top_width, self.top_height = c.MENU_TOP_SIZE
        self.bot_width, self.bot_height = c.MENU_BOT_SIZE
        self.start_screen = pygame.transform.smoothscale(pygame.image.load(os.path.join("images", "Start.png")).convert_alpha(),(self.top_width, self.top_height))
        self.death_screen = pygame.transform.smoothscale(pygame.image.load(os.path.join("images", "Death.png")).convert_alpha(),(self.top_width, self.top_height))
        self.win_screen = pygame.transform.smoothscale(pygame.image.load(os.path.join("images", "Win.png")).convert_alpha(),(self.top_width, self.top_height))
        
        # load menu screen
        self.menu_screen = pygame.transform.smoothscale(pygame.image.load(os.path.join("images", "Menu.png")).convert_alpha(),(self.bot_width, self.bot_height))

        # create game object
        self.game = game.Game(self.screen, self.clock)

        # display menu and go to menu loop
        self.display_menu()

    def display_menu(self):

        self.state = c.game_state.EXIT
        
        show_menu = True
        
        # main loop for displaying the menu with the correct banner on top ("You died","You Won","Mazewalker") 
        while show_menu:
            self.screen.fill(c.BLACK)

            # Get position for top banner
            top_dest = Rect(math.floor(self.window_w / 2)-math.floor(self.top_width / 2),math.floor(self.window_h / 4)-math.floor(self.top_height / 2),self.top_width,self.top_height)
            
            if self.state == c.game_state.EXIT:                
                self.screen.blit(self.start_screen, top_dest)
            elif self.state == c.game_state.WIN:
                self.screen.blit(self.win_screen, top_dest)
            elif self.state == c.game_state.DEATH:
                self.screen.blit(self.death_screen, top_dest)

            # Get position for bottom menu
            bot_dest = Rect(math.floor(self.window_w / 2)-math.floor(self.bot_width / 2),math.floor(self.window_h / 4)-math.floor(self.bot_height / 2) + math.floor(self.window_h / 2),self.bot_width,self.bot_height)
            self.screen.blit(self.menu_screen, bot_dest)

            pygame.display.flip()
            
            #check for player inputs
            for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            show_menu = False
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                show_menu = False
                            if event.key == pygame.K_RETURN:
                                self.state = self.game.run_game(20,20)
            

if __name__=="__main__":
    new_Main = Main()