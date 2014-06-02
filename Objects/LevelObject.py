import pyganim
from Objects.BaseObject import *
from HelpFunctions import to_bool


class LevelObject(BaseObject):
    def __init__(self, var_dict):
        BaseObject.__init__(self, var_dict)
        self.type = LEVEL_OBJECT
        self.files = []

        if 'file2' in var_dict.keys():
            self.files.append(var_dict['file2'])
            self.idle_anim = pyganim.PygAnimation([(os.path.join(var_dict['file1']), .75),
                                                   (os.path.join(var_dict['file2']), .75)])
            self.idle_anim.set_colorkey((255, 255, 255))
        elif 'file1' in var_dict.keys():
            self.files.append(var_dict['file1'])
            self.idle_anim = pyganim.PygAnimation([(os.path.join(var_dict['file1']), 1)])
            self.idle_anim.set_colorkey((255, 255, 255))

        #If width or height is 0, use default w/h
        if var_dict['w'] == 0 or var_dict['h'] == 0:
            self.rect.w = self.idle_anim.getRect().w
            self.rect.h = self.idle_anim.getRect().h
        else:
            self.idle_anim.scale((var_dict['w'], var_dict['h']))
        self.rect.x = var_dict['x']
        self.rect.y = var_dict['y']
        self.col_objects = []
        self.on_object = None
        self._layer = var_dict['_layer']
        self.layer = self._layer
        self.collidable = to_bool(var_dict['collidable'])
        self.idle_anim.play()
        self.obey_gravity = to_bool(var_dict['obey_gravity'])
        self.visible = True

    def draw(self, screen, translated):
        self.idle_anim.blit(screen, translated)

    def update(self):
        self.move()

    def do_gravity(self, gravity):
        self._change_vel(DIR_DOWN, gravity)

    def collide(self, obj):
        if self.rect.colliderect(obj.rect):
            if obj.collidable:
                self.col_objects.append(obj)
                if obj.type == PLAYER:
                    return
                if obj.rect.collidepoint(self.rect.midbottom):
                    self.yvel = 0
                    #save the object the object is on
                    self.on_object = obj.rect
        elif obj in self.col_objects:
            self.col_objects.remove(obj)

    def config_files(self, config, counter):
        config.set(self.name, 'file' + str(counter), self.files[counter])
        if counter >= len(self.files):
            counter += 1
            self.config_files(config, counter)

    def provide_type_vars(self):
        BaseObject.provide_type_vars(self)
        yield ('type', obj_type_str(self.type))
        yield ('layer', str(self._layer))
        yield ('trans', "True")  # Transparency
        for file, i in enumerate(self.files):
            yield ('file' + str(i), self.files[i])

    def serialize(self, config):
        BaseObject.serialize(self, config)