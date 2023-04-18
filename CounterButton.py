from RectWithText import *


class CounterButton:

    class Vertical:
        pass

    class Horizontal:
        pass

    def __init__(self, size: Vector2, show_number: int, align: type):
        self.size = Vector2(size)
        self.number = int(show_number)
        self.align = align
        if align is self.Vertical:
            self.add_button = RectWithText(Vector2(size.x, size.y/3), "+")
            self.sub_button = RectWithText(Vector2(size.x, size.y/3), "-")
            self.show_button = RectWithText(Vector2(size.x, size.y / 3), str(show_number))

        elif align is self.Horizontal:
            self.add_button = RectWithText(Vector2(size.x/3, size.y), "+")
            self.sub_button = RectWithText(Vector2(size.x/3, size.y), "-")
            self.show_button = RectWithText(Vector2(size.x/3, size.y), str(show_number))
        else:
            assert False, "[ERROR] Invalid align type"
        self.setPosition(Vector2(0, 0))
        self.increment = 1
        self.maximum = None
        self.minimum = None

    def setPosition(self, position: Vector2):
        size = self.size
        self.add_button.setPosition(position)
        if self.align is self.Vertical:
            self.sub_button.setPosition(position + Vector2(0, 2 * size.y / 3))
            self.show_button.setPosition(position + Vector2(0, size.y / 3))
        else:
            self.sub_button.setPosition(position + Vector2(2*size.x/3, 0))
            self.show_button.setPosition(position + Vector2(size.x / 3, 0))

    def setSize(self, size:Vector2):
        self.size = size
        if self.align is self.Vertical:
            self.add_button.setSize(Vector2(size.x, size.y/3))
            self.sub_button.setSize(Vector2(size.x, size.y/3))
            self.show_button.setSize(Vector2(size.x, size.y/3))
        else:
            self.add_button.setSize(Vector2(size.x/3, size.y))
            self.sub_button.setSize(Vector2(size.x/3, size.y))
            self.show_button.setSize(Vector2(size.x/3, size.y))
        self.setPosition(self.add_button.rect.position)

    def setIncrement(self, add_value: int):
        self.increment = add_value

    def clamp(self):
        n = int(self.number)
        if self.minimum is not None:
            n = max(n, self.minimum)
        if self.maximum is not None:
            n = min(n, self.maximum)
        self.number = n

    def setMaximum(self, maximum):
        self.maximum = maximum
        self.number = min(self.number, maximum)

    def setMinimum(self, minimum):
        self.minimum = minimum
        self.number = max(self.number, minimum)

    def add(self):
        self.number += self.increment
        self.clamp()
        self.show_button.setString(str(self.number))

    def sub(self):
        self.number -= self.increment
        self.clamp()
        self.show_button.setString(str(self.number))

    def setShowings(self, number: int):
        self.number = number
        self.clamp()
        self.show_button.setString(str(self.number))

    def draw(self, screen: pg.Surface):
        self.add_button.draw(screen)
        self.sub_button.draw(screen)
        self.show_button.draw(screen)
