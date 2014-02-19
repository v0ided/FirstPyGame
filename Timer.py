import pygame


class Timer():
    _timers = []
    _free_ids = []

    def __init__(self, length, to_exec, repeat=False):
        self.timer_id = 0
        self.length = length
        self.to_exec = to_exec
        self.repeat = repeat
        Timer._timers.append(self)

    def start_timer(self):
        self.timer_id = Timer.__next_id()
        print('Starting timer id: ' + str(self.timer_id))
        pygame.time.set_timer(self.timer_id, self.length)

    def stop_timer(self):
        pygame.time.set_timer(self.timer_id, 0)

    def exec(self):
        print('Executing timer id: ' + str(self.timer_id))
        if self.to_exec:
            self.to_exec()
            self.stop_timer()
            self.release_id()

    def release_id(self):
        print('Released timer id: ' + str(self.timer_id))
        Timer.__release_id(self.timer_id)
        self.timer_id = 0

    @staticmethod
    def handle_event(timer_id):
        print('Handling event for timer id: ' + str(timer_id))
        for timer in Timer._timers:
            if timer.timer_id == timer_id:
                timer.exec()
                return True
        return False

    @staticmethod
    def __next_id():
        if len(Timer._free_ids) == 0:
            Timer._free_ids.extend(range(pygame.USEREVENT, pygame.NUMEVENTS))
        t_id = Timer._free_ids.pop()
        print('Getting id: ' + str(t_id))
        return t_id

    @staticmethod
    def __release_id(t_id):
        if t_id not in Timer._free_ids:
            Timer._free_ids.append(t_id)
        else:
            print('Duplicate id found in free ids')
