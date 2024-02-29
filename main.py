import pygame
import pygwidgets
from classes import *
from abc import ABC, abstractclassmethod

# Create Display Window
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 800
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
timer = pygame.time.Clock() # Timer for FPS
fps = 60
font = pygame.font.Font(None, 36)

# Game States
main_menu = "main"
menu_state = "main"

# Classes

# Helper Fucncitons

# Trackers

# Text

# Input Text

# Buttons
exit_button = pygwidgets.TextButton(window, (290, 450), "Exit", width=200, height=50, fontSize=36)

# Elements


# Game Loop
run = True

while run:
    window.fill(("white"))
    timer.tick(fps)
    
    if menu_state == "main":
        # Main Menu
        exit_button.draw()
        
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if exit_button.handleEvent(event):
                run = False
                
    pygame.display.update()