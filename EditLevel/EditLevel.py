__author__ = 'thvoidedline'

import configparser
import collections
from EditLevel.EditCamera import EditCamera
from EditLevel.SelectionTarget import SelectionTarget
from Level import Level
from ObjectFactory import ObjFactory
from HelpFunctions import *
from Gui.GuiStates.GuiLevelOptions import GuiLevelOptions
from Gui.GuiStates.GuiQuitLevel import GuiQuitLevel
from Gui.GuiStates.GuiObjSearch import GuiObjSearch
from Gui.GuiStates.GuiEditObj import GuiEditObj
from Objects.Part import Part


class EditLevel(Level):
    def __init__(self, w, h, filename, data_path):
        #If a blank filename is passed, create a new level file 'new_level_1.ini, if the file exists in level_data,
        #increment i until a filename that does not exist in working dir is found
        if os.path.isfile(os.path.join(data_path, 'level_data', filename)):
            print("Existing level found, loading..")
        else:
            if filename is "":
                i = 0
                while True:
                    i += 1
                    filename = 'new_level_' + str(i) + '.ini'
                    if not os.path.isfile(os.path.join(data_path, 'level_data', filename)):
                        break

        Level.__init__(self, w, h, filename, data_path)
        self.selected_obj = None
        self.camera = EditCamera(800, 600, 2000, 800)
        #offsets from selected object's top left corner to mouse at time of selection
        self._sel_m_x = 0
        self._sel_m_y = 0
        self._menu_focus = False
        self.sel_target = SelectionTarget(data_path)

        level_options = GuiLevelOptions(False)
        quit_lvl_gui = GuiQuitLevel(False)
        obj_search_gui = GuiObjSearch(False)
        edit_obj_gui = GuiEditObj(True)

        self.gui_manager.add(QUIT_GAME, quit_lvl_gui)
        self.gui_manager.add(OBJECT_SEARCH, obj_search_gui)
        self.gui_manager.add(LEVEL_OPTIONS, level_options)
        self.gui_manager.add(EDIT_OBJ, edit_obj_gui)
        self.del_bind = pygame.K_d
        self.edit_bind = pygame.K_e
        self.options_bind = pygame.K_F1
        self.spawn_bind = pygame.K_SPACE
        #1 = left mouse button
        self.sel_bind = 1

    def mouse_input(self, mouse_event):
        if mouse_event.type == pygame.MOUSEBUTTONUP:
            #If there is a blocking menu, returns true
            if not self.gui_manager.input(mouse_event.type):
                print('no blocking menu found')
                if mouse_event.button == self.sel_bind:
                    if self.selected_obj:
                        self.place_object()
                    else:
                        self.select_object_at(mouse_event.pos)

    def key_input(self, user_input):
        if not self.gui_manager.input(user_input):
            if user_input == self.del_bind:
                self.remove_object(self.selected_obj)
                #clear selected_obj
                self.place_object()
            elif user_input == self.edit_bind:
                self.edit_obj_menu(self.selected_obj)
            elif user_input == self.options_bind:
                self.gui_manager.toggle_state(LEVEL_OPTIONS, self)
            elif user_input == self.spawn_bind:
                self.gui_manager.toggle_state(OBJECT_SEARCH, self)

    def draw(self, screen):
        Level.draw(self, screen)
        if self.selected_obj:
            translated = self.camera.translate_to(self.selected_obj.rect)
            self.sel_target.draw(screen, translated)

    def edit_obj_menu(self, obj):
        if obj:
            self.gui_manager.toggle_state(EDIT_OBJ, self, self.selected_obj)

    def focus_menu(self, b_focus):
        #pygame.mouse.set_visible(not b_focus)
        self._menu_focus = b_focus

    def update(self):
        self.gui_manager.update()
        if not self.gui_manager.active_blocking:
            #update object positions
            for obj in self.objects:
                obj.update()
                if obj.obey_gravity:
                    obj.do_gravity(self.gravity)

            self.check_collisions()
            self.camera.update(pygame.mouse.get_pos())
            m_x, m_y = pygame.mouse.get_pos()
            self.update_pre_place_pos(m_x, m_y)

    def save(self, filedict):
        self._filename = filedict['filename']
        config = configparser.ConfigParser()
        sfile = open(os.path.join(self._data_dir, 'level_data', self._filename), "w")
        for obj in self.objects:
            #If object with this name has already been added, skip it
            if obj.name in config.sections():
                print(obj.name + " already exists")
                continue
            obj.serialize(config)
        config.write(sfile)
        print("Saved Level.")

    def clear(self):
        Level.clear(self)
        self.selected_obj = None

    def remove_object(self, obj):
        if obj in self.objects:
            self.objects.remove(obj)

    def pre_place_object(self, filename):
        self.objects.add(ObjFactory('levelobject', {'name': 'pre_place',
                                                    'type': 'LevelObject',
                                                    'file1': filename,
                                                    'x': pygame.mouse.get_pos()[X],
                                                    'y': pygame.mouse.get_pos()[Y],
                                                    'w': 0,
                                                    'h': 0,
                                                    '_layer': 15,
                                                    'collidable': 'True',
                                                    'trans': 'True',
                                                    'obey_gravity': 'False'}))
        self.select_object(next((x for x in self.objects if x.name == 'pre_place'), None))

    def update_pre_place_pos(self, x, y):
        if self.selected_obj:
            cords = (x + self._sel_m_x,  y + self._sel_m_y)
            self.selected_obj.rect.x, self.selected_obj.rect.y = self.camera.translate_cords_to(cords)

    def place_object(self):
        print('placing object')
        if self.selected_obj:
            #Executed only if no name is set
            if self.selected_obj.name is None or self.selected_obj.name == 'pre_place':
                x = 1
                while True:
                    name = "LevelObject" + str(len(self.objects) + x)
                    exisit = next((obj for obj in self.objects if obj.name == name), None)
                    if exisit is None:
                        self.selected_obj.name = name
                        print('Placed: ' + name)
                        break
                    else:
                        print(exisit.name + ' exists')
                    x += 1
            self.selected_obj = None
        else:
            print("Trying to place an object, but none is selected")

    def move_sel_obj(self, direction):
        if self.selected_obj:
            if direction == DIR_UP:
                self.selected_obj.rect.y -= 15
            elif direction == DIR_RIGHT:
                self.selected_obj.rect.x += 15
            elif direction == DIR_DOWN:
                self.selected_obj.rect.y += 15
            elif direction == DIR_LEFT:
                self.selected_obj.rect.x -= 15

    def select_object_at(self, screen_cords):
        t_x, t_y = self.camera.translate_cords_to(screen_cords)
        objs = self.objects_at(t_x, t_y)
        if objs:
            #Find the mouse offset from the top left of object for offset when moving with mouse
            self._sel_m_x = objs[0].rect.x - t_x
            self._sel_m_y = objs[0].rect.y - t_y
            self.select_object(objs[0])

    def select_object(self, obj):
        if obj:
            self.selected_obj = obj
            self.sel_target.resize(self.selected_obj.rect)
        else:
            print('NoneType sent to select_object')

    def edit_object(self, var_dict):
        """Remove selected object and spawn an object using variables passed"""
        self.remove_object(self.selected_obj)
        self.selected_obj = None
        self.spawn_object(var_dict)