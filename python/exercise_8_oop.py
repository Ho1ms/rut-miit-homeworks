import random
from random import choice, randint
from functools import reduce


class Warrior:
    def __init__(
            self,
            name: str = 'Викинг',
            min_damage: int = 5,
            max_damage: int = 25,
            accuracy: float = 0.5,
            attack_speed: float = 1,
            hp: int = 100
    ):

        self.hp = hp
        self.name = name
        self.min_damage = min_damage
        self.max_damage = max_damage
        self.accuracy = accuracy
        self.attack_speed = attack_speed
        self.attack_state = 0

    def generate_damage_args(self):

        return (
            random.randint(self.min_damage, self.max_damage),
            random.random() < self.accuracy
        )

    def generate_damage(self) -> int:
        damage_args = self.generate_damage_args()
        if 0 in damage_args:
            return 0

        return reduce(lambda a, b: a * b, damage_args)

    def generate_hp_args(self):
        return (
            1,
        )

    def take_damage(self, damage):
        self.hp -= damage * reduce(lambda a, b: a * b, self.generate_hp_args())

    def do_attack(self) -> int:
        self.attack_state += self.attack_speed
        damage = 0

        while self.attack_state >= 1:
            self.attack_state -= 1
            damage += self.generate_damage()

        return damage


class Fight:
    def __init__(self, first_fighter: Warrior, second_fighter: Warrior):
        self.first_fighter = first_fighter
        self.second_fighter = second_fighter

    def fight(self) -> Warrior:
        figther_1 = self.first_fighter
        figther_2 = self.second_fighter

        while figther_1.hp > 0 and figther_2.hp > 0:
            figther_2.take_damage(figther_1.do_attack())
            figther_1.take_damage(figther_2.do_attack())

        winner = figther_1 if figther_1.hp > figther_2.hp else figther_2

        print(f'FIRST HP: {figther_1.hp}')
        print(f'SECOND HP: {figther_2.hp}\n')

        print(f'Победил {winner.name}')
        return winner


class Ninja(Warrior):

    def __init__(self, name: str = 'Ниндзя', block: float = 0.5, super_attack: float = 0.5, **kwargs):
        self.block = block
        self.super_attack = super_attack
        super().__init__(name, **kwargs)

    def generate_hp_args(self):
        return not(random.random() < self.block),

    def generate_damage_args(self):
        return (
            random.randint(self.min_damage, self.max_damage),
            random.random() < self.accuracy,
            (random.random() < self.super_attack) * 2 or 1
        )


Danila = Ninja(name='Даня', min_damage=20, max_damage=50, accuracy=1.0,
               attack_speed=0.6, hp=100, block=1, super_attack=0)

Alexander = Warrior(name='Саня', min_damage=30, max_damage=60, accuracy=1.0, attack_speed=0.5, hp=100)

figth = Fight(Danila, Alexander)
figth.fight()
