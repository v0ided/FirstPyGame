from GroupObject import *


#todo: Change graphic/name for magnet to claw :)
class CraneObject(GroupObject):
    def __init__(self, var_dict):
        GroupObject.__init__(self, var_dict)

        self.type = CRANE_OBJECT

        #list of tuples representing coordinates and wait time ie dest[0] = (x,y,wait)
        #Contains coordinates for each destination
        self.dests = []
        self.cur_dest = 0
        #Arm and Magnet objects have to be declared before the crane object or they will be set to None
        self.arm = next((x for x in BaseObject._objects if x.name == var_dict['arm']), None)
        self.magnet = next((i for i in BaseObject._objects if i.name == var_dict['magnet']), None)

        if not self.arm or not self.magnet:
            print("Couldn't find arm or magnet for crane.")

        #These x and y values represent the crane's posistion when telling it to move somewhere (ie the arm/claw)
        self.x = self.magnet.rect.x
        self.y = self.magnet.rect.y + self.magnet.rect.h

        self.moving = False

        #These variables' values will be set in __setup_vars(var_dict)
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
        self.add_dest(800, 450, 5000)
        self.add_dest(100, 450, 5000)
        self._waiting = False
        self._power = False
        self.state = OFF

    def _next_dest(self):
        print('Moving to destination: ' + str(self.cur_dest))
        if self.cur_dest + 1 >= len(self.dests):
            self.cur_dest = 0
        else:
            self.cur_dest += 1
        self._waiting = False

    def __get_next_dest_id(self):
        if self.cur_dest + 1 >= len(self.dests):
            return 0
        else:
            return self.cur_dest + 1

    #def _pickup(self):

    def _move(self):
        if self._power and self.arm and self.magnet:
            if self.dests[self.cur_dest][X] > self.x:
                self.arm.rect.x += self.xspeed
                self.magnet.rect.x += self.xspeed
                self.x += self.xspeed
            elif self.dests[self.cur_dest][X] < self.x:
                self.arm.rect.x -= self.xspeed
                self.magnet.rect.x -= self.xspeed
                self.x -= self.xspeed
            elif self.dests[self.cur_dest][Y] > self.y:
                self.magnet.rect.y += self.yspeed
                self.arm.idle_anim.scale((self.arm.rect.w, self.arm.rect.h + self.yspeed))
                self.arm.rect.y += self.yspeed
                self.y += self.yspeed
            elif self.dests[self.cur_dest][Y] < self.y:
                self.magnet.rect.y -= self.yspeed
                self.arm.idle_anim.scale((self.arm.rect.w, self.arm.rect.h - self.yspeed))
                self.arm.rect.y -= self.yspeed
                self.y -= self.yspeed
            else:
                if not self._waiting:
                    self.dests[self.__get_next_dest_id()][WAIT].start_timer()
                    self._waiting = True

    def update(self):
        self._move()

    def add_dest(self, x, y, wait):
        width = self.xmax - self.xmin
        height = self.ymax - self.ymin
        bounds = pygame.Rect(self.xmin, self.ymin, width, height)
        if bounds.collidepoint(x, y):
            wait_t = Timer(wait, self._next_dest)
            self.dests.append((x, y, wait_t))
        else:
            print('Invalid Coordinates found: ' + str(x) + "," + str(y))

    def go_home(self):
        self.cur_dest = 0

    def toggle_power(self):
        print(self.name + " toggling power.")
        if self._power:
            self._power = False
        else:
            self._power = True