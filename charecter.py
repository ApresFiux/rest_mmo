import random

class Character:
    def __init__(self, hp, mp, armor, power, id, name):
        self.hp = hp
        self.armor = armor
        self.mp = mp
        self.power = power
        self.id = id
        self.name = name

    def receive_hit(self, dmg):
        temp_armor = self.armor
        while temp_armor > dmg:
            temp_armor //= 2
        dmg -= random.randint(temp_armor // 2, temp_armor)
        self.armor -= dmg // 2
        self.hp -= dmg
        if self.hp <= 0:
            return 'Character Dead'
        return dmg