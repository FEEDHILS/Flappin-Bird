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
    
    def update(self):
        self.event_handle()
        

    def difficulty(self):
        pass # Тут будет менятся delay и также возможно с увеличением сложности, появятся трубы с более узкими проемами и трубы, движущиеся вверх-вниз

    def event_handle(self):
        if EventManager.ins.has_event(SPAWNPIPE):
            if not self.stopped:
                self.pipes.append(Pipe(self.group, position=[W, randint(MAXOFFSET[0], MAXOFFSET[1])] ,direction=[-3, 0]))
                self.timer = pygame.time.set_timer(SPAWNPIPE, self.delay, loops=1)

        if EventManager.ins.has_event(PLAYERDEAD):
            for i in self.pipes:
                i.movedir = [0, 0]
            self.stopped = True
            print("Nigga deadass")

