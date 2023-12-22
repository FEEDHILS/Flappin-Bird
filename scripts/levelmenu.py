import pygame as pg
from constants import *
from eventmanager import EventManager
from button import Button
from sys import exit

class LevelMenu():
    def __init__(self):
        self.font = pg.font.Font(FONT, 64)
        self.screen = pg.surface.Surface([W, H])
        self.Sprites = pg.sprite.Group()
        
        self.graphics()

    def graphics(self):
        # NAME OF THE GAME
        self.nametext = self.font.render("Flappin' Bird", False, "white")

        # BACKGROUND INIT AND TILING
        self.bgm = pg.image.load("gfx/background-night.png").convert()
        self.bgm = pg.transform.scale_by(self.bgm, 1.5)
        self.background = self.screen.copy()
        for i in range(W // self.bgm.get_size()[0] + 1):
            self.background.blit(self.bgm, (self.bgm.get_width() * i, 0))

        # BUTTONS
        self.startbutton = Button(self.Sprites, image="gfx/button1.png", 
                                  text="Start Game", position=[W/2, H-150], scale=4,
                                  func=lambda: EventManager.ins.set_timer(100, lambda: EventManager.ins.post_event(LOADLEVEL, {"level": 1})))


    def render(self):
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.nametext, [W/2 - self.nametext.get_width()/2, 150])


    def update(self):
        self.screen.fill("cyan")
        self.render()
        self.Sprites.draw(self.screen)
        self.Sprites.update()