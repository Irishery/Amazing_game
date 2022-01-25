import pygame

WIN_WIDTH = 1000
WIN_HEIGHT = 1000
TILESIZE = 32
FPS = 60

PLAYER_LAYER = 4
ENEMY_LAYER = 3
BLOCK_LAYER = 2
GROUND_LAYER = 1

PLAYER_SPEED = 2
ENEMY_SPEED = 1

RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

PLAYER_HIT_RECT = pygame.Rect(0, 0, 35, 35)

LOCATIONS = {
    'lobby': 'map_sprites2/map1.tmx',
    'dungeon': 'map_sprites2/map_indoors.tmx',
    'forest': 'map_sprites(forest)/forest.tmx'
}
