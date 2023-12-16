import pygame
from constants import *
from eventmanager import EventManager
from player import Player
from pipe import Pipe
from sys import exit

### INITIALIZATION ###
pygame.init()
screen = pygame.display.set_mode([W, H])
pygame.display.set_caption("Shitty Bird")
FPS = pygame.time.Clock()

### CREATING STUFF ###
Sprites = pygame.sprite.Group() # All sprites, that will be drawn on screen. (By default, please pass this group to all sprites)
event_handler = EventManager()
player = Player([W/2, H/2]  , Sprites)
testpipe = Pipe(Sprites)

### UPDATE ###
while True:
    # HANDLE EVENTS
    event_handler.update()

    # GRAPHICS
    screen.fill("cyan")
    Sprites.update()
    Sprites.draw(screen)

    # REDRAW    
    pygame.display.flip()
    FPS.tick(60)
    