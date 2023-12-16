from typing import Any
import pygame
import random
from math import sin
from constants import *

class Pipe(pygame.sprite.Sprite):
    def __init__(self, *groups: pygame.sprite.Group, position=[W, H/2], direction=[-1, 0]):
        super().__init__(*groups)

        # GRAPHICS.
        self.pipeimg = pygame.image.load("graphics/pipe-red.png").convert_alpha() # Load pipe sprite.
        imgsize = self.pipeimg.get_size()
        self.pipeimg = pygame.transform.scale(self.pipeimg, (imgsize[0]*2.25, imgsize[1]*1.5) ) # Scale the pipe.
        self.gap = random.randint(GAP[0], GAP[1]) # Gap between two pipes.
        imgsize = self.pipeimg.get_size() # Refresh size, after we scaled our image.

        self.image = pygame.surface.Surface( (imgsize[0], imgsize[1] * 2 + self.gap), pygame.SRCALPHA ) # Create a big surface for our two pipes
        # ADDING THE PIPES TO SURFACE.
        self.image.blit(pygame.transform.rotate(self.pipeimg, 180), (0, 0))
        self.image.blit(self.pipeimg, (0, imgsize[1] + self.gap))

        self.rect = self.image.get_rect()

        # VARIABLES.
        self.rect.left = position[0]
        self.rect.centery = position[1]
        self.movedir = pygame.Vector2(direction)

    
    def update(self):
        self.rect.move_ip(self.movedir*4)