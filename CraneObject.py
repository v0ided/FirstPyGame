from GroupObject import *


#todo: Convert string to object for arm and magnet
class CraneObject(GroupObject):
    def __init__(self, var_dict):
        GroupObject.__init__(self, var_dict)

        self.type = CRANE_OBJECT
        #These x and y values are for movement of the moving crane arm/magnet, not the actual object itself
        self.x = 0
        self.y = 0

        #list of tuples representing coordinates and wait time ie dest[0] = (x,y,wait)
        #Contains coordinates for each destination
        self.dests = []
        self.cur_dest = 0
        self.arm = var_dict['arm']
        self.magnet = var_dict['magnet']
        self.moving = False

        #These variables' values will be set in __setup_vars(var_dict)
        self.name = 'GroupObject'
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

    #Called by add(obj) for every object added
    def _configure(self, obj):
        if obj.job == 'Arm':
            self.arm = obj
        elif obj.job == 'Magnet':
            self.magnet = obj
            #Use lower left corner of magnet in start pos as crane home posistion
            self.xhome = self.magnet.rect.x
            self.yhome = self.magnet.rect.y + self.magnet.rect.h
            self.x = self.magnet.rect.x
            self.y = self.magnet.rect.y + self.magnet.rect.h

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

    def groupBehave(self):
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
        if self._power:
            self._power = False
        else:
            self._power = True