class CharTemplate:
    def __init__(self, hp, atk):
        self.hp = hp
        self.max_hp = hp
        self.atk = atk


class Character(CharTemplate):
    def __init__(self, hp, atk, defence, level=1):
        CharTemplate.__init__(self, hp, atk)
        self.defence = defence
        self.level = level
        self.weapon = None
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
