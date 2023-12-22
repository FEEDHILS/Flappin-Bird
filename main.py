import pygame
from level1 import LevelOne
from levelmenu import LevelMenu
from eventmanager import EventManager
from constants import *

class MainApp():

    def __init__(self):
        ### MAIN INITIALIZATION ###
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode([W, H])
        pygame.display.set_caption("Flappin' Bird")
        self.FPS = pygame.time.Clock()
        self.event_handler = EventManager()

        pygame.event.post(pygame.event.Event(TRANSITIONIN))
        self.level = LevelMenu() # Creating a Level
        self.update()

    def update(self):
        while True:
            # HANDLE EVENTS
            self.event_handler.handle()
            
            #DRAW STUFF
            self.level.update()
            self.screen.blit(self.level.screen, (0,0))

            # REDRAW    
            pygame.display.flip()
            self.FPS.tick(60)

            # LEVEL LOADING  & RELOADING
            loadevent = EventManager.ins.has_event(LOADLEVEL)
            if loadevent:
                if loadevent.level == "LevelOne":
                    self.level = LevelOne()
                elif loadevent.level == "LevelMenu":
                    self.level = LevelMenu()

            loadevent = EventManager.ins.has_event(RELOADLEVEL)
            if loadevent:
                del self.level
                self.level = LevelOne()


if __name__ == "__main__":
    app = MainApp()
    