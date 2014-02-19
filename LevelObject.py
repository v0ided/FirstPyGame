import os
import pyganim
from BaseObject import *
from HelpFunctions import to_bool


class LevelObject(BaseObject):
    def __init__(self, var_dict):
        BaseObject.__init__(self, var_dict)
        self.type = LEVEL_OBJECT

        if 'file2' in var_dict.keys():
            self.idle_anim = pyganim.PygAnimation([(os.path.join('data', var_dict['file1']), .75),
                                                   (os.path.join('data', var_dict['file2']), .75)])
        elif 'file1' in var_dict.keys():
            self.idle_anim = pyganim.PygAnimation([(os.path.join('data', var_dict['file1']), 1)])

        if var_dict['trans'] == 'yes':
            self.idle_anim.set_colorkey((255, 255, 255))

        self.idle_anim.scale((var_dict['w'], var_dict['h']))
        self.rect.x = var_dict['x']
        self.rect.y = var_dict['y']
        self.yvel = 0
        self.col_object = None
        self.on_object = None
        self._layer = var_dict['layer']
        self.collidable = to_bool(var_dict['collide'])
        self.idle_anim.play()
        self.use_timer_len = 800
        self.obey_gravity = to_bool(var_dict['gravity'])
        self.visible = True

        #Load Behaviors from dictionary
        current_b = 1
        b_id = 'behavior' + str(current_b)
        str_behaviors = []
        while b_id in var_dict:
            str_behaviors.append(var_dict[b_id])
            current_b += 1
            b_id = 'behavior' + str(current_b)
        self.set_behaviors(str_behaviors)

    def draw(self, screen, translated):
        self.idle_anim.blit(screen, translated)

    #def update(self):

    def do_gravity(self, gravity):
        if self.obey_gravity:
            self.yvel += gravity
            self.rect.y += self.yvel

    def collide(self, obj):
        if self.rect.colliderect(obj.rect):
            if obj.collidable:
                #save the last collided object
                self.col_object = obj
                if obj.type == PLAYER:
                    return
                if obj.rect.collidepoint(self.rect.midbottom):
                    self.yvel = 0
                    #save the object the object is on
                    self.on_object = obj.rect