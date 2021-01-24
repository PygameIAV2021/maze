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
        logo = pygame.image.load(os.path.join("images", "logo.png"))
        pygame.display.set_icon(logo)
        pygame.display.set_caption('Mazewalker')

        # display screen and set up clock
        self.screen = pygame.display.set_mode((c.WINDOW_WIDTH, c.WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

        self.game = game.Game(self.screen, self.clock)

        self.run_game()

    def run_game(self):
        self.game.run_game(20,20)

if __name__=="__main__":
    new_Main = Main()