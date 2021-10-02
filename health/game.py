import sys
from typing import Union, List

import pygame
from health import backend
from pygame.surface import SurfaceType

black = 0, 0, 0
pygame.init()
FOOD_FILE = "health/data/food.csv"
backend = backend.Backend(FOOD_FILE)
screen = pygame.display.set_mode()


def presnt_choice(choices: List[Union[pygame.Surface, SurfaceType]], screen) -> int:
    for choice in choices:
        screen.blit(choice, choice.get_rect())
    return 4  # True random


while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    screen.fill(black)
    presnt_choice([food.game_object for food in backend.get_food()], screen)
    pygame.display.flip()
