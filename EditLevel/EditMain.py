__author__ = 'thvoidedline'

import os
from EditLevel.EditLevel import EditLevel
from Binding import *
from Timer import Timer

DATA_PATH = os.path.join('..', 'data')


def edit_main(screen):
    #pygame.init()
    #screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('LevelEdit')
    pygame.mouse.set_visible(1)
    clock = pygame.time.Clock()
    level = EditLevel(2000, 800, 'objects1.ini', DATA_PATH)
    pygame.display.flip()
    screen.blit(level.background, (0, 0))

    while 1:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == QUIT_EVENT:
                return
            if event.type == pygame.KEYUP:
                level.key_input(event.key)
            if event.type == pygame.MOUSEBUTTONUP:
                level.mouse_input(event)
            if event.type > pygame.USEREVENT:
                Timer.handle_event(event.type)

        level.update()
        level.draw(screen)
        level.gui_manager.draw(screen)
        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()