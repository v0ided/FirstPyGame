__author__ = 'thvoidedline'


class Animation_Player:
    def __init__(self):
        self.idle = None
        self.anims = {}
        self._current_id = None

    def add(self, anim, anim_id):
        try:
            self.anims[anim_id] = anim
        except KeyError:
            print('Invalid Animation or Id')
            raise KeyError

    def set(self, anim_id, is_idle_anim):
        try:
            self._current_id = anim_id
            if is_idle_anim:
                self.idle = anim_id
        except TypeError:
            print("Invalid animation id")
            raise TypeError

    def draw(self, screen, loc):
        try:
            self.anims[self._current_id].blit(screen, loc)
        except (TypeError, KeyError):
            print("Invalid arguments given to Animation_Player.draw()")
            raise KeyError

    def play(self):
        try:
            self.anims[self._current_id].play()
        except KeyError:
            print('Invalid or no current animation')
            raise KeyError

    def pause(self):
        try:
            self.anims[self._current_id].pause()
        except KeyError:
            print('Invalid or no current animation')
            raise KeyError

    def stop(self):
        try:
            self.anims[self._current_id].play()
        except KeyError:
            print('Invalid or no current animation')
            raise KeyError