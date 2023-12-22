import pygame
from constants import *

class EventManager():
    # SINGLETON
    ins = None
    def __new__(cls):
        if cls.ins == None:
            cls.ins = super(EventManager, cls).__new__(cls)
        return cls.ins

    # CHECKS FOR EVENTS
    def handle(self):
        self.Events = pygame.event.get()

        if self.has_event(pygame.QUIT):
            pygame.quit()
            exit()

        # CLOSING THE APP WHEN ESC IS PRESSED
        keys = self.has_event(pygame.KEYDOWN)
        if keys and keys.key == pygame.K_ESCAPE:
            pygame.event.post(pygame.event.Event(pygame.QUIT))



    def has_event(self, event):
        for events in self.Events:
            if events.type == event:
                return events
        return None
