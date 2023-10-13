import sys

    
x_scale = 7000
y_scale = 3000
h_speed_scale = 1000
v_speed_scale = 1000
rotate_scale = 180
power_scale = 5


class Lander:

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
        self.x = kargs.get('x')
        self.y = kargs.get('y')
        self.h_speed = kargs.get('h_speed')
        self.v_speed = kargs.get('v_speed')
        self.fuel = kargs.get('fuel')
        self.rotate = kargs.get('rotate')
        self.power = kargs.get('power')

    def update(self, **kwargs):
        for cle, valeur in kwargs.items():
            if hasattr(self, cle):
                setattr(self, cle, valeur)
            else:
                print(f"Attention : Le champ '{cle}' n'existe pas dans la classe.", file=sys.stderr)

    def __str__(self):
        try:
            return f"{self.x} {self.y} {self.h_speed} {self.v_speed} {self.fuel} {self.rotate} {self.power}"
        except AttributeError :
            return "lander not yiet initialized"
        
    def get_state(self):
        return [self.x, self.y, self.h_speed, self.v_speed, self.fuel, self.rotate, self.power]


    def __eq__(self, other) -> bool:
        for self_attr, other_attr in zip(vars(self).values(), vars(other).values()):
            if not round(self_attr) == round(other_attr):
                return False
        return True

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)
        
    def copy(self, other):
        """Copy other into self"""
        self.update(
            other.x,
            other.y,
            other.h_speed, 
            other.v_speed, 
            other.fuel, 
            other.rotate, 
            other.power
        )
        
    def update(self, x, y, h_speed, v_speed, fuel, rotate, power):
        """Update the caracteristics of the lander"""
        self.x = x
        self.y = y
        self.h_speed = h_speed
        self.v_speed = v_speed
        self.fuel = fuel
        self.rotate = rotate
        self.power = power
