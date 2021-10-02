import csv
import random
from dataclasses import dataclass, field
from typing import List, Union
import pygame
from pygame.surface import SurfaceType


@dataclass
class food:
    name: str
    health: int
    hapiness: int
    image_file: str  # TODO
    game_object: Union[pygame.Surface, SurfaceType] = field(init=False)

    def __post_init__(self):
        self.game_object = pygame.image.load(f"health/imgs/{self.image_file}")

    def get_rect(self):
        return self.game_object.get_rect()


class Backend:
    happiness: int = 0
    health: int = 0
    foodlist: List[food] = []
    FOOD_PER_ROUND: int = 3

    def __init__(self, foodlist):
        self.foodlist = read_food_from_file(foodlist)

    def get_food(self) -> List[food]:
        if len(self.foodlist) < self.FOOD_PER_ROUND:
            raise Exception("Not enough food objects")
        return [food for food in random.choices(self.foodlist, k=self.FOOD_PER_ROUND)]


def read_food_from_file(filename: str) -> List[food]:
    results = []
    with open(filename) as file:
        rows = csv.reader(file)
        for row in rows:
            if not row:
                break
            results.append(food(row[0], row[1], row[2], row[3]))
    return results


def test():
    backend = Backend("food.csv")
    print(backend.get_food())


if __name__ == '__main__':
    test()
