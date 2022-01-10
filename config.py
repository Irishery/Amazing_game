import pygame

WIN_WIDTH = 640
WIN_HEIGHT = 480
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
WHITE = (255, 255, 255)

PLAYER_HIT_RECT = pygame.Rect(0, 0, 35, 35)

tilemap = [
    'BBBBBBBBBBBBBBBBBBBB',
    'B..................B',
    'B.............E....B',
    'B..................B',
    'B.....BB...........B',
    'B....B.............B',
    'B..................B',
    'B.......P..........B',
    'B..................B',
    'B.....B........B...B',
    'B....BB............B',
    'B........B..B......B',
    'B....E......B......B',
    'B..................B',
    'BBBBBBBBBBBBBBBBBBBB',

]
