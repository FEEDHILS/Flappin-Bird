import pygame

class EventManager():
    # SINGLETON
    instance = None
    def __new__(cls):
        if cls.instance == None:
            cls.instance = super(EventManager, cls).__new__(cls)
        return cls.instance

    # CHECKS FOR EVENTS
    def update(self):
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
