#майнкрафт спавнер)
import pygame
from pipe import Pipe
from constants import *
from eventmanager import EventManager
from random import randint
class ObstacleSpawner():
    def __init__(self, SpriteGroup : pygame.sprite.Group) -> None:
        self.group = SpriteGroup
        self.delay = 3000
        self.timer = pygame.time.set_timer(SPAWNPIPE, self.delay, loops=1)
        self.pipes = list()
        self.stopped = False
        self.speed = -3.0
        self.color = "red"
        self.pipetype = 0
        self._score = 0

    def update(self):
        self.event_handle()

    def event_handle(self):
        # Вечный двигатель... труб.
        if EventManager.ins.has_event(SPAWNPIPE):
            if not self.stopped:
                self.pipes.append( Pipe(self.group, position=[W, randint(MAXOFFSET[0], MAXOFFSET[1])], 
                                       color=self.color ,speed=self.speed, pipetype=self.pipetype) )
                self.timer = pygame.time.set_timer(SPAWNPIPE, self.delay, loops=1)

        # Останавливаем все трубы, если игрок, к сожалению, скончался...
        if EventManager.ins.has_event(PLAYERDEAD):
            for i in self.pipes:
                i.movedir = [0, 0]
            self.stopped = True
        
        # Меняем Сложность
        if EventManager.ins.has_event(SCOREUP):
            self.speed -= 0.15
            if self._score == 15:
                self.pipetype = 1
                self.color = "green"
