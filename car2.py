from ntpath import join
import pygame
from random import randint, uniform


class Ferrari(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load('cat.png').convert_alpha()
        self.rect = self.image.get_frect(center = (screen_width / 2, screen_height / 2))
        self.direction = pygame.Vector2()
        self.speed = 300

        #cooldown time
        self.can_throw = True
        self.nana_throw_time = 0
        self.cooldown_duration = 400

        #mask
        self.mask = pygame.mask.from_surface(self.image)

    def nana_timer(self):
        if not self.can_throw:
            current_time = pygame.time.get_ticks()
            if current_time - self.nana_throw_time >= self.cooldown_duration:
                self.can_throw = True


    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_throw:
            Nana(nana_surf, self.rect.midtop, (all_sprites, nana_sprites) )
            self.can_throw = False
            self.nana_throw_time = pygame.time.get_ticks()

        self.nana_timer()

class Fia(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (randint(0, screen_width),randint(0, screen_height)))

class Nana(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)
  

    def update(self, dt):
        self.rect.centery -= 400* dt
        if self.rect.bottom < 0:
            self.kill()

class Max(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.original_surf =surf
        self.image = surf
        self.rect = self.image.get_frect(center = pos)
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 3000
        self.direction = pygame.Vector2((-0.5, 0.5),1)
        self.speed = randint(400, 500)
        self.rotation_speed = randint(20,50)
        self.rotation_angle = 0
    
    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()
        self.rotation_angle += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_surf, self.rotation_angle, 1)

class animation(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(center = pos)
       

    def update(self, dt):
        self.frame_index += 20 * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.kill()

def collisions():
    global running

    collision_sprites = pygame.sprite.spritecollide(ferrari, max_sprites, True)
    if collision_sprites:
        running = False

    for nana_sprite in nana_sprites:
        collided_sprites = pygame.sprite.spritecollide(nana_sprite, max_sprites, True)
        if collided_sprites:
            nana_sprite.kill()
            animation(explosion_frames, nana_sprite.rect.midtop, all_sprites)

def scores():
    current_time = pygame.time.get_ticks() // 1000
    text_surf = font.render(str(current_time), True, (240,240,240))
    text_rect = text_surf.get_frect(midbottom = (screen_width / 2, screen_height - 50))
    screen.blit(text_surf, text_rect)
    pygame.draw.rect(screen, (240,240,240), text_rect.inflate(20,20).move(0,-5), 5, 10)

#general setup
pygame.init()
pygame.display.set_caption("F1 survival")
screen_width, screen_height = 1280, 720 #main surface we draw on
screen = pygame.display.set_mode((screen_width, screen_height))
running = True
clock = pygame.time.Clock()

#import
bg_surf = pygame.image.load('bg1.jpg').convert()
bg_surf = pygame.transform.scale(bg_surf, (screen_width, screen_height)) 
fia_surf = pygame.image.load('star.png').convert_alpha()
max_surf = pygame.image.load('kitty.png').convert_alpha()
nana_surf = pygame.image.load('nana.png').convert_alpha()
font = pygame.font.Font(None, 40)
explosion_frames = [pygame.image.load(join('boom', f'{i}.png')).convert_alpha() for i in range(7)]
print(explosion_frames)

#sprites
all_sprites = pygame.sprite.Group()
max_sprites = pygame.sprite.Group()
nana_sprites = pygame.sprite.Group()
for i in range(30):
    Fia(all_sprites, fia_surf)
ferrari = Ferrari(all_sprites)

#custom events -> max events (timer)
max_event = pygame.event.custom_type()
pygame.time.set_timer(max_event, 500)

while running:
    dt = clock.tick() / 1000
    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == max_event:
            x, y = randint(0, screen_width), randint(-200, -100)
            Max(max_surf, (x, y), (all_sprites, max_sprites))

    #update
    all_sprites.update(dt)
    collisions()

    #draw the game
    screen.blit(bg_surf, (0, 0))
    scores()
    all_sprites.draw(screen)

    pygame.display.flip()

pygame.quit()



