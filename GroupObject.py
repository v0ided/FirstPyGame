from BaseObject import *

X = 0
Y = 1
WAIT = 2


class GroupObject(BaseObject):
    def __init__(self, var_dict):
        BaseObject.__init__(self, var_dict)
        self.type = GROUP_OBJECT
        self._objects = []

    def _configure(self, obj):
        print('parent configure called.')

    def add(self, obj):
        assert(obj is not None)

        if obj not in self._objects:
            self._objects.append(obj)
            self._configure(obj)

    def groupBehave(self):
        print('parent group behave called.')