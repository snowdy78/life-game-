from Rect import *
from Text import *


class Cell:
    text_will_drawn = True

    def __init__(self, field, id: tuple, liveness: bool = False):
        self.rect = Rect(field.cell_size)
        self.liveness = liveness
        self.ID = tuple(id)
        self.field = field
        self.rect.outline_thickness = 1
        self.rect.outline_color = pg.Color(0, 0, 0)
        self.text = Text("0", field.cell_size.y/1.8)
        self.alive()
        self.kill()

    def setPosition(self, position: Vector2):
        self.rect.position = position
        rs = self.rect.size
        ts = self.text.getSize()
        cx = (rs.x - ts.x)/2
        cy = (rs.y - ts.y)/2
        self.text.setPosition(position + Vector2(cx, cy))

    def drawText(self, condition: bool):
        self.text_will_drawn = condition

    def alive(self):
        if not self.isLiving():
            self.rect.color = pg.Color(0, 0, 0)
            self.text.setColor(pg.Color(255, 255, 255))
            self.text.setBackgroundColor(pg.Color(0, 0, 0))
            self.liveness = True

    def kill(self):
        if self.isLiving():
            self.rect.color = pg.Color(255, 255, 255)
            self.text.setColor(pg.Color(0, 0, 0))
            self.text.setBackgroundColor(pg.Color(255, 255, 255))
            self.liveness = False

    def isLiving(self):
        return self.liveness

    def get_neighbour_count(self):
        return self.field.getNeighbourCount(self.ID)

    def draw(self, screen: pg.Surface):
        self.rect.draw(screen)
        if self.text_will_drawn:
            self.text.draw(screen)


