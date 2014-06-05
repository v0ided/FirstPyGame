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

    def set(self, anim_id, is_idle_anim=False):
        try:
            self._current_id = anim_id
            if is_idle_anim:
                self.idle = anim_id
        except TypeError:
            print("Invalid animation id")
            raise TypeError
        self.play()

    def draw(self, screen, loc):
        if self._current_id is None:
            return

        try:
            self.anims[self._current_id].blit(screen, loc)
        except (TypeError, KeyError):
            print("Invalid arguments given to Animation_Player.draw()")
            raise KeyError

    def play(self):
        if self._current_id is None:
            return

        try:
            self.anims[self._current_id].play()
        except KeyError:
            print('Invalid or no current animation')
            raise KeyError

    def pause(self):
        if self._current_id is None:
            return

        try:
            self.anims[self._current_id].pause()
        except KeyError:
            print('Invalid or no current animation')
            raise KeyError

    def stop(self):
        if self._current_id is None:
            return

        try:
            self.anims[self._current_id].stop()
        except KeyError:
            print('Invalid or no current animation')
            raise KeyError

    def flip(self, anim_id=None):
        """"Flip animations on the x axis, if anim_id=None, flip all animations"""
        if anim_id is None:
            [anim.flip(True, False) for anim in self.anims.values()]
        else:
            try:
                self.anims[anim_id].flip(True, False)
            except KeyError:
                print('Invalid id sent to flip function. Valid animations ids are:' + str(self.anims.keys()))