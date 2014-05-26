__author__ = 'thvoidedline'


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
        length = to_num(var_dict['time'])
        self.delay_timer = Timer(5, self._start)
        self.build_timer = Timer(length, self._finish)
        self.ready = True

    def _ready(self):
        print('ready')
        self.ready = True

    def _finish(self):
        print('Finished')
        self.ready = False
        self.delay_timer.start_timer()

    def start(self):
        if self.ready:
            print('Starting')
            self.build_timer.start_timer()

