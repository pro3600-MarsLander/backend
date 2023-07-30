import unittest
import json

from src.tools.point import Point
from src.tools.segment import Segment
from src.environment.surface import Surface
from src.environment.lander import Lander
from src.environment.environment import Environement
from src.environment.action import Action



class TestEnvironment(unittest.TestCase):

    def test_dynamic(self):
        with open("./data/surfaces/level_one_cg.json", "r") as json_file:
            initial_parameters = json.load(json_file) 
        points = initial_parameters.get('points')
        surface = Surface(list(map(lambda point: Point(*point), points)))
        initial_state = initial_parameters.get('lander_state')
        test_lander = Lander(**initial_parameters.get('lander_state'))        

        environment = Environement(surface, initial_state)

        with open('./test/data/free_fall_level_one.jsonl', 'r') as result_file:
            states = []
            for json_state in result_file:
                states.append(json.loads(json_state))

        for state in states:
            print(state, type(state))
            test_lander.update(**state)
            environment.step(rotate=0, power=0)
            self.assertEqual(environment.lander, test_lander)
