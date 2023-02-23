import pygame as pg
from pygame import Vector2
from AbstractButton import *


class Rect(AbstractButton):
    def __init__(self, size: Vector2):
        self.position = Vector2(0, 0)
        self.size = Vector2(size)
        self.color = pg.Color(255, 255, 255)
        self.outline_thickness = 0.
        self.outline_color = pg.Color(255, 255, 255)

    def draw(self, screen: pg.Surface):
        position = self.position
        size = self.size
        color = self.color
        thickness = self.outline_thickness
        if self.outline_thickness > 0.:
            pg.draw.rect(screen, self.outline_color,
                         (position.x, position.y,
                          size.x, size.y))
        pg.draw.rect(screen, color,
                     (position.x + thickness, position.y + thickness, size.x - thickness*2, size.y - thickness*2))

    def isIntersected(self, point: Vector2) -> bool:
        p = Vector2(point)
        thickness = self.outline_thickness
        return (self.position.x <= p.x <= self.position.x + self.size.x and
                self.position.y <= p.y <= self.position.y + self.size.y)

