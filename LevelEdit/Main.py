import pygame
import os
from LevelEdit import LevelEdit
from GuiState import GuiState
from GuiManager import GuiManager
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
    sel_obj_gui = GuiState()
    obj_search_gui = GuiState(False)
    toggle_search_gui = GuiState()

    level_options.keybindings.add(LevelSaveBind(pygame.K_F1, level))
    level_options.keybindings.add(LevelLoadBind(pygame.K_F2, load_lvl_gui))
    level_options.keybindings.add(LevelClearBind(pygame.K_F3, clear_lvl_gui))
    level_options.keybindings.add(LevelSaveAsBind(pygame.K_F4, save_lvl_as_gui))
    level_options.add(WINDOW, {'name': "leveloptions", 'cords': (0, 560), 'w': 800, 'h': 40, 'bg_color': (0, 0, 0),
                               'font_color': (234, 234, 234)})
    level_options.add(TEXT, {'name': "keymap", 'cords': (5, 565), 'font_color': (234, 234, 234), 'font_size': 20,
                             'text': "Save Level - F1 Load Level - F2 Clear Level - F3 | Level: ",
                             'watch': level.get_filename})

    load_lvl_gui.add(WINDOW, {'name': 'loadlevel', 'cords': (300, 350), 'w': 300, 'h': 140, 'bg_color': (0, 0, 0),
                                'font_color': (234, 234, 234)})
    load_lvl_gui.add(TEXT, {'name': 'loaddialog', 'cords': (320, 370), 'font_color': (234, 234, 234), 'font_size': 20,
                              'text': 'Filename:', 'watch': ""})
    load_txtbox = load_lvl_gui.add(TXT_BOX, {'name': 'file_txtbox', 'cords': (320, 400), 'bg_color': (255, 255, 255)})
    load_bttn = load_lvl_gui.add(BUTTON, {'name': 'load_bttn', 'cords': (320, 450), 'bg_color': (255, 255, 255),
                                            'font_color': (0, 0, 0), 'font_size': 14,
                                            'text': 'Load Level', 'action': level.load_level})
    load_lvl_gui.keybindings.add(ButtonEnter(pygame.K_RETURN, load_bttn))
    load_bttn.attach(load_txtbox)

    save_lvl_as_gui.add(WINDOW, {'name': 'savelevelas', 'cords': (300, 350), 'w': 300, 'h': 140, 'bg_color': (0, 0, 0),
                                 'font_color': (234, 234, 234)})
    save_lvl_as_gui.add(TEXT, {'name': 'saveasdialog', 'cords': (320, 370), 'font_color': (234, 234, 234), 'font_size': 20,
                               'text': 'Filename:', 'watch': ""})
    save_txtbox = save_lvl_as_gui.add(TXT_BOX, {'name': 'saveas_txtbox', 'cords': (320, 400), 'bg_color': (255, 255, 255)})
    save_bttn = save_lvl_as_gui.add(BUTTON, {'name': 'saveas_bttn', 'cords': (320, 450), 'bg_color': (255, 255, 255),
                                             'font_color': (0, 0, 0), 'font_size': 14,
                                             'text': 'Save Level As', 'action': level.save_level})
    save_lvl_as_gui.keybindings.add(ButtonEnter(pygame.K_RETURN, save_bttn))
    save_bttn.attach(save_txtbox)

    clear_lvl_gui.add(WINDOW, {'name': 'clearlvl', 'cords': (300, 350), 'w': 300, 'h': 140, 'bg_color': (0, 0, 0),
                               'font_color': (234, 234, 234)})
    clear_lvl_gui.add(TEXT, {'name': 'cleardialog', 'cords': (320, 370), 'font_color': (234, 234, 234), 'font_size': 20,
                             'text': 'Clear Level?', 'watch': ""})
    confirm_bttn = clear_lvl_gui.add(BUTTON, {'name': 'confirm_bttn', 'cords': (320, 450), 'bg_color': (255, 255, 255),
                                              'font_color': (0, 0, 0), 'font_size': 14,
                                              'text': 'Confirm', 'action': level.clear_level})

    clear_lvl_gui.keybindings.add(ButtonEnter(pygame.K_RETURN, confirm_bttn))

    sel_obj_gui.keybindings.add(PlaceObjectBind(pygame.MOUSEBUTTONUP, level, obj_search_gui))
    sel_obj_gui.keybindings.add(PlaceObjectBind(pygame.K_RETURN, level, obj_search_gui))

    obj_search_gui.keybindings.add(PrePlaceObjectBind(pygame.MOUSEBUTTONUP, "results", obj_search_gui, level, sel_obj_gui))
    obj_search_gui.keybindings.add(PrePlaceObjectBind(pygame.K_RETURN, "results", obj_search_gui, level, sel_obj_gui))
    obj_search_gui.keybindings.add(ListboxUpBind(pygame.K_UP, "results", obj_search_gui))
    obj_search_gui.keybindings.add(ListboxDownBind(pygame.K_DOWN, "results", obj_search_gui))

    txt_box = obj_search_gui.add(OBJ_S_TXT_BOX, {'name': "c_obj", 'cords': pygame.mouse.get_pos(),
                                                 'bg_color': (255, 255, 255), 'data_path': DATA_PATH})
    results_pos = (txt_box.rect.x, txt_box.rect.y + txt_box.rect.h + 25)
    results = obj_search_gui.add(LIST_BOX, {'name': "results", 'cords': results_pos, 'bg_color': (255, 255, 255)})
    txt_box.attach(results)

    toggle_search_gui.keybindings.add(ToggleSearchBind(pygame.K_SPACE, obj_search_gui, sel_obj_gui))

    gui_manager = GuiManager()
    gui_manager.add(MOVE, toggle_search_gui)
    gui_manager.add(LEVEL_OPTIONS, level_options)
    gui_manager.add(LOAD_LEVEL, load_lvl_gui)
    gui_manager.add(CLEAR_LEVEL, clear_lvl_gui)
    gui_manager.add(SAVE_AS_LEVEL, save_lvl_as_gui)
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
            if event.type == pygame.MOUSEBUTTONUP:
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