import random
WEIGHTS_ROTATION = [1]*10 + [3]*11 + [1]*10

WEIGHTS_ROTATION = [1]*31
WEIGHTS_POWER = [0.1, 0.70, 0.20]

class Action:
    """Action of the lander
        rotate : [-15,15]
            action of rotation
        power : [-1,1]
            action of power
    """

    @staticmethod
    def generator():
        action = Action(0,0)
        action.mutate()
        return action

    def __init__(self, rotate : int, power : int):
        self.rotate = rotate
        self.power = power

    def __str__(self) -> str:
        return f"{self.rotate} {self.power}"

    def __eq__(self, other) -> bool:
        return self.rotate == other.rotate and self.power == other.power

    def last_action(self, rotate):
        """Choose the best action to choose"""
        if abs(rotate) <= 15:
            self.rotate = -rotate

