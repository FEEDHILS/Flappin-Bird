import pygame
from eventmanager import EventManager
from constants import *

class Player(pygame.sprite.Sprite):
    def __init__(self, Position: tuple,  *groups: pygame.sprite.Group):
        # PRIMARY
        super().__init__(*groups)


        # VARIABLES AND MAIN INITIALIZATION.

        # GRAPHICS.
        self.birdimg = pygame.image.load("graphics/bird.png").convert_alpha()
        self.birdimg = pygame.transform.scale_by(self.birdimg, .08)
        self.image = self.birdimg
        self.rect = self.image.get_rect()
        
        # PLAYER VARIABLES.
        self.rect.center = Position
        self.velocity = pygame.Vector2(0, 0)
        self.angle = 0
        self.dash_amount = 1
        self.gravityenabled = True


    def update(self):
        # POSITION CHANGE DUE TO VELOCITY.
        self.rect.move_ip(self.velocity*PLAYERDAMPING)
        self.gravity()


        # CHECK FOR BOTTOM COLLISION.
        if self.rect.bottom >= BOTTOMCOLLISION:
            self.rect.bottom = BOTTOMCOLLISION
            self.velocity.xy = 0,0

        # CLAMPS VELOCITY.
        self.velocity.x = pygame.math.clamp(self.velocity.x, -PLAYERMAXVELOCITY[0], PLAYERMAXVELOCITY[0])
        self.velocity.y = pygame.math.clamp(self.velocity.y, -PLAYERMAXVELOCITY[1], PLAYERMAXVELOCITY[1])

        # ROTATION STUFF.
        self.angle = pygame.math.lerp(self.angle, -20, 0.04)
        self.image = pygame.transform.rotate(self.birdimg, self.angle)
        self.rect = self.image.get_rect(center = self.rect.center)

        # CHECK FOR EVENTS.
        self.event_handle()


    def gravity(self):
        self.velocity.y += GRAVITY*self.gravityenabled
        self.velocity.x = pygame.math.lerp(self.velocity.x, 0, 0.05)
    

    def jump(self):
        self.velocity.y = -PLAYERJUMPHEIGHT
        self.velocity.x = 0
        self.angle = 40
        self.gravityenabled = True


    def dash(self):
        direction = pygame.Vector2(pygame.mouse.get_pos()) - pygame.Vector2(self.rect.center)

        if direction.length() > 10 and self.dash_amount >= 1:
            direction.scale_to_length(min(MAXDASHLENGTH, direction.length()))
            direction.y = pygame.math.clamp(direction.y, -MAXDASHLENGTH/2, MAXDASHLENGTH)
            self.velocity = direction
            self.dash_amount -= 1
            pygame.time.set_timer(pygame.event.Event(DASHRELOAD), 3000, loops=1)
            self.gravityenabled = False # For a brief period of time we disable gravity, to make dash more... ehm, better?
            pygame.time.set_timer(pygame.event.Event(PLAYERENABLEGRAVITY), 100, loops=1) # Enables gravity after 100ms.
            self.angle = 40



    def event_handle(self):
        ## KEYBOARD EVENTS
        keys = EventManager().has_event(pygame.KEYDOWN)
        if keys and keys.key == pygame.K_SPACE:
            self.jump()
        

        if keys and keys.key == pygame.K_LSHIFT:
            self.dash()
            pass


        # DASH RELOADING
        if EventManager().has_event(DASHRELOAD):
            print("Dash Restored")
            self.dash_amount += 1
        
        # ENABLE GRAVITY
        if EventManager().has_event(PLAYERENABLEGRAVITY):
            self.gravityenabled = True
            