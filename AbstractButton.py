from abc import ABC, abstractmethod
from pygame import Vector2
import pygame as pg
from settings import *


class MouseButtonEvent:
    before = False

    def __init__(self, mouse_button: int):
        self.button = mouse_button
        self.current = pg.mouse.get_pressed(3)[mouse_button]

    def update(self) -> None:
        self.before = self.current
        self.current = pg.mouse.get_pressed(3)[self.button]

    def isKeydown(self) -> bool:
        return not self.before and self.current

    def isKeyup(self) -> bool:
        return self.before and not self.current

    def isKeyHold(self):
        return self.before and self.current


class AbstractButton(ABC):
    __ready_to_click = False

    @abstractmethod
    def isIntersected(self, p: Vector2) -> bool:
        pass

    def isKeyup(self, button_event, p: Vector2) -> bool:
        return self.isIntersected(p) and button_event.isKeyup()

    def isKeydown(self, button_event, p: Vector2) -> bool:
        return self.isIntersected(p) and button_event.isKeydown()

    def isKeyHold(self, button_event, p:Vector2) -> bool:
        return self.isIntersected(p) and button_event.isKeyHold()

    def isClicked(self, button_event, p: Vector2) -> bool:
        if self.isKeydown(button_event, p):
            self.__ready_to_click = True
        elif button_event.isKeyup() and self.__ready_to_click:
            self.__ready_to_click = False
            return self.isIntersected(p)
        return False
