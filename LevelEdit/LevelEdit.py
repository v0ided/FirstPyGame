import configparser
import string
from EditCamera import EditCamera
from Level import Level
from LevelObjFactory import ObjFactory
from HelpFunctions import *


#New levels created/saved levels loaded by creating a new LevelEdit instance
class LevelEdit(Level):
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

    def focus_menu(self, b_focus):
        #pygame.mouse.set_visible(not b_focus)
        self._menu_focus = b_focus

    def update(self):
        #update object positions
        for obj in self.objects:
            obj.update()
            if obj.obey_gravity:
                obj.do_gravity(self.gravity)

        self.check_collisions()
        self.camera.update(pygame.mouse.get_pos())
        m_x, m_y = pygame.mouse.get_pos()
        self.update_pre_place_pos(m_x, m_y)

    def clear_level(self):
        while self.objects:
            cur_layer = self.objects.get_top_layer()
            self.objects.remove_sprites_of_layer(cur_layer)
        self.selected_obj = None
        self.background.fill((153, 217, 234))

    def save_level(self, filename=""):
        #If no filename is given, default to current filename (save)
        #If a filename is given, set the current filename to the new filename (save as)
        if filename == "":
            filename = self._filename
        else:
            self._filename = filename
        config = configparser.ConfigParser()
        sfile = open(os.path.join(self._data_dir, 'level_data', filename), "w")
        for obj in self.objects:
            #If object with this name has already been added, skip it
            if obj.name in config.sections():
                continue
            obj.seralize(config)
        config.write(sfile)
        print("Saved Level.")

    def load_level(self, new_file):
        self.clear_level()
        self._filename = new_file
        self._load_objects()

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
                                                    'layer': 15,
                                                    'collide': 'False',
                                                    'trans': 'True',
                                                    'gravity': 'False'}))
        self.selected_obj = next((x for x in self.objects if x.name == 'pre_place'), None)

    def update_pre_place_pos(self, x, y):
        if self.selected_obj:
            if not self._menu_focus:
                self.selected_obj.rect.x, self.selected_obj.rect.y = self.camera.translate_cords_to(x + self._sel_m_x, y + self._sel_m_y)

    def place_object(self):
        if self.selected_obj:
            if self.selected_obj.name is None or self.selected_obj.name == 'pre_place':
                self.selected_obj.name = "LevelObject" + str(len(self.objects))
            self.selected_obj = None

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

    def input(self, event_type):
        if event_type == pygame.MOUSEBUTTONUP:
            if self.selected_obj is None:
                m_x, m_y = pygame.mouse.get_pos()
                t_x, t_y = self.camera.translate_cords_to(m_x, m_y)
                objs = self.objects_at(t_x, t_y)

                #If > 0 objects were clicked on and there is no selected object already, select first object
                if objs:
                    self.select_object(objs[0])
                    print(self.selected_obj.name)
            else:
                print('Placing object..')
                self.place_object()

    #bounds checking? Error checking?
    def edit_object(self, var_list):
        """Set new variables for object, must obey order"""
        if len(var_list) > 7 and self.selected_obj:
            self.selected_obj.name = var_list[0]
            self.selected_obj.rect.x = to_num(var_list[1])
            self.selected_obj.rect.y = to_num(var_list[2])
            self.selected_obj.idle_anim.scale((to_num(var_list[3]), to_num(var_list[4])))
            self.selected_obj.obey_gravity = to_bool(var_list[5])
            self.selected_obj.collidable = to_bool(var_list[6])
            self.selected_obj._layer = to_num(var_list[7])
            #After editing, place object in level
            self.place_object()
            self._menu_focus = False
        else:
            print("Not enough variables passed to edit object or there is no object selected")

    def select_object(self, obj):
        if obj:
            self.selected_obj = obj
            m_x, m_y = pygame.mouse.get_pos()
            t_x, t_y = self.camera.translate_cords_to(m_x, m_y)
            self._sel_m_x = obj.rect.x - t_x
            self._sel_m_y = obj.rect.y - t_y
        else:
            print('NoneType sent to select_object')