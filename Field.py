import pygame as pg
from pygame import Vector2
from Cell import *


class Field:
    position = Vector2(0, 0)

    def __init__(self, cell_count: Vector2):
        self.size = cell_count
        size = self.size
        cell_bounds = Vector2(WIN_WIDTH/size.x, WIN_HEIGHT/size.y)
        self.indent = Vector2(cell_bounds.x/16, cell_bounds.y/9)
        self.cell_size = Vector2((WIN_WIDTH)/size.x - self.indent.x, (WIN_HEIGHT )/size.y - self.indent.y)
        self.cells = [[Cell(self, (j, i)) for j in range(int(size.x))] for i in range(int(size.y))]
        y = 0
        for line_of_cells in self.cells:
            x = 0
            for cell in line_of_cells:
                cell.outline = 1
                cell.setPosition(Vector2((cell.rect.size.x + self.indent.x)*x,
                                         (cell.rect.size.y + self.indent.y)*y))
                x += 1
            y += 1

    def setPosition(self, position: Vector2):
        self.position = position
        self.cell_size = Vector2((WIN_WIDTH - position.x)/self.size.x - self.indent.x,
                                 (WIN_HEIGHT - position.y)/self.size.y - self.indent.y)
        y = 0
        for line_of_cells in self.cells:
            x = 0
            for cell in line_of_cells:
                cell.outline = 1
                cell.rect.size = self.cell_size
                cell.setPosition(position + Vector2((cell.rect.size.x + self.indent.x) * x,
                                         (cell.rect.size.y + self.indent.y) * y))
                x += 1
            y += 1

    def update(self):
        for line_of_cells in self.cells:
            for cell in line_of_cells:
                nc = cell.get_neighbour_count()
                cell.text.setText(str(nc))

    next_frame_live_cells = list()
    next_frame_dead_cells = list()

    def nextStep(self):
        nflc = self.next_frame_live_cells
        nfdc = self.next_frame_dead_cells
        for i in range(len(nflc)):
            nflc[i].alive()
        for i in range(len(nfdc)):
            nfdc[i].kill()
        nfdc.clear()
        nflc.clear()
        for y in range(len(self.cells)):
            for x in range(len(self.cells[y])):
                cell = self.cells[y][x]
                nc = cell.get_neighbour_count()
                if nc == 3 and not cell.isLiving():
                    nflc.append(cell)
                if not (nc == 2 or nc == 3) and cell.isLiving():
                    nfdc.append(cell)

    def kill_population(self):
        for y in self.cells:
            for cell in y:
                cell.kill()
        self.next_frame_live_cells.clear()
        self.next_frame_dead_cells.clear()

    def getSize(self):
        return Vector2((WIN_WIDTH - self.position.x), (WIN_HEIGHT - self.position.y))

    def getNeighbourCount(self, id: tuple):
        x = id[0]
        y = id[1]
        sx = int(self.size.x)
        sy = int(self.size.y)
        nc = 0  # neighbour count

        def addIfsLiving(x_, y_):
            if self.cells[y_][x_].isLiving():
                return 1
            return 0

        def getnc(x_, y_):
            ncount = 0
            ncount += addIfsLiving(x_, y_)
            if y_ + 1 < sy:
                ncount += addIfsLiving(x_, y_ + 1)
            if y_ - 1 >= 0:
                ncount += addIfsLiving(x_, y_ - 1)
            return ncount
        if x + 1 < sx:
            nc += getnc(x + 1, y)
        if x - 1 >= 0:
            nc += getnc(x - 1, y)
        if y + 1 < sy:
            nc += addIfsLiving(x, y + 1)
        if y - 1 >= 0:
            nc += addIfsLiving(x, y - 1)
        return nc

    def draw(self, screen: pg.Surface):
        cells = self.cells
        for line_of_cells in cells:
            for cell in line_of_cells:
                cell.draw(screen)
