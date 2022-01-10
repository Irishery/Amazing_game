import pygame
import sys
from sprites import *
from config import *
from tilemap import *
from inventory import *
from character import Character


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font('arialmt.ttf', 32)

        self.character = Character(7, 3, 2, 1)
        self.inventory = Inventory(self.character.hp, self)

        self.character_spritesheet = Spritesheet("img/character.png")
        self.terrain_spritesheet = Spritesheet("img/terrain.png")
        self.enemy_spritesheet = Spritesheet("img/enemy.png")
        self.attack_spritesheet = Spritesheet("img/attack.png")
        self.intro_background = pygame.image.load("img/introbackground.png")
        self.go_background = pygame.image.load("img/gameover.png")
        self.map = TiledMap("map_sprites2/map1.tmx")
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

    def create_tilemap(self):
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'block':
                Block(self, tile_object.x, tile_object.y,
                      tile_object.width, tile_object.height)
            if tile_object.name == 'player':
                self.player = Player(self, tile_object.x, tile_object.y)
                self.spawn_point = (tile_object.x, tile_object.y)
            if tile_object.name == 'enemy':
                Enemy(self, tile_object.x, tile_object.y)

    def respawn(self):
        self.character.hp = 7
        self.player = Player(self, self.spawn_point[0], self.spawn_point[1])

    def new(self):
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        # self.player = Player(self, 10, 10)
        self.create_tilemap()
        self.camera = Camera(self.map.width, self.map.height)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.player.facing == 'up':
                        Attack(self, self.player.rect.x, self.player.rect.y - 25)
                    if self.player.facing == 'down':
                        Attack(self, self.player.rect.x, self.player.rect.y + 45)
                    if self.player.facing == 'left':
                        Attack(self, self.player.rect.x - TILESIZE, self.player.rect.y + 25)
                    if self.player.facing == 'right':
                        Attack(self, self.player.rect.x + TILESIZE, self.player.rect.y + 20)
                if event.key == pygame.K_i:
                    self.inventory.render(self.screen)
                    pygame.display.update()

    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)

    def draw(self):
        pygame.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def game_over(self):
        text = self.font.render('Game Over', True, WHITE)
        text_rect = text.get_rect()

        restart_button = Button(10, WIN_HEIGHT - 60, 120, 50, WHITE, BLACK, 'Restart', 32)

        for sprite in self.all_sprites:
            sprite.kill()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                self.new()
                self.main()

            self.screen.blit(self.go_background, (0, 0))
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_button.image, restart_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def intro_screen(self):
        intro = True

        title = self.font.render('Amazind game', True, BLACK)
        title_rect = title.get_rect(x=10, y=10)

        play_button = Button(10, 50, 100, 50, WHITE, BLACK, 'Play', 32)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False

            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()


g = Game()
g.intro_screen()
g.new()
g.inventory.add_item(Weapon('img', 1, 7, 'axe', 'Great axe'))
g.inventory.add_item(Weapon('img', 1, 5, 'sword', 'Ukraine'))
g.inventory.add_item(Weapon('img', 1, 2, 'axe', 'Small axe'))
g.inventory.add_item(Weapon('img', 1, 0, 'Very low', 'IQ'))
g.inventory.add_item(Weapon('img', 1, 7, 'axe', 'Great axe'))
g.inventory.add_item(Weapon('img', 1, 7, 'axe', 'Great axe'))
g.inventory.add_item(Weapon('img', 1, 7, 'axe', 'Great axe'))
g.inventory.add_item(Weapon('img', 1, 7, 'axe', 'Great axe'))
g.inventory.add_item(Weapon('img', 1, 7, 'axe', 'Great axe'))
g.inventory.add_item(Weapon('img', 1, 7, 'axe', 'Great axe'))
g.inventory.add_item(Weapon('img', 1, 7, 'axe', 'Great axe'))
g.inventory.add_item(Weapon('img', 1, 7, 'axe', 'Great axe'))
g.inventory.add_item(Weapon('img', 1, 7, 'axe', 'Great axe'))
g.inventory.add_item(Weapon('img', 1, 7, 'axe', 'Great axe'))
g.inventory.add_item(Weapon('img', 1, 7, 'axe', 'Great axe'))
g.inventory.add_item(Weapon('img', 1, 7, 'axe', 'Great axe'))


while g.running:
    g.main()
    g.game_over()

pygame.quit()
