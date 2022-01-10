import pygame
from config import *
import math
import random


class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height, color=WHITE):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(color)
        return sprite


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = 38
        self.height = 52

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.animation_loop = 1

        self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.up_animations = [self.game.character_spritesheet.get_sprite(0, 0, 38, 52),
                              self.game.character_spritesheet.get_sprite(38, 0, 32, 50),
                              self.game.character_spritesheet.get_sprite(69, 0, 32, 50),
                              self.game.character_spritesheet.get_sprite(131, 0, 32, 50),
                              self.game.character_spritesheet.get_sprite(162, 0, 32, 50),
                              self.game.character_spritesheet.get_sprite(194, 0, 32, 50),
                              self.game.character_spritesheet.get_sprite(228, 0, 32, 50)]

        self.left_animations = [self.game.character_spritesheet.get_sprite(0, 65, 38, 52),
                                self.game.character_spritesheet.get_sprite(38, 65, 32, 50),
                                self.game.character_spritesheet.get_sprite(69, 65, 32, 50),
                                self.game.character_spritesheet.get_sprite(131, 65, 32, 50),
                                self.game.character_spritesheet.get_sprite(162, 65, 32, 50),
                                self.game.character_spritesheet.get_sprite(194, 65, 32, 50),
                                self.game.character_spritesheet.get_sprite(228, 65, 32, 50)]

        self.down_animations = [self.game.character_spritesheet.get_sprite(0, 130, 38, 52),
                                self.game.character_spritesheet.get_sprite(38, 130, 32, 50),
                                self.game.character_spritesheet.get_sprite(69, 130, 32, 50),
                                self.game.character_spritesheet.get_sprite(131, 130, 32, 50),
                                self.game.character_spritesheet.get_sprite(162, 130, 32, 50),
                                self.game.character_spritesheet.get_sprite(194, 130, 32, 50),
                                self.game.character_spritesheet.get_sprite(228, 130, 32, 50)]

        self.right_animations = [self.game.character_spritesheet.get_sprite(0, 194, 38, 52),
                                 self.game.character_spritesheet.get_sprite(38, 194, 32, 50),
                                 self.game.character_spritesheet.get_sprite(69, 194, 32, 50),
                                 self.game.character_spritesheet.get_sprite(131, 194, 32, 50),
                                 self.game.character_spritesheet.get_sprite(162, 194, 32, 50),
                                 self.game.character_spritesheet.get_sprite(194, 194, 32, 50),
                                 self.game.character_spritesheet.get_sprite(228, 194, 32, 50)]

    def update(self):
        self.movement()
        self.animate()
        self.collide_enemy()

        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y_change += PLAYER_SPEED
            self.facing = 'down'

    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            self.game.character.hp -= 0.5
            self.attacked()
        if self.game.character.hp <= 0:
            self.kill()
            self.game.respawn()

    def attacked(self):
        self.rect.x -= 30
        self.rect.y -= 30

    def collide_blocks(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                    return
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                    return

        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                    return
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    return

    def animate(self):
        if self.facing == 'down':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(0, 130, 38, 52)
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.2
                if self.animation_loop >= 7:
                    self.animation_loop = 1

        if self.facing == 'up':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(0, 0, 38, 52)
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.2
                if self.animation_loop >= 7:
                    self.animation_loop = 1

        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(0, 65, 38, 52)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.2
                if self.animation_loop >= 7:
                    self.animation_loop = 1

        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(0, 194, 38, 52)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.2
                if self.animation_loop >= 7:
                    self.animation_loop = 1


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(['left', 'right'])
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = random.randint(7, 30)

        self.image = self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.left_animations = [self.game.enemy_spritesheet.get_sprite(10, 75, 36, 50),
                                self.game.enemy_spritesheet.get_sprite(45, 75, 36, 50),
                                self.game.enemy_spritesheet.get_sprite(10, 75, 36, 50),
                                self.game.enemy_spritesheet.get_sprite(84, 75, 36, 50)]

        self.right_animations = [self.game.enemy_spritesheet.get_sprite(10, 205, 42, 50),
                                 self.game.enemy_spritesheet.get_sprite(55, 205, 36, 50),
                                 self.game.enemy_spritesheet.get_sprite(10, 205, 42, 50),
                                 self.game.enemy_spritesheet.get_sprite(94, 205, 36, 50)]

    def update(self):
        self.movement()
        self.animate()
        # self.collide_enemy()

        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        if self.facing == 'left':
            self.x_change -= ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= 0 - self.max_travel:
                self.facing = 'right'

        if self.facing == 'right':
            self.x_change += ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = 'left'

    def animate(self):
        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(10, 75, 36, 47)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 4:
                    self.animation_loop = 1

        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(10, 205, 36, 47)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 4:
                    self.animation_loop = 1


class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y


class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(64, 352, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font('arialmt.ttf', fontsize)
        self.content = content

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.fg = fg
        self.bg = bg

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))
        self.image.blit(self.text, self.text_rect)

    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                print((self.rect.x, self.rect.y))
                print(pos)
                return True
            return False
        return False


class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE

        self.animation_loop = 0

        self.image = self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.right_animations = [self.game.attack_spritesheet.get_sprite(0, 64, self.width, self.height, BLACK),
                                 self.game.attack_spritesheet.get_sprite(30, 64, self.width, self.height, BLACK),
                                 self.game.attack_spritesheet.get_sprite(64, 64, self.width, self.height, BLACK),
                                 self.game.attack_spritesheet.get_sprite(96, 64, self.width, self.height, BLACK),
                                 self.game.attack_spritesheet.get_sprite(128, 64, self.width, self.height, BLACK)]

        self.down_animations = [self.game.attack_spritesheet.get_sprite(0, 30, self.width, self.height, BLACK),
                                self.game.attack_spritesheet.get_sprite(30, 30, self.width, self.height, BLACK),
                                self.game.attack_spritesheet.get_sprite(64, 30, self.width, self.height, BLACK),
                                self.game.attack_spritesheet.get_sprite(96, 30, self.width, self.height, BLACK),
                                self.game.attack_spritesheet.get_sprite(128, 30, self.width, self.height, BLACK)]

        self.left_animations = [self.game.attack_spritesheet.get_sprite(0, 96, self.width, self.height, BLACK),
                                self.game.attack_spritesheet.get_sprite(30, 96, self.width, self.height, BLACK),
                                self.game.attack_spritesheet.get_sprite(64, 96, self.width, self.height, BLACK),
                                self.game.attack_spritesheet.get_sprite(96, 96, self.width, self.height, BLACK),
                                self.game.attack_spritesheet.get_sprite(128, 96, self.width, self.height, BLACK)]

        self.up_animations = [self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height, BLACK),
                              self.game.attack_spritesheet.get_sprite(30, 0, self.width, self.height, BLACK),
                              self.game.attack_spritesheet.get_sprite(64, 0, self.width, self.height, BLACK),
                              self.game.attack_spritesheet.get_sprite(96, 0, self.width, self.height, BLACK),
                              self.game.attack_spritesheet.get_sprite(128, 0, self.width, self.height, BLACK)]

    def update(self):
       self.animate()
       self.collide()

    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, True)

    def animate(self):
        direction = self.game.player.facing

        if direction == 'up':
            self.image = self.up_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

        if direction == 'down':
            self.image = self.down_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

        if direction == 'left':
            self.image = self.left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

        if direction == 'right':
            self.image = self.right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()
