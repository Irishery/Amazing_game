quests = {
    'Скелеты'
}


class Entity:
    def __init__(self, hp, atk):
        self.hp = hp
        self.max_hp = hp
        self.atk = atk


class Character(Entity):
    def __init__(self, hp, atk, defence, level=1):
        Entity.__init__(self, hp, atk)
        self.defence = defence
        self.level = level
        self.weapon = None
        self.quest = None
        self.kills = 0
        self.armor = {
            "head": None,
            "chest": None,
            "acc": None,
            "shield": None
        }

    def addHp(self, amount):
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def equip_weapon(self, weapon):
        if self.weapon:
            self.unequip_weapon()

        self.weapon = weapon
        self.atk += weapon.atk

    def unequip_weapon(self):
        if self.weapon:
            self.atk -= self.weapon.atk
            self.weapon = None

    def equip_armor(self, armor, slot):
        if self.armor[slot]:
            self.unequip_armor(slot)

        self.armor[slot] = armor
        self.defence += armor.defence

    def uneqip_armor(self, slot):
        if self.armor[slot]:
            self.defence -= self.armor[slot].defence
            self.armor[slot] = None


class Enemy(Entity):
    def __init__(self, hp, atk):
        Entity.__init__(self, hp, atk)


class NPC:
    def __init__(self, name, avatar=None):
        self.name = name
        self.avatar = None
        self.quest = None

        self.dialog_stage = 0

    def get_vars(self):
        pass

    def get_quest(self):
        pass

    def reaction(self, phrase):
        pass


class Bob(NPC):
    def __init__(self, name, game, avatar=None):
        NPC.__init__(self, name=name, avatar=avatar)
        self.intro = 'Приветсвую тебя, странник'
        self.ch_loc = 'Куда ты хочешь отправиться?'
        self.kills = 0
        self.game = game

    def get_vars(self):
        if self.dialog_stage == 0:
            if self.quest:
                return {
                    '0': self.intro,
                    '49': 'Кто я?',
                    '50': 'Где я?',
                    '51': 'Что мне делать?',
                    '52': "Хочу отправиться в другую локацию",
                    '53': self.get_quest()
                }
            return {
                '0': self.intro,
                '49': 'Кто я?',
                '50': 'Где я?',
                '51': 'Что мне делать?',
                '52': "Хочу отправиться в другую локацию"
            }
        elif self.dialog_stage == 1:
            return {
                '0': self.ch_loc,
                '49': 'В лес',
                '50': 'В подземелье',
                '51': 'Уже не хочу'
            }

    def check_quests_completion(self, quest):
        if quest == 'скелеты':
            if self.kills >= 3:
                self.kills = 0
                return True
            return False

    def get_quest(self):
        if self.quest:
            if self.quest == 'Скелеты':
                return 'Я убил скелетов'

    def reaction(self, phrase):
        if self.dialog_stage == 0:
            return self.stage_zero(phrase)
        elif self.dialog_stage == 1:
            return self.choosing_location(phrase)

    def stage_zero(self, phrase):
        if phrase == 'Где я?':
            return 'Подумай'
        elif phrase == 'Кто я?':
            return 'Монах'
        elif phrase == 'Что мне делать?':
            self.quest = 'Скелеты'
            return 'Иди в лес и убей трёх скелетов'
        elif phrase == 'Хочу отправиться в другую локацию':
            self.dialog_stage = 1

        if phrase == 'Я убил скелетов':
            if self.check_quests_completion('скелеты'):
                self.quest = None
                return 'Благослави тебя священный \nлетающий макаронный монстр'
            return 'Ты убил недостаточно'

    def choosing_location(self, phrase):
        if phrase == 'В лес':
            print("Ну лесник получается")
            self.game.current_map = 'forest'
            self.game.dialog.is_open = False
            self.game.change_loc()
        elif phrase == 'В подземелье':
            self.game.current_map = 'dungeon'
            self.game.dialog.is_open = False
            self.game.change_loc()
            print("Ну любитель полземелий получается")
        elif phrase == 'Уже не хочу':
            self.dialog_stage = 0
