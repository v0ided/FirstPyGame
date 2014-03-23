import pygame


class Camera(pygame.sprite.Sprite):
    def __init__(self, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.focus_tol = 200
        self.x_speed = 2
        self.y_speed = 1.5

    def update(self, target):
        if target.rect.x > self.rect.x + (self.rect.w - self.focus_tol):
            self.rect.x += self.x_speed
        elif target.rect.x < self.rect.x + self.focus_tol:
            self.rect.x -= self.x_speed

        if target.rect.y > self.rect.y + (self.rect.h - self.focus_tol):
            self.rect.y += self.y_speed
        elif target.rect.y < self.rect.y + self.focus_tol:
            self.rect.y -= self.y_speed

    def on_screen(self, target):
        #todo:check if target is a valid rect
        if self.rect.colliderect(target):
            return True
        else:
            return False

    def translate_to(self, trans_rect):
        return trans_rect.move((-self.rect.x, -self.rect.y))

    def translate_from(self, rect):
        return rect.move((self.rect.x, self.rect.y))