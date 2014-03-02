from GroupObject import *


#Names for indicies inside tuple stored in dest list
X = 0
Y = 1
WAIT = 2


#todo: Change graphic for arm parts/claw to one, animate for set path (Stop trying to be too dynamic!)
class CraneObject(GroupObject):
    def __init__(self, var_dict):
        GroupObject.__init__(self, var_dict)

        self.type = CRANE_OBJECT

        #list of tuples representing coordinates and wait time ie dest[0] = (x,y,wait)
        #Contains coordinates and wait time for each destination
        self.dests = []
        self.cur_dest = 0
        #Arm and Magnet objects have to be declared before the crane object or they will be set to None
        self.arm = next((x for x in BaseObject._objects if x.name == var_dict['arm']), None)

        if not self.arm:
            print("Couldn't find arm or magnet for crane.")

        #These x and y values represent the crane's posistion when telling it to move somewhere (ie the arm/claw)
        self.x = self.arm.rect.right
        self.y = self.arm.rect.bottom

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
        if self._power and self.arm:
            #if destx to the right of x
            if self.dests[self.cur_dest][X] > self.x:
                self.arm.rect.x += self.xspeed
                self.x += self.xspeed
            #if destx is to the left of x
            elif self.dests[self.cur_dest][X] < self.x:
                self.arm.rect.x -= self.xspeed
                self.x -= self.xspeed
            #if desty below y
            elif self.dests[self.cur_dest][Y] > self.y:
                self.arm.rect.y += self.yspeed
                self.y += self.yspeed
            #if desty above y
            elif self.dests[self.cur_dest][Y] < self.y:
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