import sys

from environment.entities.entity import Entity
from environment.utils.constants import X_SCALE, Y_SCALE, H_SPEED_SCALE, V_SPACE_SCALE, ROTATE_SCALE, POWER_SCALE
    

class Lander(Entity):

    """Define the lander
    x : [0, 6999]
        Coordinate on the horizontal axe
    y : [0, 2999]
        Coordinate on the vertical axe
    h_speed : [-499, 499] 
        horizontal speed
    v_speed : [-499, 499] 
        vertical speed
    fuel : [0, 2000] 
        fuel that remains
    rotate : [-90, 90] 
        angle of the lander with 0 deg at the zenith
    power : [0, 4]
        power of the engine 
    """

    x : int
    y : int
    h_speed : float
    v_speed : float
    fuel : int
    rotate : int
    power : int
    
    def __init__(self, **kargs):
        super().__init__(**kargs)
        self.fuel = kargs.get('fuel')
        self.rotate = kargs.get('rotate')
        self.power = kargs.get('power')

    def __str__(self):
        try:
            return f"x, y: {self.x}  {self.y} | speed: {self.h_speed} {self.v_speed} | fuel, rotate, power: {self.fuel} {self.rotate} {self.power}"
        except AttributeError :
            return "lander not yiet initialized"
        
    def get_state(self):
        return [self.x, self.y, self.h_speed, self.v_speed, self.fuel, self.rotate, self.power]

        

