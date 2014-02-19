import configparser
from HelpFunctions import *
from LevelObject import *
from Camera import Camera
from ObjFactory import *


class Background(pygame.sprite.Sprite):
    def __init__(self, bg_filename):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(bg_filename, -1)
        self.surface.blit(self.image, (0, 0))


class Level():
    def __init__(self, w, h, filename):
        self.width = w
        self.height = h
        self.background = pygame.Surface((w, h))
        self.background = self.background.convert()
        self.background.fill((153, 217, 234))
        self.objects = pygame.sprite.LayeredUpdates()
        self.gravity = .5
        self.camera = Camera(800, 600)
        self.groups = {}
        self.filename = filename
        self._load_objects()
        self.player = self._get_player_from_objects()

    def _get_player_from_objects(self):
        for obj in self.objects:
            if obj.type == PLAYER:
                return obj
        return None

    def _load_objects(self):
        obj_filename = os.path.join('data', 'level_data', self.filename)
        parser = configparser.ConfigParser()
        parser.read(obj_filename)

        object_list = parser.sections()
        for objname in object_list:
            obj_type = parser[objname]['type']
            var_dict = {'name': objname}
            for option in parser[objname]:
                value = parser[objname][option]
                if value.strip().isdigit():
                    var_dict[option] = to_num(value)
                else:
                    var_dict[option] = value

            self.objects.add(ObjFactory(obj_type, var_dict))

    def update(self):
        #update object positions
        for obj in self.objects:
            obj.update()
            if obj.obey_gravity:
                obj.do_gravity(self.gravity)
        self.group_obj_update()

        self.check_collisions()
        self.camera.update(self.player)

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        for sprite_layer in self.objects.layers():
            for sprite in self.objects.get_sprites_from_layer(sprite_layer):
                if self.camera.on_screen(sprite.rect) and sprite.visible:
                    translated = self.camera.translate(sprite.rect)
                    sprite.draw(screen, translated)

    #calls collide for each object against each object besides itself
    #objects' collide function carries out what it means to collide and how to respond
    def check_collisions(self):
        for a_obj in self.objects:
            for b_obj in self.objects:
                if a_obj == b_obj:
                    continue
                a_obj.collide(b_obj)

    def spawn_object(self, obj):
        #first determine spawn location, object should already have properties set
        for col_obj in self.objects:
            if col_obj.collidable:
                if obj is col_obj:
                    continue
                if col_obj is self.player:
                    continue
                if obj.rect.colliderect(col_obj.rect):
                    obj.rect.bottom = col_obj.rect.top
        obj.obey_gravity = True

    def _create_groups(self):
        for obj in self.objects:
            #If object is in a group
            if obj.group != 'no':
                #If group object for group exists yet
                if obj.group in self.groups:
                    #Checks if obj is in group already, if not adds to group
                    self.groups[obj.group].add(obj)

    def group_obj_update(self):
        for grp_name in self.groups:
            self.groups[grp_name].groupBehave()

    def get_group(self, name):
        if name in self.groups.keys():
            return self.groups[name]

    def objects_at(self, x, y, w=0, h=0):
        col_objects = []
        if w == 0 or h == 0:
            for obj in self.objects:
                if obj.rect.collidepoint(x, y):
                    col_objects.append(obj)
        else:
            for obj in self.objects:
                centered = pygame.Rect(x - (w / 2), y - (h / 2), w, h)
                if obj.rect.colliderect(centered):
                    col_objects.append(obj)
        return col_objects