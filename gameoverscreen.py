from typing import Any
import pygame
from button import Button
from constants import *
from levelmenu import LevelMenu

class GameOver(pygame.sprite.Sprite):
    def __init__(self, *groups: pygame.sprite.Group):
        super().__init__(*groups)

        self.image = pygame.image.load("gfx/gameoverscreen.png").convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 6)
        self.rect = self.image.get_rect()
        self.rect.center = [W/2, -H/2]
        self.ogrect = self.rect
        self.ogimg = self.image
        self.start(groups)

    def reload(self):
        pygame.time.set_timer(pygame.event.Event(RELOADLEVEL), 100, loops=1)
    
    def leave(self):
        pygame.time.set_timer(pygame.event.Event(LOADLEVEL, level="LevelMenu"), 100, loops=1)

    def start(self, *groups: pygame.sprite.Group):
        pos = (self.rect.left + 150, self.rect.centery + 50)

        self.retrybutton = Button(groups, image="gfx/button1.png", text="Retry", 
                                  position=pos, scale=2.5, func=self.reload)
    

        pos = (self.rect.centerx + 120, self.rect.centery + 50)

        self.leavebutton = Button(groups, image="gfx/button2.png", text="", 
                                  position=pos, scale=2.5, func=self.leave)
        

    def update(self):
        pass
        