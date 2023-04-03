from abc import ABC, abstractmethod
from pygame import Vector2
import pygame as pg


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
        return self.current


class AbstractButton(ABC):
    @abstractmethod
    def isIntersected(self, p: Vector2) -> bool:
        pass

    def isKeyup(self, button_event, p: Vector2) -> bool:
        return self.isIntersected(p) and button_event.isKeyup()

    def isKeydown(self, button_event, p: Vector2) -> bool:
        return self.isIntersected(p) and button_event.isKeydown()

    def isKeyHold(self, button_event, p:Vector2) -> bool:
        return self.isIntersected(p) and button_event.isKeyHold()

