import pygame as pg
from eventmanager import EventManager
from constants import *

class PlayerHitbox():
    def __init__(self, image : pg.surface.Surface):
        self.image = image
        self.rect = image.get_rect()
        self.mask = pg.mask.from_surface(self.image)

class Player(pg.sprite.Sprite):
    def __init__(self, Position: tuple,  *groups: pg.sprite.Group):
        super().__init__(*groups)

        # Графика.
        self.birdimg = pg.image.load("gfx/bird.png").convert_alpha()
        self.birdimg = pg.transform.scale_by(self.birdimg, .08)
        self.image = self.birdimg
        self.rect = self.image.get_rect()

        # Звуки.
        self.jumpsound = pg.mixer.Sound("sounds/sound_wing.wav")
        self.jumpsound.set_volume(0.3)
        self.dashsound = pg.mixer.Sound("sounds/sound_whoosh.wav")
        self.dashsound.set_volume(0.3)
        self.hitsound = pg.mixer.Sound("sounds/sound_hit.wav")
        self.hitsound.set_volume(0.3)
        self.diesound = pg.mixer.Sound("sounds/sound_die.wav")
        self.diesound.set_volume(0.3)


        # Кастомный хитбокс
        hitboxsize = pg.transform.scale_by(self.birdimg, 0.75)
        self.hitbox = PlayerHitbox(hitboxsize)
        
        # Переменные игрока
        self.ogposition = Position
        self.velocity = pg.Vector2(0, 0)
        self.angle = 0
        self.dash_amount = 2
        self.gravityenabled = True
        self.dead = False


    def update(self):
        # Позиция и "Физика"
        self.rect.move_ip(self.velocity*PLAYERDAMPING)
        self.gravity()
        # Если птичка мертва, нет смысла идти дальше
        if self.dead:
            return

        self.collide()
        
        # Возвращает птичку обратно после деша.
        if self.gravityenabled:
            self.rect.centerx = pg.math.lerp(self.rect.centerx, self.ogposition[0], 0.01)

        # Быть может немного лишнее, но на всякий случай обрезаем velocity.
        self.velocity.x = pg.math.clamp(self.velocity.x, -PLAYERMAXVELOCITY[0], PLAYERMAXVELOCITY[0])
        self.velocity.y = pg.math.clamp(self.velocity.y, -PLAYERMAXVELOCITY[1], PLAYERMAXVELOCITY[1])

        # Вращательные Приколы.
        self.angle = pg.math.lerp(self.angle, -20, 0.04)
        self.image = pg.transform.rotate(self.birdimg, self.angle)
        self.rect = self.image.get_rect(center = self.rect.center)

        # Проверка событий.
        self.event_handle()


    def gravity(self):
        self.velocity.y += GRAVITY*self.gravityenabled
        self.velocity.x = pg.math.lerp(self.velocity.x, 0, 0.05)
        if self.rect.bottom >= BOTTOMCOLLISION:
            self.rect.bottom = BOTTOMCOLLISION
            self.velocity.xy = 0,0
    

    def jump(self):
        self.velocity.y = -PLAYERJUMPHEIGHT
        self.velocity.x = 0
        self.angle = 40
        self.gravityenabled = True # Полезно после дэша.
        self.jumpsound.play()

    def collide(self):
        # Коллизия с трубами
        _group = self.groups()[0]
        self.hitbox.rect.center = self.rect.center

        collision = pg.sprite.spritecollide(self.hitbox, _group, False, pg.sprite.collide_mask)
        _second = pg.sprite.spritecollide(self.hitbox, _group, False) # Этот нужен для того чтобы проверять
                                                                # Пролетели ли мы через трубу, полезно чтобы обновлять Score.
        for i in _second:
            if i.__class__.__name__ == "Pipe":
                if i in collision:
                    self.hitsound.play()
                    EventManager.ins.set_timer(100, method=lambda: self.diesound.play())
                    self.dead = True
                
                EventManager.ins.post_event(SCOREUP, {"pipe": i}) # Запоминаем с какой трубой соприкасаемся, 
                                                                    # чтобы не давать за одну трубу очки.

        # Проверка на коллизию с полом
        if self.rect.bottom >= BOTTOMCOLLISION:
            self.dead = True
            self.hitsound.play()


        if self.dead:
            EventManager.ins.post_event(PLAYERDEAD)


    def dash(self):
        direction = pg.Vector2(pg.mouse.get_pos()) - pg.Vector2(self.rect.center)

        if self.dash_amount > 0:
            direction.scale_to_length(MINDASHLENGTH)
            #direction.y = pg.math.clamp(direction.y, -MAXDASHLENGTH/2, MAXDASHLENGTH)
            self.velocity = direction
            self.angle = 40
            self.dash_amount -= 1
            self.dashsound.play()

            EventManager.ins.set_timer(delay=1500, method=self.dash_reload)
            self.gravityenabled = False # Выключаем на немного гравитацию, чтобы сделать дэш более протянутым
                                        # И убрать влияние гравитации на него
            EventManager.ins.set_timer(100, method=self.enable_gravity)


    # Вспомогательные методы, использующиеся в таймерах.
    def dash_reload(self): self.dash_amount += 1
    def enable_gravity(self): self.gravityenabled = True

    def event_handle(self):
        # Проверка Польз. Ввода
        keys = EventManager.ins.has_event(pg.KEYDOWN)
        if keys and keys.key == pg.K_SPACE:
            self.jump()

        if keys and keys.key == pg.K_LSHIFT:
            self.dash()
            