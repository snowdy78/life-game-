from Field import *
from Stopwatch import *
from CounterButton import *
from SwitcherButton import *

pg.init()
pg.font.init()


screen = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
running = True


def menu():
    global screen, running

    indent = WIN_WIDTH/64
    switcher_size = Vector2(WIN_WIDTH/48, WIN_HEIGHT/18)
    alive_buttons = [SwitcherButton(switcher_size) for i in range(9)]

    def setButtonsPosition(position, buttons):
        nonlocal switcher_size, indent
        id = 0
        for i in buttons:
            i.setPosition(position + Vector2((switcher_size.x + indent) * id, 0))
            id += 1

    still_live_buttons = [SwitcherButton(switcher_size) for i in range(9)]
    alive_size_width = len(alive_buttons)*switcher_size.x + indent*(len(alive_buttons) - 1)
    alive_pos_x = (WIN_WIDTH - alive_size_width)/2
    alive_pos_y = WIN_HEIGHT/3
    slive_pos_y = WIN_HEIGHT*3/5
    setButtonsPosition(Vector2(alive_pos_x, alive_pos_y), alive_buttons)
    setButtonsPosition(Vector2(alive_pos_x, slive_pos_y), still_live_buttons)
    alive_buttons_description = RectWithText(Vector2(WIN_WIDTH/6, WIN_HEIGHT/14), "Alive:")
    slive_buttons_description = RectWithText(Vector2(WIN_WIDTH/6, WIN_HEIGHT/14), "Still live:")
    alive_buttons_description.setPosition(alive_buttons[0].position -
                                          Vector2(alive_buttons_description.size.x + indent, 0))
    slive_buttons_description.setPosition(still_live_buttons[0].position -
                                          Vector2(slive_buttons_description.size.x + indent, 0))
    for i in [slive_buttons_description, alive_buttons_description]:
        i.setColor(BLACK)
        i.setTextColor(WHITE)
    for i in range(len(alive_buttons)):
        alive_buttons[i].setString(str(i))
    for i in range(len(still_live_buttons)):
        still_live_buttons[i].setString(str(i))
    mouse_event = MouseButtonEvent(0)
    for i in json_settings["When-cells-will-alive"]:
        for j in range(len(alive_buttons)):
            if i == j:
                alive_buttons[j].setActive(True)
    for i in json_settings["When-cells-still-live"]:
        for j in range(len(still_live_buttons)):
            if i == j:
                still_live_buttons[j].setActive(True)
    counter_size = Vector2(switcher_size.x, switcher_size.y*2)

    cell_count_width = CounterButton(counter_size, json_settings["cell-count"][0],
                                     CounterButton.Vertical)
    cell_count_height = CounterButton(counter_size, json_settings['cell-count'][1],
                                      CounterButton.Vertical)
    counter_pos_x = (WIN_WIDTH - counter_size.x)/2
    setButtonsPosition(Vector2(counter_pos_x, WIN_HEIGHT/5), [cell_count_width, cell_count_height])
    cell_count_width.setMinimum(1)
    cell_count_height.setMinimum(1)

    while running:
        mouse_event.update()
        mouse_position = Vector2(pg.mouse.get_pos())
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                break
        if pg.key.get_pressed()[pg.K_ESCAPE]:
            json_settings["When-cells-still-live"] = [i for i in range(len(still_live_buttons))
                                                      if still_live_buttons[i].isActive()]
            json_settings["When-cells-will-alive"] = [i for i in range(len(alive_buttons))
                                                      if alive_buttons[i].isActive()]
            json_settings["cell-count"] = [cell_count_width.number, cell_count_height.number]
            with open("settings.json", "w") as f:
                f.write(json.dumps(json_settings))
            return
        screen.fill(BLUE)

        for i in alive_buttons:
            if i.isClicked(mouse_event, mouse_position):
                i.setActive(not i.isActive())
        for i in still_live_buttons:
            if i.isClicked(mouse_event, mouse_position):
                i.setActive(not i.isActive())

        for i, j in zip(alive_buttons, still_live_buttons):
            i.draw(screen)
            j.draw(screen)
        for i in [cell_count_width, cell_count_height]:
            if i.add_button.isClicked(mouse_event, mouse_position):
                i.add()

            if i.sub_button.isClicked(mouse_event, mouse_position):
                i.sub()
            i.draw(screen)
        alive_buttons_description.draw(screen)
        slive_buttons_description.draw(screen)
        pg.display.flip()


