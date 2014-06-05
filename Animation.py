__author__ = 'thvoidedline'


import pyganim


class Animation:
    def __init__(self, files, times):
        times = [float(time) for time in times if time != '']
        self.files = list(zip(files, times))
        self.id = -1
        self.anim = None
        self.loop = False

        self.idle_anim = pyganim.PygAnimation(self.files)

    def getRect(self):
        return self.idle_anim.getRect()

    def scale(self, w_h):
        return self.idle_anim.scale(w_h)

    def blit(self, destSurface, dest):
        return self.idle_anim.blit(destSurface, dest)

    def blitFrameNum(self, frame_num, destSurface, dest):
        return self.idle_anim.blitFrameNum(frame_num, destSurface, dest)

    def play(self, startTime=None):
        self.idle_anim.play(startTime)

    def stop(self):
        self.idle_anim.stop()

    def set_colorkey(self, color=None, flags=0):
        return self.idle_anim.set_colorkey(color, flags)

    def flip(self, boolx, booly):
        return self.idle_anim.flip(boolx, booly)