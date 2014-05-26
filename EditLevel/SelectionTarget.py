__author__ = 'thvoidedline'

import pygame
import os
from HelpFunctions import load_image


class SelectionTarget(pygame.sprite.Sprite):
    def __init__(self, data_path):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(os.path.join(data_path, "selection_target.png"))
        self.image.set_colorkey((255, 255, 255))

    def draw(self, screen, translated):
        screen.blit(self.image, translated)

    def resize(self, sel_obj):
        self.image = pygame.transform.scale(self.image, (sel_obj.w, sel_obj.h))