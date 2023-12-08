import pygame
from sys import exit

### INITIALIZATION ###
pygame.init()
screen = pygame.display.set_mode([640, 720])
pygame.display.set_caption("Shitty Bird")
FPS = pygame.time.Clock()

### CREATING STUFF ###
Sprites = pygame.sprite.Group() # ALL SPRITES THAT WILL BE DRAWN AND UPDATED ON SCREEN (By default, please pass this group to all sprites)

### UPDATE ###
while True:
    # HANDE EVENTS
    for event in pygame.event.get():
        # QUIT EVENT.
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # KEYBOARD EVENTS.
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    # GRAPHICS
    screen.fill("cyan")
    Sprites.update()
    Sprites.draw(screen)

    # REDRAW    
    pygame.display.flip()
    FPS.tick(60)
    