import pygame as pg
from constants import *
from player import Player
from obstaclespawner import ObstacleSpawner
from gameoverscreen import GameOver

from eventmanager import EventManager

class LevelOne():
    def __init__(self) -> None:
        # Объектики
        self.Sprites = pg.sprite.Group() # Тут все спрайты отрисовываются, тут круто!
        self.player = Player([W/4, H/2]  , self.Sprites)
        self.Spawner = ObstacleSpawner(self.Sprites)
        self.screen = pg.surface.Surface([W, H])

        self.gameover = None # Создадим его позже, когда игрок помрет.
        self.gameoverGroup = pg.sprite.Group() # Группа для объектов экрана смерти

        self.font = self.font = pygame.font.Font(FONT, 64)
        self.score = 0
        self.backgroundinit()

        # всякий мусор
        self.stopbg = False
        self.curspeed = 20
        self._remberpipe = list() # ностальгия по трубам...
        self.scoresound = pg.mixer.Sound("sounds/sound_point.wav")


    # Генерим задний фон
    def backgroundinit(self):
        self.bgm = pg.image.load("gfx/background-night.png").convert()
        self.bgm = pg.transform.scale_by(self.bgm, 1.5)
        self.background = pg.surface.Surface([W*2, H])
        for i in range(W*2 // self.bgm.get_width() + 1):
            self.background.blit(self.bgm, (self.bgm.get_width() * i, 0))

        self.bgx = 0

        
    def update(self):
        # База
        self.Spawner.update()
        self.Sprites.update()
        self.event_handle()
        # Возможность остановить прокрутку задника. Если например игрок помер(rip)
        if not self.stopbg:
            self.bgdraw()

        # Небольшая анимация для экрана смерти (не синего...)
        if self.gameover:
            self.curspeed = pg.math.lerp(self.curspeed, 0, 0.025)
            for sprites in self.gameoverGroup.sprites():
                sprites.ogrect.move_ip(0, self.curspeed)

        # Графика
        self.screen.blit(self.background, (self.bgx, 0))
        self.Sprites.draw(self.screen)
        scoretext = self.font.render( "Score: " + str(self.score), False, "white" )
        self.screen.blit( scoretext, (W/2 - scoretext.get_width()/2, 0))

    def bgdraw(self):
        self.bgx -= 1.5
        if -self.bgx >= W:
            self.bgx = -self.bgm.get_width()/2 + 10 # дерьмо покруче evil floating point bit hacking

    def event_handle(self):
        if EventManager.ins.has_event(PLAYERDEAD):
            self.gameover = GameOver(self.gameoverGroup)
            self.Sprites.add(self.gameoverGroup)
            self.stopbg = True

        # Обновляем счетчик.
        scoreEvent = EventManager.ins.has_event(SCOREUP)
        if scoreEvent:
            if scoreEvent.dict.get("pipe") not in self._remberpipe:
                self.score += 1
                self.scoresound.play()
                self._remberpipe.append( scoreEvent.dict.get("pipe") )
        
       
        