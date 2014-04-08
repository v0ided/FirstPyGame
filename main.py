from Level import *
from Constants import *

DATA_PATH = os.path.join('data')


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Game')
    pygame.mouse.set_visible(0)
    clock = pygame.time.Clock()
    level = Level(2000, 800, 'objects1.ini', DATA_PATH)
    pygame.display.flip()
    screen.blit(level.background, (0, 0))

#Main Loop
    while 1:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            if event.type > pygame.USEREVENT:
                Timer.handle_event(event.type)

        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            level.player.move_direction(DIR_RIGHT)
        elif pygame.key.get_pressed()[pygame.K_LEFT]:
            level.player.move_direction(DIR_LEFT)
        else:
            level.player.iswalking = False
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            if level.player.jump_state == NOT_JUMPING and level.player.airborne is not True:
                level.player.start_jump()
        if pygame.key.get_pressed()[pygame.K_a]:
            level.player.interact(None, level)

        level.update()
        level.draw(screen)

        pygame.display.flip()

if __name__ == '__main__': main()