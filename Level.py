import configparser
import pygame
import os
from HelpFunctions import load_image, to_num
from Constants import PLAYER
from Camera import Camera
from LevelObjFactory import ObjFactory
from Gui.GuiManager import GuiManager


class Background(pygame.sprite.Sprite):
    def __init__(self, bg_filename):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(bg_filename, -1)
        self.surface.blit(self.image, (0, 0))


class Level():
    def __init__(self, w, h, filename, data_dir):
        self.width = w
        self.height = h
        self._data_dir = data_dir
        os.chdir(self._data_dir)

        self.background = pygame.Surface((self.width, self.height))
        self.background = self.background.convert()
        self.background.fill((153, 217, 234))
        self.objects = pygame.sprite.LayeredUpdates()
        self.gravity = .5
        self.camera = Camera(800, 600)
        self._filename = filename
        self._load_objects()
        self.player = self._get_player_from_objects()
        self.input_binds = []
        self.gui_manager = GuiManager()

    def get_filename(self):
        return self._filename

    def _get_player_from_objects(self):
        for obj in self.objects:
            if obj.type == PLAYER:
                return obj
        return None

    def get_obj(self, obj_name):
        for obj in self.objects:
            if obj_name == obj.name:
                return obj
        return None

    def _load_objects(self):
        obj_filename = os.path.join('level_data', self._filename)
        parser = configparser.ConfigParser()
        if obj_filename not in parser.read(obj_filename):
            print(obj_filename + 'not found/cant be read')

        object_list = parser.sections()
        for objname in object_list:
            obj_type = parser[objname]['type']
            var_dict = {'name': objname}
            for option in parser[objname]:
                value = parser[objname][option]
                var_dict[option] = to_num(value)
            self.objects.add(ObjFactory(obj_type, var_dict))

    def clear(self):
        while self.objects:
            cur_layer = self.objects.get_top_layer()
            self.objects.remove_sprites_of_layer(cur_layer)
        self.background.fill((153, 217, 234))

    def load(self, new_file=None):
        if new_file:
            self._filename = new_file
        self.clear()
        self._load_objects()
        self.player = self._get_player_from_objects()

    def update(self):
        #update object positions
        for obj in self.objects:
            obj.update()
            if obj.obey_gravity:
                obj.do_gravity(self.gravity)

        self.check_collisions()
        self.camera.update(self.player)

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        for sprite_layer in self.objects.layers():
            for sprite in self.objects.get_sprites_from_layer(sprite_layer):
                if self.camera.on_screen(sprite.rect) and sprite.visible:
                    translated = self.camera.translate_to(sprite.rect)
                    sprite.draw(screen, translated)

    #calls collide for each object against each object besides itself
    #objects' collide function carries out what it means to collide and how to respond
    def check_collisions(self):
        for a_obj in self.objects:
            for b_obj in self.objects:
                if a_obj == b_obj:
                    continue
                a_obj.collide(b_obj)

    def objects_at(self, x, y):
        col_objs = [obj for obj in self.objects if obj.rect.collidepoint(x, y)]
        if col_objs:
            return col_objs
        else:
            return None