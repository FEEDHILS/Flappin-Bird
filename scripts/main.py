import pygame as pg
from levelmanager import LevelManager
from eventmanager import EventManager
from constants import *

class MainApp():

    def __init__(self):
        ### MAIN INITIALIZATION ###
        pg.init()
        pg.font.init()
        self.screen = pg.display.set_mode([W, H])
        pg.display.set_caption("Flappin' Bird")
        self.FPS = pg.time.Clock()
        self.event_handler = EventManager()
        self.lvlManager = LevelManager(0)
        pg.mixer.music.load("sounds/music.wav")
        pg.mixer.music.play(-1)
        self.update()



    def update(self):
        while True:
            # HANDLE EVENTS
            self.event_handler.handle()
            self.lvlManager.event_handle()
            
            #DRAW STUFF
            level = self.lvlManager.GetLevel()
            level.update()
            self.screen.blit(level.screen, (0,0))

            # REDRAW    
            pg.display.flip()
            self.FPS.tick(60)


if __name__ == "__main__":
    app = MainApp()
    