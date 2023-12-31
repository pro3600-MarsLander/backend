import unittest
import json

from src.utils.point import Point
from src.utils.segment import Segment
from src.environment.surface import Surface
from backend.src.environment.entities.lander import Lander
from src.environment.environment import Environement
from src.environment.action import Action



class TestEnvironment(unittest.TestCase):

    def test_dynamic_free_fall(self):
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
            test_lander.update(**state)
            environment.step(Action(0, 0))
            self.assertEqual(environment.lander, test_lander)


    def test_dynamic_power_fall(self):
        with open("./data/surfaces/level_one_cg.json", "r") as json_file:
            initial_parameters = json.load(json_file) 
        points = initial_parameters.get('points')
        surface = Surface(list(map(lambda point: Point(*point), points)))
        initial_state = initial_parameters.get('lander_state')
        test_lander = Lander(**initial_parameters.get('lander_state'))        

        environment = Environement(surface, initial_state)
        actions = [Action(0, 1), Action(0, 2)] + [Action(0, 3)]*100
        with open('./test/data/power_fall_level_one.jsonl', 'r') as result_file:
            states = []
            for json_state in result_file:
                states.append(json.loads(json_state))
        for action, state in zip(actions, states):
            test_lander.update(**state)
            environment.step(action)
            self.assertEqual(environment.lander, test_lander)
