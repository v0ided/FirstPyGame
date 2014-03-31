__author__ = 'thvoidedline'

from Camera import Camera
from Constants import *


class EditCamera(Camera):
    def __init__(self, w, h):
        Camera.__init__(self, w, h)
        self.x_speed = 3
        self.y_speed = 3

    def update(self, mousepos):
        if mousepos[X] > self.rect.w * 0.75:
            self.rect.x += self.x_speed
        elif mousepos[X] < self.rect.w * 0.25:
            self.rect.x -= self.x_speed
        if mousepos[Y] > self.rect.h * 0.75:
            self.rect.y += self.y_speed
        elif mousepos[Y] < self.rect.h * 0.25:
            self.rect.y -= self.y_speed
