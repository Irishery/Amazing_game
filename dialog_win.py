import pygame
from entities_templates import NPC
from config import *


class Dialog:
    def __init__(self, width, height, npc: NPC, game):
        # general
        self.npc = npc
        self.game = game
        # win sets
        self.font = pygame.font.Font('arialmt.ttf', 16)
        self.prompt_font = pygame.font.Font('arialmt.ttf', 45)
        self.width = width
        self.height = height
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill(BLACK)
        self.surf.set_alpha(200)
        self.pos_x = (WIN_WIDTH - self.width) / 2
        self.pos_y = (WIN_HEIGHT - self.height) / 2
        # avatar sets
        self.av_size = (100, 100)
        self.as_pos = (15, 15)
        self.avatar = pygame.image.load('NPCs/Bob.png')
        # win statements
        self.is_open = False

    def daccept_render(self):
        text = self.font.render(f"'F' - начать диалог", True, WHITE)
        self.game.screen.blit(text, (self.game.player.rect.x, self.game.player.rect.y))

    def clear_surface(self):
        self.game.draw()
        self.surf.fill(BLACK)

    def render_dwin(self, screen, phrase=None):
        self.surf.blit(self.avatar, self.as_pos)
        props = self.npc.get_vars()

        for num, prop in enumerate(props.keys()):
            if phrase:
                for num, line in enumerate(phrase.split('\n')):
                    text = self.font.render(f'{line}', True, WHITE)
                    self.surf.blit(text, (135, 15 + 16 * num))
                phrase = None
            elif num == 0:
                text = self.font.render(f'{props[prop]}', True, WHITE)
                self.surf.blit(text, (135, 15))
            else:
                text = self.font.render(f'{num} - {props[prop]}', True, WHITE)
                self.surf.blit(text, (135, 75 + 20 * num))
        screen.blit(self.surf, (self.pos_x, self.pos_y))

    def render(self, screen):
        self.is_open = True

        self.render_dwin(screen)
        while self.is_open:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        self.is_open = False
                        self.clear_surface()
                    elif pygame.key.get_mods() & pygame.KMOD_CTRL:
                        if event.key < 100:
                            try:
                                answer = self.npc.reaction(self.npc.get_vars()[str(event.key)])
                                self.clear_surface()
                                self.render_dwin(self.game.screen, answer)
                            except Exception as e:
                                print(e)

            pygame.display.update()
