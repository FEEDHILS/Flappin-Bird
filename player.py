import pygame
from eventmanager import EventManager
from constants import *

class PlayerHitbox():
    def __init__(self, image : pygame.surface.Surface):
        self.image = image
        self.rect = image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

class Player(pygame.sprite.Sprite):
    def __init__(self, Position: tuple,  *groups: pygame.sprite.Group):
        super().__init__(*groups)
        ### VARIABLES AND MAIN INITIALIZATION. ###

        # GRAPHICS.
        self.birdimg = pygame.image.load("gfx/bird.png").convert_alpha()
        self.birdimg = pygame.transform.scale_by(self.birdimg, .08)
        self.image = self.birdimg
        self.rect = self.image.get_rect()

        #CUSTOM HITBOX
        hitboxsize = pygame.transform.scale_by(self.birdimg, 0.75)
        self.hitbox = PlayerHitbox(hitboxsize)
        
        # PLAYER VARIABLES.
        self.ogposition = Position
        self.velocity = pygame.Vector2(0, 0)
        self.angle = 0
        self.dash_amount = 2
        self.gravityenabled = True
        self.dead = False


    def update(self):
        # POSITION & PHYSICS.
        self.rect.move_ip(self.velocity*PLAYERDAMPING)
        self.gravity()
        if not self.dead:
            self.collide()

        

        # Brings the bird back after dash.
        if self.gravityenabled:
            self.rect.centerx = pygame.math.lerp(self.rect.centerx, self.ogposition[0], 0.01)

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
        self.gravityenabled = True # Полезно после дэша.

    def collide(self):
        # PIPE COLLISION
        _group = self.groups()[0]
        self.hitbox.rect.center = self.rect.center

        collision = pygame.sprite.spritecollide(self.hitbox, _group, False, pygame.sprite.collide_mask)
        for i in collision:
            if i.__class__.__name__ == "Pipe":
                self.dead = True


        # CHECK FOR BOTTOM COLLISION.
        if self.rect.bottom >= BOTTOMCOLLISION:
            self.rect.bottom = BOTTOMCOLLISION
            self.velocity.xy = 0,0
            self.dead = True

        
        if self.dead:
            pygame.event.post(pygame.event.Event(PLAYERDEAD))


    def dash(self):
        direction = pygame.Vector2(pygame.mouse.get_pos()) - pygame.Vector2(self.rect.center)

        if self.dash_amount >= 1:
            direction.scale_to_length(MINDASHLENGTH)
            #direction.y = pygame.math.clamp(direction.y, -MAXDASHLENGTH/2, MAXDASHLENGTH)
            self.velocity = direction
            self.angle = 40
            self.dash_amount -= 1

            pygame.time.set_timer(pygame.event.Event(DASHRELOAD), 1500, loops=2-self.dash_amount)
            self.gravityenabled = False # For a brief period of time we disable gravity, to make dash more... ehm, better?
            pygame.time.set_timer(pygame.event.Event(PLAYERENABLEGRAVITY), 100, loops=1) # Enables gravity after 100ms.



    def event_handle(self):
        ## KEYBOARD EVENTS
        if self.dead:
            return

        keys = EventManager.ins.has_event(pygame.KEYDOWN)
        if keys and keys.key == pygame.K_SPACE:
            self.jump()

        if keys and keys.key == pygame.K_LSHIFT:
            self.dash()
            pass

        # DASH RELOADING
        if EventManager.ins.has_event(DASHRELOAD):
            print("Dash Restored")
            self.dash_amount += 1
        
        # ENABLE GRAVITY
        if EventManager.ins.has_event(PLAYERENABLEGRAVITY):
            self.gravityenabled = True
            