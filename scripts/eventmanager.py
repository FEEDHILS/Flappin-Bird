import pygame as pg
from constants import *

class EventManager():
    # Синглетон
    ins = None
    def __new__(cls):
        if cls.ins == None:
            cls.ins = super(EventManager, cls).__new__(cls)
        return cls.ins
    
    def __init__(self):
        self.timers = list()

    # Смотрим события
    def handle(self):
        self.Events = pg.event.get()

        if self.has_event(pg.QUIT):
            pg.quit()
            exit()

        # Закрываем приложение когда "esc" moment...
        keys = self.has_event(pg.KEYDOWN)
        if keys and keys.key == pg.K_ESCAPE:
            pg.event.post(pg.event.Event(pg.QUIT))

        # Выполняем функции наших таймеров
        for funkytown in self.timers:
            if pg.time.get_ticks() >= funkytown["wait"]:
                if funkytown["func"]: funkytown["func"]()
                self.timers.remove(funkytown)


    def set_timer(self, delay, method = None):
        self.timers.append( {"wait": pg.time.get_ticks() + delay, "func": method} )


    def has_event(self, event):
        for events in self.Events:
            if events.type == event:
                return events
        return None
    
    def post_event(self, eventType, params={}):
        event = pg.event.Event(eventType, params)
        pg.event.post(event)
