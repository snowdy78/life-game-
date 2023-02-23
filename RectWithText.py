from Rect import *
from Text import *
from AbstractButton import *


class RectWithText(AbstractButton):
    def __init__(self, size: Vector2, string: str):
        self.rect = Rect(size)
        self.text = Text(string, int(size.y/3))
        self.text.setColor(pg.Color(0, 0, 0))
        self.text.setBackgroundColor(self.rect.color)
        rs = self.rect.size
        ts = self.text.getSize()
        cx = (rs.x - ts.x) / 2
        cy = (rs.y - ts.y) / 2
        self.text.setPosition(self.rect.position + Vector2(cx, cy))

    def setColor(self, color: pg.Color):
        self.rect.color = color
        self.text.setBackgroundColor(self.rect.color)

    def setTextColor(self, color: pg.Color):
        self.text.setColor(color)

    def setPosition(self, position: Vector2):
        self.rect.position = position
        rs = self.rect.size
        ts = self.text.getSize()
        cx = (rs.x - ts.x) / 2
        cy = (rs.y - ts.y) / 2
        self.text.setPosition(self.rect.position + Vector2(cx, cy))

    def setSize(self, size: Vector2):
        self.rect.size = size
        rs = self.rect.size
        ts = self.text.getSize()
        cx = (rs.x - ts.x) / 2
        cy = (rs.y - ts.y) / 2
        self.text.setPosition(self.rect.position + Vector2(cx, cy))

    def setString(self, string: str):
        self.text.setText(string)
        rs = self.rect.size
        ts = self.text.getSize()
        cx = (rs.x - ts.x) / 2
        cy = (rs.y - ts.y) / 2
        self.text.setPosition(self.rect.position + Vector2(cx, cy))

    def draw(self, screen: pg.Surface):
        self.rect.draw(screen)
        self.text.draw(screen)

    def isIntersected(self, p: Vector2) -> bool:
        return self.rect.isIntersected(p)
