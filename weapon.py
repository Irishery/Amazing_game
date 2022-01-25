import pygame

from inventory import Weapon
from sprites import Spritesheet


class GreatAxe(Weapon):
    def __init__(self, value=1, atk=7, wpn_type='axe', name='Great Axe'):
        sw_sprite = pygame.image.load("weapon/monochrome_sword_pack_16x16.png").convert()
        cropped_region = (0, 0, 16, 16)
        img = sw_sprite.subsurface(cropped_region)
        Weapon.__init__(self, img, value, atk, wpn_type, name)


class Ukraine(Weapon):
    def __init__(self, value=1, atk=99, wpn_type='sword', name='Ukraine'):
        sw_sprite = pygame.image.load("weapon/monochrome_sword_pack_16x16.png").convert()
        cropped_region = (0, 16, 16, 16)
        img = sw_sprite.subsurface(cropped_region)
        Weapon.__init__(self, img, value, atk, wpn_type, name)


class SmallAxe(Weapon):
    def __init__(self, img, value, atk, wpn_type, name):
        Weapon.__init__(self, img, value, atk, wpn_type, name)


class IQ(Weapon):
    def __init__(self, img, value, atk, wpn_type, name):
        Weapon.__init__(self, img, value, atk, wpn_type, name)
