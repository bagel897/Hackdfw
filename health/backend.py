import csv
import enum
import random
from typing import List, Union
import arcade
import arcade.gui
import pygame as pygame
from PIL import Image

STARTING_EVENT = 1

FOOD_SCALE = 300
ACTION_SCALE = 300
MOTIVATION_LOSS: int = 5
HEALTH_LOSS: int = 5
FOOD_EVENTS = [1, 3, 5]
ACTION_EVENTS = [2, 4]


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
        scale = FOOD_SCALE / Image.open(f"health/imgs/FoodEvents/{self.image_file}").size[0]
        super().__init__(f"health/imgs/FoodEvents/{self.image_file}", scale=scale)


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
        self.motivation = max(min(self.motivation + food.motivation, 10), -10)
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


class action(arcade.Sprite):
    name: str
    health: int
    motivation: int
    image_file: str

    def __init__(self, line: List[str]):
        self.name = line[0]
        self.health = int(line[1])
        self.motivation = int(line[2])
        self.image_file = line[3]
        filename = f"health/imgs/NormalActionEvents/{self.image_file}"
        scale = ACTION_SCALE / Image.open(filename).size[0]
        super().__init__(filename, scale=scale)


class Backend:
    foodlist: List[food] = []
    actionList: List[action] = []
    FOOD_PER_ROUND: int = 3
    ACTIONS_PER_ROUND: int = 3

    player: player
    Day: int = 1
    Event: int = STARTING_EVENT

    def __init__(self, foodlist: str, actionList: str):
        self.foodlist = read_food_from_file(foodlist)
        self.actionList = read_actions_from_file(actionList)
        self.player = player()

    def get_events(self) -> Union[List[food], List[action]]:
        if self.Event in FOOD_EVENTS:
            if len(self.foodlist) < self.FOOD_PER_ROUND:
                raise Exception("Not enough food objects")
            return [FOOD for FOOD in random.sample(self.foodlist, k=self.FOOD_PER_ROUND)]
        elif self.Event in ACTION_EVENTS:
            if len(self.actionList) < self.ACTIONS_PER_ROUND:
                raise Exception("Not enough action objects")
            return [Action for Action in random.sample(self.actionList, k=self.ACTIONS_PER_ROUND)]
        raise Exception("Unexpected result")

    def get_player(self) -> player:
        self.player = player()
        return self.player

    def get_motivation_text(self) -> str:
        return f"Motivation: {self.player.motivation}"

    def DayEnd(self):
        self.Day += 1
        self.Event = STARTING_EVENT

    def event(self):
        if self.Event < 5:
            self.Event += 1
        else:
            self.DayEnd()

    def get_day_text(self) -> str:
        return f"Day: {self.Day}"


def read_food_from_file(filename: str) -> List[food]:
    results = []
    with open(filename) as file:
        rows = csv.reader(file)
        for row in rows:
            if not row:
                break
            results.append(food(row))
    return results


def read_actions_from_file(filename: str) -> List[action]:
    results = []
    with open(filename) as file:
        rows = csv.reader(file)
        for row in rows:
            if not row:
                break
            results.append(action(row))
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
