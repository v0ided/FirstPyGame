import pyganim
import os
from BaseObject import *


class PlayerSprite(BaseObject):
    def __init__(self, var_dict):
        BaseObject.__init__(self, var_dict)
        self.type = PLAYER
        self.xvel = 0
        self.yvel = 0
        self.jumpvel = 0.75
        self.walkvel = 0.1
        self.maxXvel = 2.5
        self.maxYvel = 8
        self.direction = DIR_RIGHT
        self.iswalking = False
        self.on_object = None
        self.col_object = None
        self.jump_state = NOT_JUMPING
        self.airborne = True
        self.j_delay_timer = Timer(500, self.__next_jump_state, False)
        self.jump_timer = Timer(200, self.__next_jump_state, False)
        self._layer = 10
        #array of objects currently colliding with
        #used to track objects that are possible to interact with
        self.pos_interact = []
        self.has_item = False
        self.held_item = None
        self.drop_item = None
        self.collidable = True
        self.held_ofs_x = 0.0
        self.held_ofs_y = 0.0
        self.obey_gravity = True
        self.visible = True

        #Jumping Animation:
        self.jumping_anim = pyganim.PygAnimation([(os.path.join('PlayerJumping1.bmp'), 0.1),
                                                  (os.path.join('PlayerJumping2.bmp'), 0.1),
                                                  (os.path.join('PlayerJumping3.bmp'), 0.2),
                                                  (os.path.join('PlayerJumping4.bmp'), 0.4),
                                                  (os.path.join('PlayerJumping5.bmp'), 0.4),
                                                  (os.path.join('PlayerStanding.bmp'), 1)])
        self.jumping_anim.set_colorkey((255, 255, 255))

        #Walking Animation:
        self.walking_anim = pyganim.PygAnimation([(os.path.join('PlayerStanding.bmp'), 0.25),
                                                  (os.path.join('PlayerWalking1.bmp'), 0.25),
                                                  (os.path.join('PlayerWalking2.bmp'), 0.25),
                                                  (os.path.join('PlayerWalking3.bmp'), 0.25),
                                                  (os.path.join('PlayerWalking4.bmp'), 0.25),
                                                  (os.path.join('PlayerWalking5.bmp'), 0.25),
                                                  (os.path.join('PlayerWalking6.bmp'), 0.25)])
        self.walking_anim.set_colorkey((255, 255, 255))
        self.rect.x = var_dict['x']
        self.rect.y = var_dict['y']
        #self.rect = pygame.Rect(var_dict['x'], var_dict['y'], walk_wh[0], walk_wh[1])
        self.walking_anim.play()

    def draw(self, screen, rect_loc):
        if self.jump_state > 0:
            self.jumping_anim.play()
            self.walking_anim.stop()
            self.jumping_anim.blit(screen, rect_loc)
        elif self.iswalking is True:
            self.walking_anim.play()
            self.jumping_anim.stop()
            self.walking_anim.blit(screen, rect_loc)
        else:
            self.walking_anim.play()
            self.jumping_anim.stop()
            self.walking_anim.blitFrameNum(0, screen, rect_loc)

    def move(self):
        if self.iswalking is False:
            if self.xvel <= 0:
                self.xvel = 0
            else:
                self.xvel -= 1
        if self.direction == DIR_RIGHT and self.iswalking:
            if self.col_object is None:
                self._change_vel(DIR_RIGHT, self.walkvel)
            else:
                #check what side the object is on, permit walking the other way
                if self.col_object.rect.x < self.rect.x:
                    self._change_vel(DIR_RIGHT, self.walkvel)
        elif self.direction == DIR_LEFT and self.iswalking:
            if self.col_object is None:
                self._change_vel(DIR_LEFT, self.walkvel)
            else:
                if self.col_object.rect.x > self.rect.x:
                    self._change_vel(DIR_LEFT, self.walkvel)

        #Is the player colliding with ANY objects?
        if self.col_object is not None:
            #Check if still colliding with col_object
            if not self.rect.colliderect(self.col_object.rect):
                self.col_object = None

        #If player was on top of an object last tick
        if self.on_object is not None:
            #Check if player is still on object
            if self.on_object.rect.collidepoint(self.rect.midbottom):
                self.airborne = False
                #If player is on an object and yvel is being modified by do_jump(), stop the jump
                #if self._is_jumping():
                 #   self._stop_jump()
            else:
                self.on_object = None
        else:
            self.airborne = True

        if self.jump_state == JUMP:
            self._do_jump()

        self.update_pos()

    def move_direction(self, player_dir):
        #check if changing direction, if so reset x velocity
        if player_dir != self.direction:
            #self.xvel = 0
            self._flip_image()
        self.direction = player_dir
        self.iswalking = True

    # This function checks if the object is colliding and handles how the player
    # responds to collisions and maintains the list of possible interactive objects
    def collide(self, obj):
        if self.rect.colliderect(obj.rect):
            if obj not in self.pos_interact:
                    self.pos_interact.append(obj)
            if obj.collidable:
                #save the last collided object
                self.col_object = obj
                if obj.rect.collidepoint(self.rect.midbottom):
                    self.yvel = 0
                    self.rect.bottom = obj.rect.top
                    #save the object the player is on
                    self.on_object = obj
                elif obj.rect.collidepoint(self.rect.bottomleft):
                    if self.direction == DIR_LEFT:
                        self.xvel = 0
                elif obj.rect.collidepoint(self.rect.bottomright):
                    if self.direction == DIR_RIGHT:
                        self.xvel = 0
        else:
            if obj in self.pos_interact:
                    self.pos_interact.remove(obj)

    def interact(self, null, level):
        #interact with collide objects
        for obj in self.pos_interact:
            obj.interact(self, level)
        #interact with held item
        if self.held_item is not None:
            self.held_item.interact(self, level)

    def _flip_image(self):
        self.walking_anim.flip(True, False)
        self.jumping_anim.flip(True, False)

    def __next_jump_state(self):
        if self.jump_state == NOT_JUMPING:
            self.jump_state = JUMP_DELAY
            self.j_delay_timer.start_timer()
        elif self.jump_state == JUMP_DELAY:
            self.jump_state = JUMP
            self.jump_timer.start_timer()
            self._change_vel(DIR_UP, 2)
        elif self.jump_state == JUMP:
            self.jump_state = NOT_JUMPING
        else:
            print("Invalid player jump state: " + str(self.jump_state))

    def start_jump(self):
        self.__next_jump_state()

    def _do_jump(self):
        self._change_vel(DIR_UP, self.jumpvel)

    def update(self):
        self.move()

    def do_gravity(self, gravity):
        self._change_vel(DIR_DOWN, gravity)

    def drop(self, level):
        self.drop_item = self.held_item
        self.drop_item.obey_gravity = True
        self.held_item = None
        #level.place_object(self.drop_item)

    def pickup(self, obj, level):
        self.held_item = obj
        self.held_item.obey_gravity = False
        level.objects.change_layer(self.held_item, self._layer)
        self.held_item.rect.y = self.rect.centery + (self.rect.w / 6)
        self.held_item.rect.x = self.rect.centerx

        #save offsets from the top left of player sprite
        self.held_ofs_x = self.held_item.rect.x - self.rect.x
        self.held_ofs_y = self.held_item.rect.y - self.rect.y

    def update_pos(self):
        self.rect.x += self.xvel
        self.rect.y += self.yvel
        if self.held_item is not None:
            self.held_item.rect.x = self.rect.x + self.held_ofs_x
            self.held_item.rect.y = self.rect.y + self.held_ofs_y