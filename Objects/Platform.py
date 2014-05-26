__author__ = 'thvoidedline'

import os
import pyganim
from Objects.LevelObject import LevelObject
from Constants import PLATFORM, TOGGLE_POWER
from HelpFunctions import obj_type_str

READY = 1
BAD_ITEM = 2
FINISHED = 3


class Platform(LevelObject):
    def __init__(self, var_dict):
        LevelObject.__init__(self, var_dict)

        self.type = PLATFORM
        self.recipe_list = var_dict['recipe']
        self.state = READY
        self.good_file = var_dict['good']
        self.bad_file = var_dict['bad']
        self.bad_anim = pyganim.PygAnimation([(os.path.join(self.bad_file), 1)])
        self.good_anim = pyganim.PygAnimation([(os.path.join(self.good_file), 1)])

    def collide(self, obj):
        LevelObject.collide(self, obj)

    def draw(self, screen, translated):
        if self.state == READY:
            self.idle_anim.play()
            self.idle_anim.blit(screen, translated)
        elif self.state == BAD_ITEM:
            self.bad_anim.play()
            self.bad_anim.blit(screen, translated)
        elif self.state == FINISHED:
            self.good_anim.play()
            self.good_anim.blit(screen, translated)

    def interact(self, obj, behavior):
        print('interacting with ' + self.recipe_list)
        if behavior == TOGGLE_POWER:
            for item in self.recipe_list:
                is_missing = True
                for obj in self.col_objects:
                    if obj_type_str(obj.type) == item:
                        is_missing = False
                        break
                if is_missing is True:
                    self.state = READY
                    return
            self.state = FINISHED

    def serialize(self, config):
        LevelObject.serialize(self, config)
        config.set(self.name, 'recipe', self.recipe_list)
        config.set(self.name, 'good', self.good_file)
        config.set(self.name, 'bad', self.bad_file)