def main():
    global screen, running
    field = Field(Vector2(json_settings["cell-count"][0], json_settings["cell-count"][1]))
    field_position = Vector2(WIN_WIDTH / 8, WIN_HEIGHT / 9)
    field.setPosition(field_position)

    left_panel = Rect(Vector2(field_position.x - field.cell_size.x / 16, WIN_HEIGHT))
    left_panel.color = BLUE

    top_panel = Rect(Vector2(WIN_WIDTH, field_position.y - field.cell_size.y / 9))
    top_panel.color = BLUE
    indent_between_buttons = Vector2(field.cell_size.x/16, field.cell_size.y / 9)
    top_panel_button_size = Vector2(WIN_WIDTH / 6, field_position.y - field.cell_size.y / 3)
    left_panel_button_size = Vector2(field.position.x - field.cell_size.x/4, top_panel_button_size.y)
    next_step_button = RectWithText(top_panel_button_size, "Next")
    next_step_button.setPosition(Vector2(field_position.x - indent_between_buttons.x, field.cell_size.y / 9))

    auto_button = SwitcherButton(Vector2(top_panel_button_size), "Auto")
    auto_button.setPosition(Vector2(next_step_button.position.x +
                                    next_step_button.size.x + indent_between_buttons.x,
                                    next_step_button.position.y))

    menu_button = RectWithText(Vector2(field_position.x - 3 * indent_between_buttons.x, top_panel_button_size.y), "Menu")
    menu_button.setPosition(Vector2(indent_between_buttons.x, next_step_button.position.y))

    display_neighbour_count = SwitcherButton(left_panel_button_size, "Display neighbour count:")
    display_neighbour_count.text.setCharSize(int(34*display_neighbour_count.size.y/display_neighbour_count.size.x))
    display_neighbour_count.active_color = RED
    display_neighbour_count.default_color = left_panel.color
    display_neighbour_count.outline_thickness = 1
    display_neighbour_count.updateColor()

    display_neighbour_count.setPosition(Vector2(menu_button.position.x, field_position.y - field.cell_size.y / 9))

    clear_button = RectWithText(Vector2(top_panel_button_size), "Clear")
    clear_button.setPosition(Vector2(auto_button.position.x +
                                     auto_button.size.x + indent_between_buttons.x,
                                     auto_button.position.y))

    display_cell_outline = SwitcherButton(left_panel_button_size, "Display cell outline:")
    display_cell_outline.text.setCharSize(int(34*display_cell_outline.size.y/display_cell_outline.size.x))
    display_cell_outline.active_color = RED
    display_cell_outline.default_color = left_panel.color
    display_cell_outline.outline_thickness = 1
    display_cell_outline.updateColor()

    display_cell_outline.setPosition(Vector2(menu_button.position.x,
                                             display_neighbour_count.position.y +
                                             display_neighbour_count.size.y + indent_between_buttons.y))

    counter_size = Vector2(top_panel_button_size.x / 5, top_panel_button_size.y)
    speed_counter = CounterButton(counter_size, 2, CounterButton.Vertical)
    speed_counter.add_button.outline_thickness = 1
    speed_counter.sub_button.outline_thickness = 1
    speed_counter.show_button.outline_thickness = 1
    speed_counter.setMaximum(20)
    speed_counter.setMinimum(1)
    cb_pos = clear_button.position
    cb_size = clear_button.size
    speed_counter.setPosition(Vector2(cb_pos.x + cb_size.x + WIN_WIDTH / 12, cb_pos.y))
    field.setRules(json_settings["When-cells-will-alive"], json_settings["When-cells-still-live"])


    def setAutoButtonActiveStatus(status: bool):
        nonlocal auto_button, next_step_button
        auto_button.setActive(status)
        if auto_button.isActive():
            next_step_button.setColor(pg.Color(LIGHT_GRAY))
            next_step_button.setTextColor(pg.Color(DARK_GRAY))
        else:
            next_step_button.setColor(pg.Color(WHITE))
            next_step_button.setTextColor(pg.Color(BLACK))

    def onNextButtonPress():
        nonlocal next_step_button, field
        field.nextStep()

    def onAutoButtonPress():
        nonlocal auto_button
        setAutoButtonActiveStatus(not auto_button.isActive())

    def onDiplayNCButtonPress():
        nonlocal field, display_neighbour_count
        if display_neighbour_count.color == RED:
            display_neighbour_count.setColor(left_panel.color)
            for i in field.cells:
                for cell in i:
                    cell.drawText(True)
        else:
            display_neighbour_count.setColor(RED)
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
        nonlocal field
        if display_cell_outline.color == pg.Color(left_panel.color):
            display_cell_outline.setColor(RED)
            for i in field.cells:
                for cell in i:
                    cell.rect.outline_thickness = 0
        else:
            display_cell_outline.setColor(left_panel.color)
            for i in field.cells:
                for cell in i:
                    cell.rect.outline_thickness = 1

    background = Rect(Vector2(WIN_WIDTH, WIN_HEIGHT))
    mouse_event = MouseButtonEvent(0)
    stopwatch = Stopwatch()
    last_clicked_cell = None

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
        auto_button.draw(screen)
        clear_button.draw(screen)
        speed_counter.draw(screen)
        display_neighbour_count.draw(screen)
        display_cell_outline.draw(screen)
        ####

        if speed_counter.add_button.isClicked(mouse_event, mouse_position):
            speed_counter.add()
        if speed_counter.sub_button.isClicked(mouse_event, mouse_position):
            speed_counter.sub()
        if menu_button.isClicked(mouse_event, mouse_position):
            return

        if display_cell_outline.isClicked(mouse_event, mouse_position):
            onDisplayCellOutlineButtonPress()

        if auto_button.isClicked(mouse_event, mouse_position):
            onAutoButtonPress()

        if display_neighbour_count.isClicked(mouse_event, mouse_position):
            onDiplayNCButtonPress()

        if auto_button.isActive() and stopwatch.time() // (1000/speed_counter.number) > 0:
            stopwatch.reset()
            before_living_cells = []
            for cell_line in field.cells:
                for cell in cell_line:
                    before_living_cells.append(cell.isLiving())
            field.nextStep()
            after_living_cells = []
            for cell_line in field.cells:
                for cell in cell_line:
                    after_living_cells.append(cell.isLiving())
            if before_living_cells == after_living_cells:
                setAutoButtonActiveStatus(False)

        if clear_button.isClicked(mouse_event, mouse_position):
            onClearButtonPress()

        if not auto_button.isActive() and next_step_button.isClicked(mouse_event, mouse_position):
            onNextButtonPress()

        for line_of_cells in field.cells:
            for cell in line_of_cells:
                if cell.rect.isKeydown(mouse_event, mouse_position):
                    last_clicked_cell = cell
                    onCellPress(cell)
                    break
                elif mouse_event.isKeyup():
                    last_clicked_cell = None
                    break
                elif last_clicked_cell is not None:
                    if cell.isLiving() != last_clicked_cell.isLiving() and cell.rect.isKeyHold(mouse_event, mouse_position):
                        if last_clicked_cell.isLiving():
                            cell.alive()
                            break
                        cell.kill()
                        break
        field.draw(screen)
        pg.display.flip()


if __name__ == '__main__':
    menus = [main, menu]  # work for two menus
    running = True
    while running:
        for m in menus:
            m()
            if not running:
                break
        if not running:
            break
