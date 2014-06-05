__author__ = 'thvoidedline'


from Objects.BaseObject import BaseObject
from Animation import Animation
from Timer import Timer
from Constants import *
from AnimationPlayer import Animation_Player

IDLE_ANIM = 0
WALK_ANIM = 1
JUMP_ANIM = 2


class PlayerSprite(BaseObject):
    def __init__(self, var_dict):
        BaseObject.__init__(self, var_dict)
        self.type = PLAYER
        self.xvel = 0
        self.yvel = 0
        self.jumpvel = 1
        self.walkvel = 0.05
        self.maxXvel = 2.3
        self.maxYvel = 8
        self.direction = DIR_RIGHT
        self.iswalking = False
        self.on_object = None
        self.col_object = None
        self.jump_state = NOT_JUMPING
        self.airborne = True
        self.j_delay_timer = Timer(50, self.__next_jump_state, False)
        self.jump_timer = Timer(240, self.__next_jump_state, False)
        self._layer = 10
        #Array of objects currently colliding with rect - Tracks objects that are possible to interact with
        self.pos_interact = []
        self.held_item = None
        self.drop_item = None
        self.collidable = True
        self.held_ofs_x = 0.0
        self.held_ofs_y = 0.0
        self.obey_gravity = True
        self.visible = True

        self.idle_files = var_dict['idle_files'].split(',')
        self.idle_times = var_dict['idle_times'].split(',')
        self.jump_files = var_dict['jump_files'].split(',')
        self.jump_times = var_dict['jump_times'].split(',')
        self.walk_files = var_dict['walk_files'].split(',')
        self.walk_times = var_dict['walk_times'].split(',')
        self.idle_anim = Animation(self.idle_files, self.idle_times)
        self.jumping_anim = Animation(self.jump_files, self.jump_times)
        self.walking_anim = Animation(self.walk_files, self.walk_times)
        self.walking_anim.set_colorkey((255, 255, 255))

        if var_dict['w'] == 0 or var_dict['h'] == 0:
            self.rect.w = self.idle_anim.getRect().w
            self.rect.h = self.idle_anim.getRect().h
        else:
            pass
            #Needs to scale all animations while keeping aspect ratio.
            #self.walking_anim.scale((var_dict['w'], var_dict['h']))
            #self.jumping_anim.scale((var_dict['w'], var_dict['h']))
        self.anim_player = Animation_Player()
        self.anim_player.add(self.walking_anim, WALK_ANIM)
        self.anim_player.add(self.jumping_anim, JUMP_ANIM)
        self.anim_player.add(self.idle_anim, IDLE_ANIM)
        self.anim_player.set(IDLE_ANIM, True)

    def draw(self, screen, rect_loc):
        if self.jump_state > 0:
            self.anim_player.set(JUMP_ANIM)
        elif self.iswalking is True:
            self.anim_player.set(WALK_ANIM)
        else:
            self.anim_player.set(IDLE_ANIM)

        self.anim_player.draw(screen, rect_loc)

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
        #check if changing direction, if so lessen x velocity
        if player_dir != self.direction:
            self.xvel -= self.xvel / 2
            self.anim_player.flip()
        self.direction = player_dir
        self.iswalking = True

    def collide(self, obj):
        """Returns if object is colliding, calls _respond_collision on True and _check_pos_interact every time"""
        colliding = False
        if self.rect.colliderect(obj.rect):
            colliding = True
            self._respond_collision(obj)

        self._check_pos_interact(obj, colliding)
        return colliding

    def _respond_collision(self, obj):
        """Responds to a collision, trusts the caller that the objects are colliding"""
        if obj.collidable:
                #save the last collided object
                self.col_object = obj
                if obj.rect.collidepoint(self.rect.midbottom):
                    self.yvel = 0
                    self.rect.bottom = obj.rect.top
                    #save the object the player is on
                    self.on_object = obj
                    #If falling, let jump state know player landed
                    if self.jump_state == FALLING:
                        self.__next_jump_state()
                elif obj.rect.collidepoint(self.rect.bottomleft):
                    if self.direction == DIR_LEFT:
                        self.xvel = 0
                elif obj.rect.collidepoint(self.rect.bottomright):
                    if self.direction == DIR_RIGHT:
                        self.xvel = 0

    def _check_pos_interact(self, obj, colliding):
        """Maintains list of objects with possible interaction"""
        if colliding:
            if obj not in self.pos_interact:
                self.pos_interact.append(obj)
        else:
            if obj in self.pos_interact:
                self.pos_interact.remove(obj)

    def __next_jump_state(self):
        if self.jump_state == NOT_JUMPING:
            self.jump_state = JUMP_DELAY
            self.j_delay_timer.start_timer()
        elif self.jump_state == JUMP_DELAY:
            self.jump_state = JUMP
            self.jump_timer.start_timer()
            self._change_vel(DIR_UP, 2)
        elif self.jump_state == JUMP:
            self.jump_state = FALLING
        elif self.jump_state == FALLING:
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

    def check_interactions(self):
        if not self._use_timer:
            self._use_timer = Timer(self.use_timer_len, self._set_can_use)
        if self._can_use:
            #interact with held item
            if self.held_item:
                if self.interact(self.held_item, PLACE):
                    self._can_use = False
                    self._use_timer.start_timer()
                    return

            for obj in self.pos_interact:
                if self.interact(obj, TOGGLE_POWER):
                    return

    def interact(self, obj, behvaior):
        print('interacting with ' + obj.name)
        for behavior in self.behaviors:
            if self.delegate_behavior(obj, behavior):
                return True
        return False

    def delegate_behavior(self, obj, behavior):
        if behavior == PICKUP:
            return self.pickup(obj)
        if behavior == PLACE:
            return self.drop()

        return obj.interact(self, behavior)

    def drop(self):
        if self.held_item:
            self.drop_item = self.held_item
            self.drop_item.visible = True
            self.drop_item.obey_gravity = True
            self.held_item = None
            print('dropped item')
            return True
        return False

    def pickup(self, obj):
        if PICKUP in obj.behaviors and not self.held_item:
            obj.visible = False
            obj.obey_gravity = False
            self.held_item = obj
            #level.objects.change_layer(self.held_item, self._layer) #Check/update this in level.draw function
            self.held_item.rect.y = self.rect.centery + (self.rect.w / 6)
            self.held_item.rect.x = self.rect.centerx
            #save offsets from the top left of player sprite
            self.held_ofs_x = self.held_item.rect.x - self.rect.x
            self.held_ofs_y = self.held_item.rect.y - self.rect.y
            print('picked up item')
            return True
        return False

    def update_pos(self):
        self.rect.x += self.xvel
        self.rect.y += self.yvel
        if self.held_item:
            self.held_item.rect.x = self.held_ofs_x + self.rect.x
            self.held_item.rect.y = self.held_ofs_y + self.rect.y