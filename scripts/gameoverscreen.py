from typing import Any
import pygame as pg
from button import Button
from constants import *
from levelmenu import LevelMenu
from eventmanager import EventManager

class GameOver(pg.sprite.Sprite):
    def __init__(self, *groups: pg.sprite.Group):
        super().__init__(*groups)

        self.image = pg.image.load("gfx/gameoverscreen.png").convert_alpha()
        self.image = pg.transform.scale_by(self.image, 6)
        self.rect = self.image.get_rect()
        self.rect.center = [W/2, -H/2]
        self.ogrect = self.rect
        self.ogimg = self.image
        self.group = groups[1]

        self.slidespeed = 20 # Для анимаций
        self.start(groups)

    def reload(self): EventManager.ins.set_timer(100, lambda: EventManager.ins.post_event(LOADLEVEL, {"level": 1}))
    
    def leave(self): EventManager.ins.set_timer(100, lambda: EventManager.ins.post_event(LOADLEVEL, {"level": 0}))


    def start(self, *groups: pg.sprite.Group):
        pos = (self.rect.left + 150, self.rect.centery + 50)

        self.retrybutton = Button(groups, image="gfx/button1.png", text="Retry", 
                                  position=pos, scale=2.5, func=self.reload)
    

        pos = (self.rect.centerx + 120, self.rect.centery + 50)

        self.leavebutton = Button(groups, image="gfx/button2.png", text="", 
                                  position=pos, scale=2.5, func=self.leave)
        
    def update(self):
        # Небольшая анимация
        self.slidespeed = pg.math.lerp(self.slidespeed, 0, 0.025)
        for sprites in self.group:
            sprites.ogrect.move_ip(0, self.slidespeed)
        