import random

from environment.utils.constants import ACTION_POWER_SCALE, ACTION_ROTATE_SCALE
from environment.utils.utils import clamp

class Action:
    """Action of the lander
        rotate : [-15,15]
            action of rotation
        power : [-1,1]
            action of power
    """

    def __init__(self, rotate : int, power : int):
        self.rotate = clamp(rotate, -ACTION_ROTATE_SCALE, ACTION_ROTATE_SCALE)
        self.power = clamp(power, -ACTION_POWER_SCALE, ACTION_POWER_SCALE)

    def __str__(self) -> str:
        return f"{self.rotate} {self.power}"

    def __eq__(self, other) -> bool:
        return self.rotate == other.rotate and self.power == other.power

    def last_action(self, rotate):
        """Choose the best action to choose"""
        if abs(rotate) <= 15:
            self.rotate = -rotate

