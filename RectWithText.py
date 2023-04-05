from Rect import *
from Text import *
from AbstractButton import *
from Rect import *


class RectWithText(Rect):
    def __init__(self, size: Vector2, string: str):
        super().__init__(size)
        self.text = Text(string, int(size.y/3))
        self.text.setColor(pg.Color(0, 0, 0))
        self.text.setBackgroundColor(self.color)
        rs = self.size
        ts = self.text.getSize()
        cx = (rs.x - ts.x) / 2
        cy = (rs.y - ts.y) / 2
        self.text.setPosition(self.position + Vector2(cx, cy))

    def setColor(self, color: pg.Color):
        self.color = color
        self.text.setBackgroundColor(self.color)

    def setTextColor(self, color: pg.Color):
        self.text.setColor(color)

    def setPosition(self, position: Vector2):
        self.position = position
        rs = self.size
        ts = self.text.getSize()
        cx = (rs.x - ts.x) / 2
        cy = (rs.y - ts.y) / 2
        self.text.setPosition(self.position + Vector2(cx, cy))

    def setSize(self, size: Vector2):
        self.size = size
        rs = self.size
        ts = self.text.getSize()
        cx = (rs.x - ts.x) / 2
        cy = (rs.y - ts.y) / 2
        self.text.setPosition(self.position + Vector2(cx, cy))

    def setString(self, string: str):
        self.text.setText(string)
        rs = self.size
        ts = self.text.getSize()
        cx = (rs.x - ts.x) / 2
        cy = (rs.y - ts.y) / 2
        self.text.setPosition(self.position + Vector2(cx, cy))

    def draw(self, screen: pg.Surface):
        super().draw(screen)
        self.text.draw(screen)

