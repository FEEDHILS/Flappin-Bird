import pygame
from constants import *
from player import Player
from ObstacleSpawner import ObstacleSpawner
from gameoverscreen import GameOver
from sys import exit
from eventmanager import EventManager

class LevelOne():
    def __init__(self) -> None:
        self.Sprites = pygame.sprite.Group() # All sprites, that will be drawn on screen. (By default, please pass this group to all sprites)
        self.player = Player([W/4, H/2]  , self.Sprites)
        self.Spawner = ObstacleSpawner(self.Sprites)
        self.screen = pygame.surface.Surface([W, H])
        self.gameover = None
        self.gameoverGroup = pygame.sprite.Group() # Objects from gameover screen
        self.backgroundinit()
        self.curspeed = 20
        self.stopbg = False

    # Создание заднего фона
    def backgroundinit(self):
        self.bgm = pygame.image.load("gfx/background-night.png").convert()
        self.bgm = pygame.transform.scale_by(self.bgm, 1.5)
        self.background = pygame.surface.Surface([W*2, H])
        for i in range(W*2 // self.bgm.get_width() + 1):
            self.background.blit(self.bgm, (self.bgm.get_width() * i, 0))

        self.bgx = 0

        
    def update(self):
         # ACTUAL GAMEPLAY
        self.Spawner.update()
        self.Sprites.update()
        if not self.stopbg:
            self.bgdraw()
        
        if EventManager.ins.has_event(PLAYERDEAD):
            self.gameover = GameOver(self.gameoverGroup)
            self.Sprites.add(self.gameoverGroup)
            self.stopbg = True

        # Litte GameOverScreen Animation here
        if self.gameover:
            self.curspeed = pygame.math.lerp(self.curspeed, 0, 0.025)
            for sprites in self.gameoverGroup.sprites():
                sprites.ogrect.move_ip(0, self.curspeed)

        # GRAPHICS
        self.screen.blit(self.background, (self.bgx, 0))
        self.Sprites.draw(self.screen)

    def bgdraw(self):
        self.bgx -= 1.5
        if -self.bgx >= W:
            self.bgx = -self.bgm.get_width()/2 + 10 # дерьмо покруче evil floating point bit level hacking
        
       
        