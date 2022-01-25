import pygame
import math

from sprites import Spritesheet
from config import WIN_HEIGHT, WIN_WIDTH, BLACK, WHITE


class InventoryItem:
    def __init__(self, img, value):
        self.img = img
        self.value = value
        self.rect: pygame.Rect

    def set_rect(self, rect):
        self.rect = rect


class Consumable(InventoryItem):
    def __init__(self, img, value, hp_gain, mp_gain):
        InventoryItem.__init__(self, img, value)
        self.hp_gain = hp_gain
        self.mp_gain = mp_gain

    def use(self, target):
        target.addHp(self.hp_gain)
        target.addMP(self.mp_gain)


class Equipable(InventoryItem):
    def __init__(self, img, value):
        InventoryItem.__init__(self, img, value)
        self.is_equipped = False
        self.equipped_to = None

    def equip(self, target):
        self.is_equipped = True
        self.equipped_to = target

    def unequip(self):
        self.is_equipped = False
        self.equipped_to = None


class Weapon(Equipable):
    def __init__(self, img, value, atk, wpn_type, name):
        Equipable.__init__(self, img, value)
        self.atk = atk
        self.wpn_type = wpn_type
        self.name = name

    def equip(self, target):
        Equipable.equip(self, target)
        target.equip_weapon(self)

    def unequip(self):
        self.equipped_to.unequip_weapon()
        Equipable.unequip(self)

    def get_info(self):
        return {
            'atk': self.atk,
            'type': self.wpn_type,
            'name': self.name
        }


class Armor(Equipable):
    def __init__(self, img, value, defence, mdef, slot, name):
        Equipable.__init__(self, img, value)
        self.defence = defence
        self.mdef = mdef
        self.slot = slot
        self.eq_type = 'armor'
        self.name = name

    def equip(self, target):
        Equipable.equip(self, target)
        target.equip_armor(self, self.slot)

    def unequip(self):
        self.equipped_to.unequip_armor(self.slot)
        Equipable.unequip(self)

    def get_info(self):
        return {
            'def': self.defence,
            'slot': self.slot,
            'type': self.eq_type,
            'name': self.name
        }


class Inventory:
    def __init__(self, hp, game):
        self.hp = hp
        self.items = [[]]
        self.game = game
        self.avatar = pygame.image.load('img/avatar.png')
        # inventory win
        self.width = 500
        self.height = 350
        # surface sets
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill(BLACK)
        self.surf.set_alpha(200)
        self.pos_x = (WIN_WIDTH - self.width) / 2
        self.pos_y = (WIN_HEIGHT - self.height) / 2
        # item sets
        self.cell_size = 50
        self.cell_size = 50
        # font
        self.font = pygame.font.Font('arialmt.ttf', 16)
        # item info texts
        self.texts = []
        # win statements
        self.invent_open = False

    def add_item(self, item):
        row = len(self.items) - 1
        if len(self.items[row]) == 5:
            if row == 2:
                return 'Inventory is full'
            self.items.append([item])
        else:
            self.items[row].append(item)

    def remove_item(self, item):
        for i, sublist in enumerate(self.items):
            if item in sublist:
                self.items[i].remove(item)
                if len(self.items[i]) == 0:
                    self.items.remove(self.items[i])

    def update_hp(self, amount):
        self.hp = amount

    # get mouse position in surf
    def get_act_pos(self, pos):
        return pos[0] - self.pos_x, pos[1] - self.pos_y

    def is_pressed(self, rect, pos, pressed):
        if rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False

    def get_cell_render(self, item, lx, ly):
        y = 15 + self.cell_size * ly + 15 * ly if ly else 15
        x = 135 + self.cell_size * lx + 15 * lx if lx else 135

        item_rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
        item.set_rect(item_rect)
        sprite = pygame.transform.scale(item.img, (50, 50))
        return sprite, (x, y)

    def get_cell(self, mouse_pos):
        cell_x = math.floor((mouse_pos[0] - 135) / self.cell_size)
        cell_y = math.floor((mouse_pos[1] - 15) / self.cell_size)

        cell_x = math.floor((mouse_pos[0] - 135 - cell_x * 15) / self.cell_size)
        cell_y = math.floor((mouse_pos[1] - 15 - cell_y * 15) / self.cell_size)
        try:
            rect = self.items[cell_y][cell_x].rect
            pressed = self.is_pressed(rect, mouse_pos, [1, 0])
            if pressed:
                return self.items[cell_y][cell_x]
            return False

        except Exception as e:
            return None

    def render_invent_win(self, screen, rend_info=False):
        self.invent_open = True
        self.surf.blit(self.avatar, (15, 15))

        for ly, sublist in enumerate(self.items):
            for lx, item in enumerate(sublist):
                item_sprite, pos = self.get_cell_render(item, lx, ly)
                self.surf.blit(item_sprite, (pos[0], pos[1]))
        if not rend_info:
            screen.blit(self.surf, (self.pos_x, self.pos_y))

    def clear_surface(self):
        self.game.draw()
        self.surf.fill(BLACK)

    def render_item_info(self, screen, item):
        props = item.get_info()

        self.clear_surface()
        self.render_invent_win(screen, rend_info=True)
        for num, prop in enumerate(props.keys()):
            text = self.font.render(f'{prop}: {props[prop]}', True, WHITE)
            self.texts.append(text)
            self.surf.blit(text, (135, 195 + 20 * num))
        screen.blit(self.surf, (self.pos_x, self.pos_y))

    def render(self, screen):
        self.render_invent_win(screen)

        self.invent_open = True

        while self.invent_open:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_i:
                        if self.invent_open:
                            self.clear_surface()
                        self.invent_open = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    mouse_pressed = pygame.mouse.get_pressed()

                    item = self.get_cell(self.get_act_pos(mouse_pos))
                    if item:
                        self.render_item_info(screen, item)

                    if not self.is_pressed(self.surf.get_rect(), self.get_act_pos(mouse_pos), mouse_pressed):
                        self.invent_open = False

            pygame.display.update()
