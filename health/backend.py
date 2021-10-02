import csv
import enum
import math
import random
from dataclasses import dataclass, field
from typing import List, Union
import arcade
from PIL import Image


class food(arcade.Sprite):
    name: str
    health: int
    happiness: int
    image_file: str

    def __init__(self, line: List[str]):
        self.name = line[0]
        self.health = int(line[1])
        self.happiness = int(line[2])
        self.image_file = line[3]
        scale = 100 / Image.open(f"health/imgs/{self.image_file}").size[0]
        super().__init__(f"health/imgs/{self.image_file}", scale=scale, hit_box_algorithm="Detailed")

class HEALTH(enum.Enum):
    SAD = 1
    OK = 2
    HAPPY = 3


class player(arcade.Sprite):
    happiness: int = 7
    health: int = 7
    HAPPINESS_LOSS: int = 5
    HEALTH_LOSS: int = 15
    image_file: str = "banana.gif"

    def __init__(self):
        super().__init__(f"health/imgs/{self.image_file}")

    def eatFood(self, food: food):
        self.happiness = min(self.happiness + food.happiness - self.HAPPINESS_LOSS, 10)
        self.health += food.health

    def endDay(self) -> HEALTH:
        self.health -= self.HEALTH_LOSS
        health = self.health + random.randint(-1, 1)
        if health < 4:
            return HEALTH.SAD
        elif health < 7:
            return HEALTH.OK
        else:
            return HEALTH.HAPPY


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
