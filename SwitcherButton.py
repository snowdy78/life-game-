from RectWithText import *


class SwitcherButton(RectWithText):
    def __init__(self, size: Vector2, text: str = "", is_active: bool = False):
        super().__init__(size, text)
        self.active_color = GREEN
        self.default_color = RED
        self.is_active = is_active
        self.updateColor()

    def updateColor(self):
        self.setColor(self.active_color if self.is_active else self.default_color)

    def setActive(self, is_active):
        self.is_active = is_active
        self.updateColor()

    def isActive(self) -> bool:
        return self.is_active

