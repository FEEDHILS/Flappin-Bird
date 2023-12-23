import pygame as pg
from constants import *
from player import Player
from obstaclespawner import ObstacleSpawner
from gameoverscreen import GameOver

from eventmanager import EventManager

class LevelOne():
    def __init__(self):
        # Объектики
        self.Sprites = pg.sprite.Group() # Тут все спрайты отрисовываются, тут круто!
        self.player = Player([W/4, H/2]  , self.Sprites)
        self.Spawner = ObstacleSpawner(self.Sprites)
        self.screen = pg.surface.Surface([W, H])

        self.gameover = None # Создадим его позже, когда игрок помрет.
        self.gameoverGroup = pg.sprite.Group() # Группа для объектов экрана смерти

        self.font = self.font = pygame.font.Font(FONT, 64)
        self.score = 0

        # всякий мусор
        self.stopbg = False
        self.bgx =0
        self.scoresound = pg.mixer.Sound("sounds/sound_point.wav")
        self.scoresound.set_volume(0.1)
        self.daybgm = self.backgroundinit()
        self.nightbgm = self.backgroundinit(state="night")
        self.nightbgm.set_alpha(0)
        self.bgalpha = 0



    # Генерим задний фон
    def backgroundinit(self, state="day"):
        bgm = pg.image.load(f"gfx/background-{state}.png").convert()
        bgm = pg.transform.scale_by(bgm, 1.5)
        background = pg.surface.Surface([W*2, H])
        for i in range(W*2 // bgm.get_width() + 1):
            background.blit(bgm, (bgm.get_width() * i, 0))

        return background

    def basegeneration(self):
        base = pg.image.load("gfx/base.png").convert_alpha()
        base = pg.transform.scale_by(base, 2)
        plane = pg.surface.Surface((base.get_width()*3, base.get_height()))
        for i in range(3):
            plane.blit(base, (base.get_width()*i, 0))

        return plane

        
    def update(self):
        # База
        self.Spawner.update()
        self.Sprites.update()
        self.event_handle()

        self.bgdraw()

        # Графика
        self.screen.blit(self.daybgm, (self.bgx, 0))
        self.screen.blit(self.nightbgm, (self.bgx, 0))
        self.screen.blit(self.basegeneration(), (self.bgx*2, H-50))

        self.Sprites.draw(self.screen)
        scoretext = self.font.render( "Score: " + str(self.score), False, "white" )
        self.screen.blit( scoretext, (W/2 - scoretext.get_width()/2, 0))

    def bgdraw(self):
        # Смещение задника
        self.bgx -= 1.5 * (not self.stopbg)
        if -self.bgx >= W:
            self.bgx = -216 + 10 # дерьмо покруче evil floating point bit hacking
    

        # Переход задника из дневного в ночной.
        if self.score >= 15:
            self.bgalpha = pg.math.lerp(self.bgalpha, 255, 0.01)
            self.nightbgm.set_alpha(self.bgalpha)


    def event_handle(self):
        if EventManager.ins.has_event(PLAYERDEAD):
            self.gameover = GameOver(self.Sprites, self.gameoverGroup)
            self.stopbg = True

        # Обновляем счетчик.
        scoreEvent = EventManager.ins.has_event(SCOREUP)
        if scoreEvent:
            self.score += 1
            self.Spawner._score += 1
            self.scoresound.play()
       
        