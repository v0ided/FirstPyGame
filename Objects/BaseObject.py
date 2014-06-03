from HelpFunctions import *


class BaseObject(pygame.sprite.Sprite):
    _objects = []

    def __init__(self, var_dict):
        pygame.sprite.Sprite.__init__(self)
        self._layer = 0
        self.behaviors = []
        self._use_timer = None
        self.use_timer_len = 800
        self._can_use = True
        self.type = BASE_OBJECT
        self.visible = False
        self.name = var_dict.get('name', "")
        self.obey_gravity = False
        self.collidable = False
        self.xvel = 0
        self.yvel = 0
        self.maxXvel = 8
        self.maxYvel = 8
        self.move_dir = DIR_LEFT
        self.x = var_dict.get('x', 'no')
        self.y = var_dict.get('y', 'no')
        self.w = var_dict.get('w', 'no')
        self.h = var_dict.get('h', 'no')
        #Not None because 0 = False
        if self.x != 'no' and self.y != 'no' and self.w != 'no' and self.h != 'no':
            self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        else:
            print(self.name + " is missing a value")
            self.rect = pygame.Rect(0, 0, 0, 0)

        #Create a list of string behaviors from filtered results in var_dict (keys containing 'behavior')
        str_behaviors = [var_dict[key] for key in var_dict.keys() if 'behavior' in key]
        #Create enum behavior list from recognized behaviors
        self.behaviors = [to_behavior(str_behavior) for str_behavior in str_behaviors if str_behavior != NOTHING]
        print(self.name + " behaviors: " + str(len(self.behaviors)))

        #self.type_vars = {'type': self.type, 'x': self.rect.x, 'y': self.rect.y, 'w': self.rect.w, 'h': self.rect.h,
                          #'gravity': self.obey_gravity, 'collide': self.collidable}

        BaseObject._objects.append(self)

    @staticmethod
    def object_by_name(obj_name):
        obj = next((x for x in BaseObject._objects if x.name == obj_name), None)
        return obj

    def interact(self, obj, behavior):
        return

    #Executed by object use timer upon completion
    def _set_can_use(self):
        self._can_use = True

    def draw(self, screen, rect_loc):
        print('Base object print called for ' + self.name)

    def collide(self, obj):
        pass

    def move(self):
        self._update_pos()

    def teleport_to(self, x, y, ALIGN=TOP_LEFT):
        if ALIGN == TOP_LEFT:
            self.rect.x = x
            self.rect.y = y
        elif ALIGN == CENTER:
            self.rect.center = (x, y)
        elif ALIGN == MID_TOP:
            self.rect.midtop = (x, y)
        elif ALIGN == TOP_RIGHT:
            self.rect.topright = (x, y)
        elif ALIGN == MID_RIGHT:
            self.rect.midright = (x, y)
        elif ALIGN == BOT_RIGHT:
            self.rect.bottomright = (x, y)
        elif ALIGN == MID_BOT:
            self.rect.midbottom = (x, y)
        elif ALIGN == BOT_LEFT:
            self.rect.bottomleft = (x, y)
        elif ALIGN == MID_LEFT:
            self.rect.midleft = (x, y)

    def _change_vel(self, move_dir, move_vel):
        if move_dir == DIR_RIGHT:
            if self.xvel + move_vel < self.maxXvel:
                self.xvel += move_vel
        elif move_dir == DIR_LEFT:
            if self.xvel - move_vel > 0 - self.maxXvel:
                self.xvel -= move_vel
        elif move_dir == DIR_UP:
            if self.yvel + move_vel > 0 - self.maxYvel:
                self.yvel -= move_vel
        elif move_dir == DIR_DOWN:
            if self.yvel + move_vel < self.maxYvel:
                self.yvel += move_vel

    def _update_pos(self):
        self.rect.x += self.xvel
        self.rect.y += self.yvel
        self.x = self.rect.x
        self.y = self.rect.y

    def serialize(self, config):
        try:
            config.add_section(self.name)
            member_vars = vars(self)
            for name, value in member_vars.items():
                config.set(self.name, name, to_string(name, value))
        except TypeError as exception:
            print(exception)
            raise