from colors import *


class Text:
    def __init__(self, text: str, char_size: int):
        self.position = Vector2(0, 0)
        self.char_size = int(char_size)
        self.path = r'fonts/Winston/Winston-Regular.ttf'
        self.font = pg.font.Font(self.path, self.char_size)
        self.color = Color(255, 255, 255)
        self.bg_color = Color(0, 0, 0, 0)
        self.content = str(text)

    def setColor(self, color: Color):
        self.color = color

    def getSize(self):
        return Vector2(self.font.size(self.content))

    def setBackgroundColor(self, color: Color):
        self.bg_color = color

    def setFont(self, filepath: str):
        self.path = filepath
        self.font = pg.font.Font(filepath, self.char_size)

    def setCharSize(self, size):
        self.char_size = size
        self.font = pg.font.Font(self.path, self.char_size)

    def setPosition(self, pos: Vector2):
        self.position = pos

    def setText(self, text: str):
        self.content = str(text)

    def draw(self, screen: pg.Surface):
        txt = self.font.render(self.content, True, self.color, self.bg_color)
        screen.blit(txt, (floor(self.position.x), floor(self.position.y)))
