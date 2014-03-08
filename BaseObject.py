from Constants import *
from Timer import *
from Behavior import Behavior


class BaseObject(pygame.sprite.Sprite):
    _objects = []

    def __init__(self, var_dict):
        pygame.sprite.Sprite.__init__(self)
        self._layer = 0
        self.behaviors = []
        self._use_timer = None
        self._can_use = True
        self.type = BASE_OBJECT
        self.visible = False
        self.name = var_dict.get('name', None)
        self.obey_gravity = False
        self.collidable = False
        self.xvel = 0
        self.yvel = 0
        self.maxXvel = .5
        self.maxYvel = .5
        self.move_dir = DIR_LEFT
        x = var_dict.get('x', 'no')
        y = var_dict.get('y', 'no')
        w = var_dict.get('w', 'no')
        h = var_dict.get('h', 'no')
        #Not None because 0 = False
        if x != 'no' and y != 'no' and w != 'no' and h != 'no':
            self.rect = pygame.Rect(x, y, w, h)
        else:
            print(self.name + " is missing a value")
            self.rect = pygame.Rect(0, 0, 0, 0)

        #Create a new dict based on filtered results for var_dict (keys containing 'behavior')
        str_behaviors = {x: i for x, i in var_dict.items() if x.find('behavior') > -1}
        #Adds the value for each dict item to behavior list for the object (Does not guarantee the behavior exists)
        self.set_behaviors(str_behaviors.values())
        print(self.name + " behaviors: " + str(len(self.behaviors)))

        BaseObject._objects.append(self)

    @staticmethod
    def object_by_name(obj_name):
        obj = next((x for x in BaseObject._objects if x.name == obj_name), None)
        return obj

    def interact(self, player, level):
        if not self._use_timer:
            self._use_timer = Timer(self.use_timer_len, self._set_can_use)
        if self._can_use:
            #iteracte through behaviors of object, if a behavior meets conditions, do behavior and start delay use timer
            for behavior in self.behaviors:
                if behavior.behave(player, self, level):
                    self._can_use = False
                    self._use_timer.start_timer()
                    break

    def _set_can_use(self):
        print('Setting can_use = True.')
        self._can_use = True

    def set_behaviors(self, behaviors):
        for behavior in behaviors:
            if behavior.lower() == 'pickup':
                self.behaviors.append(Behavior(_check_plyr_pickup, do_plyr_pickup))
            elif behavior.lower() == 'place':
                self.behaviors.append(Behavior(_check_plyr_place, do_plyr_place))
            elif behavior.lower() == 'toggle_power':
                self.behaviors.append(Behavior(_check_power_crane, do_power_crane))

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


##PLAYER PICKUP CONDITIONS##
def _check_plyr_pickup(player, obj):
    if player.held_item is None:
        print("Can Pickup")
        return True
    else:
        return False


##PLAYER PICKUP ACTION##
def do_plyr_pickup(player, obj, level):
        print("Pickup behaving")
        player.pickup(obj)


##PLAYER PLACE CONDITIONS##
def _check_plyr_place(player, obj):
    if player.held_item is not None:
        print("Can Place")
        return True
    else:
        return False


##PLAYER PLACE ACTION##
def do_plyr_place(player, obj, level):
    print("Place behaving")
    player.drop(level)


##CRANE TOGGLE POWER CONDITIONS##
def _check_power_crane(player, powerbox):
    return True


##CRANE TOGGLE POWER ACTION##
def do_power_crane(player, powerbox, level):
    cranes = [crane for crane in level.objects if crane.type == CRANE_OBJECT]
    if len(cranes) > 0:
        if len(cranes) > 1:
            print("Multiple cranes found. Powering first added.")
        cranes[0].toggle_power()
    else:
        print('No crane found.')



##OBJECT STATE CHANGE CONDITIONS##
#def _check_state_change(player, object):
    #return True


#def do_state_change(player, object, level):