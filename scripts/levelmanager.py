import pygame as pg
from constants import *
from eventmanager import EventManager
from level1 import LevelOne
from levelmenu import LevelMenu

class LevelManager():

    def __init__(self, _currentLevel : int) -> None:
        self.LoadLevel(_currentLevel)

    def LoadLevel(self, levelIndex : int):
        if levelIndex == 0:
            self.currentLevel = LevelMenu()
        elif levelIndex == 1:
            self.currentLevel = LevelOne()
        self.currentIndex = levelIndex

    def LevelReload(self):
        del self.currentLevel
        self.LoadLevel(self.currentIndex)

    def GetLevel(self):
        return self.currentLevel
    
    def event_handle(self):
        levelEvent = EventManager.ins.has_event(LOADLEVEL)
        if levelEvent:
            self.LoadLevel(levelEvent.dict.get("level", 0))
