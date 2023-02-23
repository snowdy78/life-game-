import pygame as pg
import json
import os
from settings import *
from Rect import *
from Field import *
from Cell import *
from Text import *
from tkinter import *
from RectWithText import *
from Stopwatch import *

pg.init()
pg.font.init()

BLACK = pg.Color(0, 0, 0)
WHITE = pg.Color(255, 255, 255)
GRAY = pg.Color(100, 100, 100)
DARK_GRAY = pg.Color(50, 50, 50)
LIGHT_GRAY = pg.Color(150, 150, 150)
RED = pg.Color(230, 80, 80)
GREEN = pg.Color(80, 210, 80)


def main():
    screen = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    running = True

    field = Field(Vector2(40, 30))
    field_position = Vector2(WIN_WIDTH / 8, WIN_HEIGHT / 9)
    field.setPosition(field_position)

    left_panel = Rect(Vector2(field_position.x - field.cell_size.x / 16, WIN_HEIGHT))
    left_panel.color = BLACK

    top_panel = Rect(Vector2(WIN_WIDTH, field_position.y - field.cell_size.y / 9))
    top_panel.color = BLACK

    top_panel_button_size = Vector2(WIN_WIDTH / 6, field_position.y - 3 * field.cell_size.y / 9)

    next_step_button = RectWithText(top_panel_button_size, "Next")
    next_step_button.setPosition(Vector2(field_position.x - field.cell_size.x / 16, field.cell_size.y / 9))

    auto_button = RectWithText(Vector2(top_panel_button_size), "Auto")
    auto_button.setPosition(Vector2(next_step_button.rect.position.x +
                                    next_step_button.rect.size.x + field.cell_size.x / 16,
                                    next_step_button.rect.position.y))
    auto_button.setColor(pg.Color(RED))
    auto_button_is_active = False

    menu_button = RectWithText(Vector2(field_position.x - 3 * field.cell_size.x / 16, top_panel_button_size.y), "Menu")
    menu_button.setPosition(Vector2(field.cell_size.x / 16, next_step_button.rect.position.y))

    display_neighbour_count = Text("Display neighbour count:", 18)
    display_neighbour_count.setPosition(Vector2(menu_button.rect.position.x, field_position.y - field.cell_size.y / 9))

    is_display_nc_button = Rect(Vector2(field.cell_size))
    is_display_nc_button.position = Vector2(menu_button.rect.position.x +
                                            (menu_button.rect.size.x - is_display_nc_button.size.x) / 2,
                                            menu_button.rect.position.y + display_neighbour_count.position.y +
                                            display_neighbour_count.getSize().y)
    is_display_nc_button.color = pg.Color(GREEN)

    clear_button = RectWithText(Vector2(top_panel_button_size), "Clear")
    clear_button.setPosition(Vector2(auto_button.rect.position.x +
                                     auto_button.rect.size.x + field.cell_size.x / 16,
                                     auto_button.rect.position.y))
    display_cell_outline = Text("Display cell outline:", 18)
    display_cell_outline.setPosition(Vector2(menu_button.rect.position.x,
                                             is_display_nc_button.position.y +
                                             is_display_nc_button.size.y + field.cell_size.y / 9))
    cell_outline_button = Rect(Vector2(field.cell_size))
    cell_outline_button.position = Vector2(is_display_nc_button.position.x,
                                           display_cell_outline.position.y + display_cell_outline.getSize().y)
    cell_outline_button.color = pg.Color(GREEN)

    def onMenuButtonPress():
        pass

    def setAutoButtonActiveStatus(status: bool):
        nonlocal auto_button, auto_button_is_active, next_step_button
        auto_button_is_active = status
        if auto_button_is_active:
            auto_button.setColor(pg.Color(GREEN))
            next_step_button.setColor(pg.Color(LIGHT_GRAY))
            next_step_button.setTextColor(pg.Color(DARK_GRAY))
        else:
            auto_button.setColor(pg.Color(RED))
            next_step_button.setColor(pg.Color(WHITE))
            next_step_button.setTextColor(pg.Color(BLACK))

    def onNextButtonPress():
        nonlocal next_step_button, field
        field.nextStep()

    def onAutoButtonPress():
        nonlocal auto_button_is_active
        setAutoButtonActiveStatus(not auto_button_is_active)

    def onDiplayNCButtonPress():
        nonlocal field, is_display_nc_button
        if is_display_nc_button.color == pg.Color(RED):
            is_display_nc_button.color = pg.Color(GREEN)
            for i in field.cells:
                for cell in i:
                    cell.drawText(True)
        else:
            is_display_nc_button.color = pg.Color(RED)
            for i in field.cells:
                for cell in i:
                    cell.drawText(False)

    def onClearButtonPress():
        nonlocal field
        field.kill_population()
        setAutoButtonActiveStatus(False)

    def onCellPress(cell: Cell):
        if cell.isLiving():
            cell.kill()
        else:
            cell.alive()

    def onDisplayCellOutlineButtonPress():
        nonlocal cell_outline_button, field
        if cell_outline_button.color == pg.Color(GREEN):
            cell_outline_button.color = pg.Color(RED)
            for i in field.cells:
                for cell in i:
                    cell.rect.outline_thickness = 0
        else:
            cell_outline_button.color = pg.Color(GREEN)
            for i in field.cells:
                for cell in i:
                    cell.rect.outline_thickness = 1

    background = Rect(Vector2(WIN_WIDTH, WIN_HEIGHT))
    mouse_event = MouseButtonEvent(0)
    stopwatch = Stopwatch()
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        mouse_event.update()
        mouse_position = Vector2(pg.mouse.get_pos())
        screen.fill((0, 0, 0))
        field.update()

        # rendering
        background.draw(screen)
        left_panel.draw(screen)
        top_panel.draw(screen)
        menu_button.draw(screen)
        next_step_button.draw(screen)
        is_display_nc_button.draw(screen)
        auto_button.draw(screen)
        clear_button.draw(screen)
        display_neighbour_count.draw(screen)
        display_cell_outline.draw(screen)
        cell_outline_button.draw(screen)
        ####
        if menu_button.isKeyup(mouse_event, mouse_position):
            onMenuButtonPress()

        if cell_outline_button.isKeyup(mouse_event, mouse_position):
            onDisplayCellOutlineButtonPress()

        if auto_button.isKeydown(mouse_event, mouse_position):
            onAutoButtonPress()

        if is_display_nc_button.isKeyup(mouse_event, mouse_position):
            onDiplayNCButtonPress()

        if auto_button_is_active and stopwatch.time() // 500 > 0:
            field.nextStep()
            stopwatch.reset()

        if clear_button.isKeyup(mouse_event, mouse_position):
            onClearButtonPress()

        if not auto_button_is_active and next_step_button.isKeyup(mouse_event, mouse_position):
            onNextButtonPress()

        for line_of_cells in field.cells:
            for cell in line_of_cells:
                if cell.rect.isKeydown(mouse_event, mouse_position):
                    onCellPress(cell)

        field.draw(screen)
        pg.display.flip()


if __name__ == '__main__':
    main()
