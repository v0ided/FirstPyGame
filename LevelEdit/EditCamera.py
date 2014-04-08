__author__ = 'thvoidedline'

from Camera import Camera
from Constants import *


class EditCamera(Camera):
    def __init__(self, w, h, limit_x, limit_y):
        Camera.__init__(self, w, h)
        self.x_speed = 3
        self.y_speed = 3
        self.limit_x = limit_x
        self.limit_y = limit_y

    def update(self, mousepos):
        if mousepos[X] > self.rect.w * 0.85:
            if self.rect.x + self.rect.w < self.limit_x:
                self.rect.x += self.x_speed
        elif mousepos[X] < self.rect.w * 0.15:
            if self.rect.x > 0:
                self.rect.x -= self.x_speed
        if mousepos[Y] > self.rect.h * 0.85:
            if self.rect.y + self.rect.h < self.limit_y:
                self.rect.y += self.y_speed
        elif mousepos[Y] < self.rect.h * 0.15:
            if self.rect.y > 0:
                self.rect.y -= self.y_speed
