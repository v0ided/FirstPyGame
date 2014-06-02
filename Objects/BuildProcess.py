__author__ = 'thvoidedline'

import pygame
from Objects.LevelObject import LevelObject
from Timer import Timer
from HelpFunctions import to_num
from Constants import BUILD_PROC


class BuildProcess(LevelObject):
    def __init__(self, var_dict):
        LevelObject.__init__(self, var_dict)
        self.type = BUILD_PROC
        str_input = var_dict['input']
        str_output = var_dict['output']
        self.input_items = [x.strip() for x in str_input.split(',')]
        self.output_items = [x.strip() for x in str_output.split(',')]
        self.length = to_num(var_dict['time'])
        self.delay_timer = Timer(5, self._ready)
        self.build_timer = Timer(self.length, self._finish)
        self.ready = True
        self.built = []  # list of output items that need to be spawned into the level
        self.input_area = self.rect  # required input parts must collide with this rect to start build
        self.output_area = pygame.Rect(self.rect.right, self.rect.bottom, 200, 100)  # items with output in this rect

    def _ready(self):
        print('ready')
        self.ready = True

    def _finish(self):
        print('Finished')
        self._build()
        self.ready = False
        self.delay_timer.start_timer()

    def start(self):
        if self.ready:
            print('Starting')
            self.build_timer.start_timer()

    def _build(self):
        print('built')
        [self.built.append(x) for x in self.output_items]

    def interact(self, obj, behavior):
        if self.ready:
            print('Starting')
            self.build_timer.start_timer()

    def provide_type_vars(self):
        LevelObject.provide_type_vars(self)
        yield ('input', str(self.input_items))
        yield ('output', str(self.output_items))
        yield ('time', str(self.length))
