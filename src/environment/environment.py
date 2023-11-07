import math

from environment.surface import Surface
from environment.entities.lander import Lander
from environment.action import Action
from environment.utils.constants import MARS_GRAVITY, X_SCALE, Y_SCALE, ROTATE_SCALE, POWER_SCALE


class Environement:
    """ Environment of the Mars lander puzzle of CodinGames"""

    surface : Surface
    lander : Lander

    def __init__(self, surface : list, initial_state):
        self.surface = surface
        self.initial_state = initial_state
        self.lander = Lander(**initial_state)


    def __str__(self) -> str:
        #return "\n".join([score_info,coord_info,speed_info,rotate_info,fuel_info])
        return str(self.lander)

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __eq__(self, other) -> bool:
        
        return  self.surface == other.surface and\
                self.initial_state == other.initial_state and \
                self.lander == other.lander
 
    def reset(self):
        """Reset the lander"""
        self.lander.update(*self.initial_state)

    def exit_zone(self) -> bool:
        return not (0 <= self.lander.x < 7000 and 0 <= self.lander.y < 3000)

    def landing_on_site(self) -> bool:
        return self.surface.collision_line == self.surface.landing_site

    def landing_angle(self) -> bool:
        return self.lander.rotate == 0

    def landing_vertical_speed(self) -> bool:
        return abs(self.lander.v_speed) <= 40

    def landing_horizontal_speed(self) -> bool:
        return abs(self.lander.h_speed) <= 20

    def successful_landing(self) -> bool:
        """For a landing to be successful, the ship must:
            - land on flat ground
            - land in a vertical position (tilt angle = 0°)
            - vertical speed must be limited ( ≤ 40m/s in absolute value)
            - horizontal speed must be limited ( ≤ 20m/s in absolute value)
        """
        return (\
            self.landing_on_site() and\
            self.landing_angle() and\
            self.landing_vertical_speed() and\
            self.landing_horizontal_speed()
            )
  
    
    def next_dynamics_parameters(self, rotate, power):
        
        h_accel = - power * math.sin(rotate*math.pi/180) 
        v_accel = power * math.cos(rotate*math.pi/180) + MARS_GRAVITY   

        h_speed = self.lander.h_speed + h_accel
        v_speed = self.lander.v_speed + v_accel

        x = self.lander.x + self.lander.h_speed + h_accel/2
        y = self.lander.y + self.lander.v_speed + v_accel/2

        return x, y, h_speed, v_speed

    def step(self, action: Action) -> bool:
        """        
        -rotate is the desired rotation angle for Mars lander. 
        Please note that for each turn the actual value of the angle 
        is limited to the value of the previous turn +/- 15°.
        
        - power is the desired thrust power. 
        0 = off. 4 = maximum power. 
        Please note that for each turn the value of the actuaNl power 
        is limited to the value of the previous turn +/- 1.
        """
        
        rotate = max(-ROTATE_SCALE, min(
            ROTATE_SCALE,
            self.lander.rotate + action.rotate
        )) 

        power = max(0, min(
            POWER_SCALE,
            self.lander.power + action.power
        ))
        
        fuel = self.lander.fuel - power
        if fuel <= 0 :
            power = self.lander.fuel
            fuel = 0

        x, y, h_speed, v_speed = self.next_dynamics_parameters(rotate, power)

        self.lander.update(x=x, y=y, h_speed=h_speed, v_speed=v_speed, fuel=fuel, rotate=rotate, power=power)
        