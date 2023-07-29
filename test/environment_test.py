import unittest
import json

from src.tools.point import Point
from src.tools.segment import Segment
from src.environment.surface import Surface
from src.environment.lander import Lander
from src.environment.environment import Environement

class TestEnvironment(unittest.TestCase):

    def test_dynamic_fall(self):
        with open("./data/surfaces/flat_surface.json", "r") as json_file:
            initial_parameters = json.load(json_file) 
            points = initial_parameters.get('points')
            surface = Surface(list(map(lambda point: Point(*point), points)))
            lander = Lander()
            environment = Environement(surface, lander)

                    


         