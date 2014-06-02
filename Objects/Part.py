__author__ = 'thvoidedline'

from Objects.LevelObject import LevelObject
from Constants import PART


class Part(LevelObject):
    parts = {'edged_panel': 'e_panel.png'}

    def __init__(self, var_dict):
        try:
            var_dict['file1'] = Part.lookup_image(var_dict['name'])
            var_dict['behavior0'] = 'pickup'
            LevelObject.__init__(self, var_dict)
            self.type = PART
            self.quality = var_dict['quality']
        except KeyError:
            print('invalid/missing keys sent to part __init__')
            raise KeyError

    @staticmethod
    def lookup_image(lookup):
        try:
            part = next(x for x in Part.parts.keys() if x == lookup)
            return Part.parts[part]
        except KeyError:
            return None

    def provide_type_vars(self):
        LevelObject.provide_type_vars(self)
        yield ('quality', self.quality)


