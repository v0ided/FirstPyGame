import configparser
from Level import Level
from LevelObjFactory import ObjFactory
from EditCamera import EditCamera
from HelpFunctions import *


#New levels created/saved levels loaded by creating a new LevelEdit instance
class LevelEdit(Level):
    def __init__(self, w, h, filename=None):
        #If a blank filename is passed, create a new level file 'new_level_1.ini, if the file exists in working dir,
        #increment i until a filename that does not exist in working dir is found
        if os.path.isfile(os.path.join('../', 'data', 'level_data', filename)):
            print("Existing level found, loading..")
        else:
            if filename is None:
                i = 0
                while True:
                    i += 1
                    filename = os.path.join('../', 'data', 'level_data', 'new_level_' + str(i) + '.ini')
                    if os.path.isfile(filename):
                        break

        Level.__init__(self, w, h, filename, os.path.join('../', 'data'))
        self.selected_obj = None
        self.camera = EditCamera(800, 600)

    def update(self):
        #update object positions
        for obj in self.objects:
            obj.update()
            if obj.obey_gravity:
                obj.do_gravity(self.gravity)

        self.check_collisions()
        self.camera.update(pygame.mouse.get_pos())

    def clear_level(self):
        del self.objects[:]
        self.background.fill((153, 217, 234))

    def save_level(self):
        config = configparser.ConfigParser()
        for obj in self.objects:
            #If object with this name has already been added, skip it
            if obj.name in config.sections():
                continue
            obj.seralize(config)
            sfile = open(self.filename, "w")
            config.write(sfile)
            print("Saved Level.")

    def load_level(self):
        print('Loading level..')

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

    def update_pre_place_pos(self, m_x, m_y):
        if self.selected_obj:
            mouse_rect = pygame.Rect(m_x, m_y, 1, 1)
            trans_mouse_rect = self.camera.translate_from(mouse_rect)
            self.selected_obj.rect.x = trans_mouse_rect.x
            self.selected_obj.rect.y = trans_mouse_rect.y

    def place_object(self):
        if self.selected_obj:
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