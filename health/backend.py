import csv
import enum
import random
from typing import List
import arcade
import arcade.gui
import pygame as pygame
from PIL import Image

FOOD_SCALE = 100

ACTION_SCALE = 100

MOTIVATION_LOSS: int = 5
HEALTH_LOSS: int = 5


class food(arcade.Sprite):
    name: str
    health: int
    motivation: int
    image_file: str

    def __init__(self, line: List[str]):
        self.name = line[0]
        self.health = int(line[1])
        self.motivation = int(line[2])
        self.image_file = line[3]
        scale = FOOD_SCALE / Image.open(f"health/imgs/{self.image_file}").size[0]
        super().__init__(f"health/imgs/{self.image_file}", scale=scale)


class HEALTH(enum.Enum):
    SAD = 0
    OK = 1
    HAPPY = 2


class MOTIVATION(enum.Enum):
    SAD = 0
    OK = 1
    HAPPY = 2


class player(arcade.Sprite):
    motivation: int = 7
    health: int = 7

    image_file: str = "Avatars/SelecterAvatar.jpg"

    def __init__(self):
        super().__init__(f"health/imgs/{self.image_file}")

    def eatFood(self, food: food):
        self.motivation = max(min(self.motivation + food.motivation, 10), 0)
        self.health = max(min(self.health + food.health, 10), 0)

    def getHealth(self) -> HEALTH:
        health = self.health
        if health < 4:
            return HEALTH.SAD
        elif health < 7:
            return HEALTH.OK
        else:
            return HEALTH.HAPPY

    def getSpeed(self) -> int:
        return 5 + self.health

    def getMotivation(self) -> MOTIVATION:
        motivation = self.motivation
        if motivation < 4:
            return MOTIVATION.SAD
        elif motivation < 7:
            return MOTIVATION.OK
        else:
            return MOTIVATION.HAPPY


class Backend:
    foodlist: List[food] = []
    FOOD_PER_ROUND: int = 3
    player: player

    def __init__(self, foodlist):
        self.foodlist = read_food_from_file(foodlist)
        self.player = player()

    def get_food(self) -> List[food]:
        if len(self.foodlist) < self.FOOD_PER_ROUND:
            raise Exception("Not enough food objects")
        return [FOOD for FOOD in random.sample(self.foodlist, k=self.FOOD_PER_ROUND)]

    def get_player(self) -> player:
        self.player = player()
        return self.player
    def get_text(self) -> str:
        return str(self.player.health)


def read_food_from_file(filename: str) -> List[food]:
    results = []
    with open(filename) as file:
        rows = csv.reader(file)
        for row in rows:
            if not row:
                break
            results.append(food(row))
    return results


def test():
    backend = Backend("food.csv")
    print(backend.get_food())


if __name__ == '__main__':
    test()


class healthBar:
    image_file: str
    player: player
    sprite: arcade.Sprite

    def __init__(self, player):
        self.player = player
        self.get_image()

    def get_image(self):
        Hp: int = self.player.getHealth().value
        Mp: int = self.player.getMotivation().value
        self.image_file = f"health/imgs/BarStates/Hp{Hp}Mp{Mp}.jpg"
        scale = 1 / 4
        self.sprite = arcade.Sprite(self.image_file, scale=scale)

    def get_text(self) -> str:
        return str(player.motivation)


class Action(arcade.Sprite):
    name: str
    health: int
    motivation: int
    image_file: str

    def __init__(self, line: List[str]):
        self.name = line[0]
        self.health = int(line[1])
        self.motivation = int(line[2])
        self.image_file = line[3]
        scale = ACTION_SCALE / Image.open(f"health/imgs/{self.image_file}").size[0]
        super().__init__(f"health/imgs/{self.image_file}", scale=scale)
