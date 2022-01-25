import pygame
import pytmx
from config import *


class TiledMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth,
                                            y * self.tmxdata.tileheight))

    def make_map(self):
        temp_surface = pygame.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface


class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect, hp_bar=False):
        if hp_bar:
            return rect.move(self.camera.topleft[0], self.camera.topleft[1] - 10)
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(WIN_WIDTH / 2)
        y = -target.rect.centery + int(WIN_HEIGHT / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WIN_WIDTH), x)  # right
        y = max(-(self.height - WIN_HEIGHT), y)  # bottom
        self.camera = pygame.Rect(x, y, self.width, self.height)
