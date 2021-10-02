import csv
import random
from dataclasses import dataclass
from typing import List


@dataclass
class food:
    name: str
    health: int
    hapiness: int
    # image: str #TODO


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
            results.append(food(row[0], row[1], row[2]))
    return results


def test():
    backend = Backend("food.csv")
    print(backend.get_food())


if __name__ == '__main__':
    test()
