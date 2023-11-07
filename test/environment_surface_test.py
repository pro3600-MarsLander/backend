##
#%%
import unittest
import json
from src.environment.surface import Surface
from src.utils.point import Point
from src.utils.segment import Segment

##
#%%

class TestEnvironmentSurface(unittest.TestCase):

    def test_collision(self):
        with open("./data/surfaces/flat_surface.json", "r") as json_file:
            points = json.load(json_file).get('points')
        surface = Surface(list(map(lambda point: Point(*point), points)))
        lander_position = Point(3500, 1010)
        
        # Collision : 
        next_lander_position = Point(3500, 990)
        trajectory = Segment(lander_position, next_lander_position)
        collision_land = surface.they_collide(trajectory)
        
        self.assertTrue(surface.is_landing_area(collision_land))

        next_lander_position = Point(3500, 1001)
        trajectory = Segment(lander_position, next_lander_position)
        collision_land = surface.they_collide(trajectory)
        self.assertIsNone(collision_land)
        self.assertFalse(surface.is_landing_area(collision_land))
            
                        


# %%
