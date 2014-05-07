from BaseObject import BaseObject
from LevelObject import LevelObject
from Constants import *
import pygame
from Timer import Timer


class CraneObject(LevelObject):
    def __init__(self, var_dict):
        LevelObject.__init__(self, var_dict)

        self.type = CRANE_OBJECT

        #list of tuples representing coordinates and wait time ie dest[0] = (x,y,wait)
        #Contains coordinates and wait time for each destination
        self.dests = []
        self.cur_dest = 0
        #Arm has to be declared before the crane object or they will be set to None
        self.arm = next((x for x in BaseObject._objects if x.name == var_dict['arm']), None)

        if not self.arm:
            print("Couldn't find arm or magnet for crane.")

        self.moving = False

        #These variables' values will be set in self.__setup_vars(var_dict)
        self.name = var_dict['name']
        self.xmin = var_dict['xmin']
        self.xmax = var_dict['xmax']
        self.ymin = var_dict['ymin']
        self.ymax = var_dict['ymax']
        self.xhome = var_dict['xhome']
        self.yhome = var_dict['yhome']
        self.xspeed = var_dict['xspeed']
        self.yspeed = var_dict['yspeed']

        #Create home destination
        self.add_dest(self.xhome, self.yhome, 500)
        self.add_dest(820, 250, 5000, PICKUP)
        self.add_dest(100, 250, 5000, PLACE)
        self._waiting = False
        self._power = False
        self.state = OFF

        #These x and y values represent the crane's position when telling it to move somewhere (ie the arm/claw)
        self.x = self.arm.rect.right
        self.y = self.arm.rect.bottom

        #Objects that are possible to pick up and held objects
        self.pos_pickup = []
        self.held_objects = []

        #Area of the crane that objects can be picked up from
        pickup_w = 60
        pickup_h = 30
        pickup_x = self.x - pickup_w
        pickup_y = self.y - pickup_h
        self.pickup_area = pygame.Rect(pickup_x, pickup_y, pickup_w, pickup_h)

    #Called when the crane is done waiting at dest and is about to move to the next
    def _next_dest(self):
        print('Moving to destination: ' + str(self.cur_dest))
        if self.cur_dest + 1 >= len(self.dests):
            self.cur_dest = 0
        else:
            self.cur_dest += 1
        self._waiting = False

    #Called when first arriving at a dest
    def __get_next_dest_id(self):
        if self.cur_dest + 1 >= len(self.dests):
            return 0
        else:
            return self.cur_dest + 1

    def _pickup(self):
        for obj in self.pos_pickup:
            if obj not in self.held_objects:
                self.held_objects.append(obj)
                obj.obey_gravity = False
                #todo: Organize multiple objects in the pickup space, check if still room in pickup_area
                obj.rect.x = self.pickup_area.x
                obj.rect.y = self.pickup_area.y
                print(obj.name + ' - pickup action called')

    def _drop(self):
        for obj in self.held_objects:
            obj.obey_gravity = True
        del self.held_objects[:]

    def collide(self, obj):
        if self.pickup_area.colliderect(obj.rect):
            #if obj._layer == self._layer:
                #if not self.pickup_area.colliderect(obj.rect):
                    #self._power = False
            #if self.pickup_area.colliderect(obj.rect):
                if obj not in self.pos_pickup:
                    if obj != self.arm:
                        print(obj.name + ' added to possible pickups.')
                        self.pos_pickup.append(obj)
        else:
            if obj in self.pos_pickup:
                    self.pos_pickup.remove(obj)

    def _move(self):
        if self._power and self.arm:
            #if destx to the right of x
            if self.dests[self.cur_dest][X] > self.x:
                self._change_vel(DIR_RIGHT, self.xspeed)
            #if destx is to the left of x
            elif self.dests[self.cur_dest][X] < self.x:
                self._change_vel(DIR_LEFT, self.xspeed)
            #if desty below y
            elif self.dests[self.cur_dest][Y] > self.y:
                self._change_vel(DIR_DOWN, self.yspeed)
            #if desty above y
            elif self.dests[self.cur_dest][Y] < self.y:
                self._change_vel(DIR_UP, self.yspeed)
            else:
                if not self._waiting:
                    self.xvel = 0
                    self.yvel = 0
                    self.dests[self.__get_next_dest_id()][WAIT].start_timer()
                    self._waiting = True
                    self.__do_dest_action()
        self._update_pos()

    def _update_pos(self):
        self.x += self.xvel
        self.y += self.yvel
        self.pickup_area.x += self.xvel
        self.pickup_area.y += self.yvel
        self.arm.rect.x += self.xvel
        self.arm.rect.y += self.yvel
        for held_obj in self.held_objects:
            held_obj.rect.x += self.xvel
            held_obj.rect.y += self.yvel

    #Does the current dest action, may be NONE, actions are integer variables declared at top of source
    def __do_dest_action(self):
        action = self.dests[self.cur_dest][ACTION]
        if action == PICKUP:
            self._pickup()
        elif action == PLACE:
            self._drop()

    def update(self):
        self._move()

    def add_dest(self, x, y, wait, action=NOTHING):
        width = self.xmax - self.xmin
        height = self.ymax - self.ymin
        bounds = pygame.Rect(self.xmin, self.ymin, width, height)
        if bounds.collidepoint(x, y):
            wait_t = Timer(wait, self._next_dest)
            self.dests.append((x, y, wait_t, action))
        else:
            print('Invalid coordinates found: ' + str(x) + "," + str(y))

    def go_home(self):
        self.cur_dest = 0

    def toggle_power(self):
        print(self.name + " toggling power.")
        if self._power:
            self._power = False
        else:
            self._power = True

    def serialize(self, config):
        #Seralize referenced arm object first
        self.arm.serialize(config)
        BaseObject.serialize(self, config)
        config.set(self.name, 'xmin', str(self.xmin))
        config.set(self.name, 'ymin', str(self.ymin))
        config.set(self.name, 'xmax', str(self.xmax))
        config.set(self.name, 'ymax', str(self.ymax))
        config.set(self.name, 'xhome', str(self.xhome))
        config.set(self.name, 'yhome', str(self.yhome))
        config.set(self.name, 'xspeed', str(self.xspeed))
        config.set(self.name, 'yspeed', str(self.yspeed))
        config.set(self.name, 'arm', self.arm.name)