import os
import collections
import glob
import pygame
from Constants import *


def load_image(name, colorkey=None):
    try:
        image = pygame.image.load(name)
    except pygame.error:
        raise
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image, image.get_rect()


def search_file(path, term):
    results = []
    for file in glob.glob(os.path.join(path, "*" + term + "*")):
        if os.path.isfile(os.path.basename(file)):
            results.append(os.path.basename(file))
    return results


def to_num(s):
    try:
        s = int(s)
        return s
    except ValueError:
        pass

    try:
        s = float(s)
        return s
    except ValueError:
        pass

    return s


def get_iterable(x):
    if isinstance(x, collections.Iterable):
        return x
    else:
        return x,


def to_bool(bool_str):
    if bool_str.lower() in ['true', 'yes', 'y']:
        return True
    elif bool_str.lower() in ['false', 'no', 'n']:
        return False
    else:
        return None


def to_behavior(str_behavior):
    behavior = str_behavior.lower()
    if behavior == 'pickup':
        return PICKUP
    elif behavior == 'place':
        return PLACE
    elif behavior == 'toggle_power':
        return TOGGLE_POWER
    else:
        print(str_behavior + " was not recognized by to_behavior()")
        return NOTHING


def behavior_str(behavior):
    if behavior == PICKUP:
        return 'pickup'
    elif behavior == PLACE:
        return 'place'
    elif behavior == TOGGLE_POWER:
        return 'toggle_power'
    else:
        print("Unable to convert behavior to string")
        return "invalid"


def obj_type_str(obj_type):
    if obj_type == BASE_OBJECT:
        return "baseobject"
    if obj_type == LEVEL_OBJECT:
        return "levelobject"
    if obj_type == PLAYER:
        return "player"
    if obj_type == CRANE_OBJECT:
        return "craneobject"
    if obj_type == PLATFORM:
        return "platform"
    if obj_type == BUILD_PROC:
        return "buildprocess"
    if obj_type == PART:
        return "part"


def index_by_value(value, container):
    i = 0
    for v in container:
        if value == v:
            return i
        i += 1
    return -1


def get_colorkey_hitmask(image, rect, key=None):
    """returns a hitmask using an image's colorkey.
       image->pygame Surface,
       rect->pygame Rect that fits image,
       key->an over-ride color, if not None will be used instead of the image's colorkey"""
    if key is None:
        colorkey = image.get_colorkey()
    else:
        colorkey = key
    mask = []
    for x in range(rect.width):
        mask.append([])
        for y in range(rect.height):
            mask[x].append(not image.get_at((x, y)) == colorkey)
    return mask


def get_colorkey_and_alpha_hitmask(image, rect, colorkey=None, alpha=0):
    """returns a hitmask using an image's colorkey and alpha."""
    mask = []
    for x in range(rect.width):
        mask.append([])
        for y in range(rect.height):
            mask[x].append(not (image.get_at((x, y))[3] == alpha or image.get_at((x, y)) == colorkey))
    return mask


def check_collision(obj1, obj2):
    """checks if two objects have collided, using hitmasks"""
    try:
        rect1, rect2, hm1, hm2 = obj1.rect, obj2.rect, obj1.hitmask, obj2.hitmask
    except AttributeError:
        return False
    rect = rect1.clip(rect2)
    if rect.width == 0 or rect.height == 0:
        return False
    x1, y1, x2, y2 = rect.x-rect1.x, rect.y-rect1.y, rect.x-rect2.x, rect.y-rect2.y
    for x in range(rect.width):
        for y in range(rect.height):
            if hm1[x1+x][y1+y] and hm2[x2+x][y2+y]:
                return True
            else:
                continue
    return False