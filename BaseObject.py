from Constants import *
from Timer import *
from Behavior import Behavior


class BaseObject(pygame.sprite.Sprite):
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
        x = var_dict.get('x', 'no')
        y = var_dict.get('y', 'no')
        w = var_dict.get('w', 'no')
        h = var_dict.get('h', 'no')
        if x != 'no' and y != 'no' and w != 'no' and h != 'no':
            self.rect = pygame.Rect(x, y, w, h)
        else:
            print(self.name + " is missing a value")
            self.rect = pygame.Rect(0, 0, 0, 0)

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
            if behavior == 'pickup':
                self.behaviors.append(Behavior(_check_plyr_pickup, do_plyr_pickup))
            elif behavior == 'place':
                self.behaviors.append(Behavior(_check_plyr_place, do_plyr_place))
            elif behavior == 'toggle_power':
                self.behaviors.append(Behavior(_check_power_crane, do_power_crane))

    def draw(self, screen, rect_loc):
        print('Base object print called for ' + self.name)

    def collide(self, obj):
        pass


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


def do_power_crane(player, powerbox, level):
    level.get_group(powerbox.group).toggle_power()
    print('Powering Crane')


##OBJECT STATE CHANGE CONDITIONS##
def _check_state_change(player, object):
    return True


#def do_state_change(player, object, level):