import pygame
from eventmanager import EventManager
from constants import *

class Button(pygame.sprite.Sprite):
    def __init__(self, *groups: pygame.sprite.Group, image : str, text : str, position : tuple, scale=1, func=lambda: print("Button is Pressed")):
        super().__init__(*groups)
        self.ogimage = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale_by(self.ogimage, scale)
        self.func = func

        # ADDING TEXT TO BUTTON
        _text = pygame.font.Font(FONT, 58).render(text, False, BUTTONCOLOR)
        _size = self.image.get_size()
        _tsize = _text.get_size()
        self.image.blit(_text, (_size[0]/2 - _tsize[0]/2, _size[1]/2 - _tsize[1]/2))

        self.rect = self.image.get_rect()
        self.rect.center = position

        # BACKUP
        self.ogrect = self.rect
        self.ogsurf = self.image


    def update(self):
        event = EventManager.ins.has_event(pygame.MOUSEBUTTONDOWN)
        pos = pygame.mouse.get_pos()
        self.hover(1)
        if self.rect.collidepoint(pos):
            self.hover(1.5)
            if event:
                self.hover(0.1)
                self.press_on()
        

    def hover(self, factor):
        current = self.image.get_width() / self.ogsurf.get_width()
        _lerp = pygame.math.lerp( current, factor, 0.1 )
        self.image = pygame.transform.scale_by(self.ogsurf, _lerp)
        self.rect = self.image.get_rect(center=self.ogrect.center)
    
    def press_on(self):
        self.func()