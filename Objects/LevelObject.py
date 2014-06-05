import pyganim
from Objects.BaseObject import *
from HelpFunctions import to_bool
from Animation import Animation


class LevelObject(BaseObject):
    def __init__(self, var_dict):
        BaseObject.__init__(self, var_dict)
        self.type = LEVEL_OBJECT
        self.files = var_dict['files'].split(',')
        self.times = var_dict['times'].split(',')

        #HACK - ANIMATION WILL CHANGE THIS
        #If files is larger than 1, create animation with 2 frames
        # if len(self.files) > 1 and self.files[1] != '':
        #     self.idle_anim = pyganim.PygAnimation([(os.path.join(self.files[0]), .75),
        #                                            (os.path.join(self.files[1]), .75)])
        #     self.idle_anim.set_colorkey((255, 255, 255))
        # #Else if files has 1 file, create animation with 1 frame
        # elif len(self.files) > 0:
        #     self.idle_anim = pyganim.PygAnimation([(os.path.join(self.files[0]), 1)])
        #     self.idle_anim.set_colorkey((255, 255, 255))

        self.idle_anim = Animation(self.files, self.times)

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

    def serialize(self, config):
        BaseObject.serialize(self, config)