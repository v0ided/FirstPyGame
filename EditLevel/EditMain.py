__author__ = 'thvoidedline'

import os
from Gui.GuiManager import GuiManager
from Gui.GuiStates.GuiLevelOptions import GuiLevelOptions
from Gui.GuiStates.GuiQuitLevel import GuiQuitLevel
from Gui.GuiStates.GuiObjSearch import GuiObjSearch
from Gui.GuiStates.GuiSelectedObj import GuiSelectedObj
from Gui.GuiStates.GuiStateEditObj import GuiEditObj
from EditLevel.EditLevel import EditLevel
from Binding import *
from Timer import Timer


DATA_PATH = os.path.join('..', 'data')


def edit_main(screen):
    #pygame.init()
    #screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('LevelEdit')
    pygame.mouse.set_visible(1)
    clock = pygame.time.Clock()
    level = EditLevel(2000, 800, 'objects1.ini', DATA_PATH)
    pygame.display.flip()
    screen.blit(level.background, (0, 0))

    level_options = GuiLevelOptions(NON_BLOCKING, level)
    quit_lvl_gui = GuiQuitLevel(NON_BLOCKING, "Quit?")
    obj_search_gui = GuiObjSearch(NON_BLOCKING, level, DATA_PATH)
    select_obj_gui = GuiSelectedObj(NON_BLOCKING, level)
    edit_obj_gui = GuiEditObj(NON_BLOCKING, level)

    gui_manager = GuiManager()
    gui_manager.add(QUIT_GAME, quit_lvl_gui)
    gui_manager.add(OBJECT_SEARCH, obj_search_gui)
    gui_manager.add(LEVEL_OPTIONS, level_options)
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
                        pass
                        #level.mouse_click()
            if event.type > pygame.USEREVENT:
                Timer.handle_event(event.type)

        gui_manager.update()
        level.update()
        level.draw(screen)
        gui_manager.draw(screen)

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()