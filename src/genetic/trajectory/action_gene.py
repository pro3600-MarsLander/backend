import random

from src.genetic.gene import Gene
from src.environment.action import Action

WEIGHTS_ROTATION = [1]*31
WEIGHTS_POWER = [0.1, 0.70, 0.20]


class ActionGene(Gene, Action):
    
    def mutate(self) -> None:
        return super().mutate()
    
    def mutate(self) -> None:
        """ Set up the action with random setings"""
        self.rotate = random.choices(list(range(-15, 16)), WEIGHTS_ROTATION )[0]
        self.power = random.choices([-1, 0, 1], WEIGHTS_POWER)[0]
