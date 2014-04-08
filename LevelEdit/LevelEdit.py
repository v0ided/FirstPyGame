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

    def edit_object(self, obj):
        print("Edit Object..")

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
            self.selected_obj.rect.x, self.selected_obj.rect.y = self.camera.translate_cords_to(x, y)

    def place_object(self):
        if self.selected_obj:
            if self.selected_obj.name is None:
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
                    self.selected_obj = objs[0]
                    print(self.selected_obj.name)
            else:
                print('Placing object..')
                self.place_object()