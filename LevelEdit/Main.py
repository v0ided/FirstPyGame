import pygame
import os
from LevelEdit import LevelEdit
from GuiState import GuiState
from GuiManager import GuiManager
from Binding import *
from Timer import Timer


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('LevelEdit')
    pygame.mouse.set_visible(1)
    clock = pygame.time.Clock()
    level = LevelEdit(2000, 800, os.path.join('../', 'data', 'level_data', 'objects1.ini'))
    pygame.display.flip()
    screen.blit(level.background, (0, 0))

    level_options = GuiState()
    sel_obj_gui = GuiState()
    obj_search_gui = GuiState(False)
    toggle_search_gui = GuiState()

    level_options.keybindings.add(LevelSaveBind(pygame.K_F1, level))
    level_options.keybindings.add(LevelLoadBind(pygame.K_F2, level))
    level_options.keybindings.add(LevelClearBind(pygame.K_F3, level))
    level_options.add(WINDOW, "leveloptions", (0, 560), w=800, h=40, bg_color=(0, 0, 0), font_color=(234, 234, 234))
    level_options.add(TEXT, "keymap", (5, 565), font_color=(234, 234, 234), font_size=24,
                      text="Save Level - F1  Load Level - F2  Clear Level - F3")

    sel_obj_gui.keybindings.add(PlaceObjectBind(pygame.MOUSEBUTTONUP, level, obj_search_gui))
    sel_obj_gui.keybindings.add(PlaceObjectBind(pygame.K_RETURN, level, obj_search_gui))

    obj_search_gui.keybindings.add(PrePlaceObjectBind(pygame.MOUSEBUTTONUP, "results", obj_search_gui, level, sel_obj_gui))
    obj_search_gui.keybindings.add(PrePlaceObjectBind(pygame.K_RETURN, "results", obj_search_gui, level, sel_obj_gui))
    obj_search_gui.keybindings.add(ListboxUpBind(pygame.K_UP, "results", obj_search_gui))
    obj_search_gui.keybindings.add(ListboxDownBind(pygame.K_DOWN, "results", obj_search_gui))

    txt_box = obj_search_gui.add(TXT_BOX, "c_obj", pygame.mouse.get_pos())
    results_pos = (txt_box.cords[X], txt_box.cords[Y] + txt_box.h + 25)
    results = obj_search_gui.add(LIST_BOX, "results", results_pos)
    txt_box.attach(results)

    toggle_search_gui.keybindings.add(ToggleSearchBind(pygame.K_SPACE, obj_search_gui, sel_obj_gui))

    gui_manager = GuiManager()
    gui_manager.add(MOVE, toggle_search_gui)
    gui_manager.add(LEVEL_OPTIONS, level_options)
    gui_manager.add(OBJECT_SEARCH, obj_search_gui)
    gui_manager.add(SELECT_OBJECT, sel_obj_gui)

    while 1:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            if event.type == pygame.KEYUP:
                gui_manager.input(event.key)
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                gui_manager.input(event.type)
            if event.type > pygame.USEREVENT:
                Timer.handle_event(event.type)

        gui_manager.update()
        mousepos = pygame.mouse.get_pos()
        level.update_pre_place_pos(mousepos[X], mousepos[Y])
        level.update()
        level.draw(screen)
        gui_manager.draw(screen)

        pygame.display.flip()

if __name__ == '__main__': main()