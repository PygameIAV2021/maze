#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  24 13:18:00 2021

@author: jan
"""
import pygame
import os

import const as c
import game

class Main():
    def __init__(self):
        
        successes, failures = pygame.init()
        print("Initializing pygame: {0} successes and {1} failures.".format(successes, failures))

        # load and set logo; set window title
        logo = pygame.transform.smoothscale(pygame.image.load(os.path.join("images", "logo.png")),(16,16))
        pygame.display.set_icon(logo)
        pygame.display.set_caption('Mazewalker')

        # display screen and set up clock
        self.screen = pygame.display.set_mode((c.WINDOW_WIDTH, c.WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

        self.game = game.Game(self.screen, self.clock)

        self.display_menu()

    def display_menu(self):
        
        show_menu = True
        while show_menu:
            self.screen.fill(c.BLACK)

            pygame.display.flip()

            for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            show_menu = False
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                show_menu = False
                            if event.key == pygame.K_RETURN:
                                self.game.run_game(20,20)
            

if __name__=="__main__":
    new_Main = Main()