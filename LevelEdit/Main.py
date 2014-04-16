__author__ = 'thvoidedline'

import os
from Gui.GuiManager import GuiManager
from Gui.GuiStateOLD import GuiState
from LevelEdit import LevelEdit
from Binding import *
from Timer import Timer


DATA_PATH = os.path.join('..', 'data')


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('LevelEdit')
    pygame.mouse.set_visible(1)
    clock = pygame.time.Clock()
    level = LevelEdit(2000, 800, 'objects1.ini', DATA_PATH)
    pygame.display.flip()
    screen.blit(level.background, (0, 0))

    level_options = GuiState()
    load_lvl_gui = GuiState(False)
    save_lvl_as_gui = GuiState(False)
    clear_lvl_gui = GuiState(False)
    quit_lvl_gui = GuiState(False)
    pre_place_gui = GuiState()
    obj_search_gui = GuiState(False)
    toggle_search_gui = GuiState()
    select_obj_gui = GuiState()
    edit_obj_gui = GuiState(False)

    gui_manager = GuiManager()
    gui_manager.add(MOVE, toggle_search_gui)
    gui_manager.add(LEVEL_OPTIONS, level_options)
    gui_manager.add(LOAD_LEVEL, load_lvl_gui)
    gui_manager.add(CLEAR_LEVEL, clear_lvl_gui)
    gui_manager.add(SAVE_AS_LEVEL, save_lvl_as_gui)
    gui_manager.add(QUIT_GAME, quit_lvl_gui)
    gui_manager.add(OBJECT_SEARCH, obj_search_gui)
    gui_manager.add(PRE_PLACE, pre_place_gui)
    gui_manager.add(SEL_OBJ, select_obj_gui)
    gui_manager.add(EDIT_OBJ, edit_obj_gui)

    while 1:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == QUIT_EVENT:
                return
            if event.type == pygame.KEYUP:
                gui_manager.input(event.key)
            if event.type == pygame.MOUSEBUTTONUP:
                #temp fix, ignores all other mouse buttons from recv input
                if event.button == 1:
                    if not gui_manager.input(event.type):
                        level.input(event.type)
            if event.type > pygame.USEREVENT:
                Timer.handle_event(event.type)

        gui_manager.update()
        level.update()
        level.draw(screen)
        gui_manager.draw(screen)

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()

if __name__ == '__main__': main()