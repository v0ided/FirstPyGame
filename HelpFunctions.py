import os
import collections
import pygame


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        raise
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image, image.get_rect()


def to_num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)


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

#def if_exisit_get(objdict, key):

