import unittest
import numpy as np
import json
from src.environment.surface import Surface 
from src.environment.entities.lander import Lander
from src.environment.environment import Environment
from src.environment.action import Action
from src.environment.utils.constants import X_SCALE, Y_SCALE
from src.score.scoring_manager import ScoringManager
from src.score.utils.constants import (
    SCORE_MAX_LANDING_OFF_SITE, SCORE_MIN_LANDING_ON_SITE
)                                       
from src.utils.segment import Segment,Point


free_fall_level_one = [[2500, 2500, 0, 0, 500, 0, 0], [2500, 2498, 0, -4, 500, 0, 0], [2500, 2493, 0, -7, 500, 0, 0], [2500, 2483, 0, -11, 500, 0, 0], [2500, 2470, 0, -15, 500, 0, 0], [2500, 2454, 0, -19, 500, 0, 0], [2500, 2433, 0, -22, 500, 0, 0], [2500, 2409, 0, -26, 500, 0, 0], [2500, 2381, 0, -30, 500, 0, 0], [2500, 2350, 0, -33, 500, 0, 0], [2500, 2314, 0, -37, 500, 0, 0], [2500, 2275, 0, -41, 500, 0, 0], [2500, 2233, 0, -45, 500, 0, 0], [2500, 2186, 0, -48, 500, 0, 0], [2500, 2136, 0, -52, 500, 0, 0], [2500, 2083, 0, -56, 500, 0, 0], [2500, 2025, 0, -59, 500, 0, 0], [2500, 1964, 0, -63, 500, 0, 0], [2500, 1899, 0, -67, 500, 0, 0], [2500, 1830, 0, -71, 500, 0, 0], [2500, 1758, 0, -74, 500, 0, 0], [2500, 1682, 0, -78, 500, 0, 0], [2500, 1602, 0, -82, 500, 0, 0], [2500, 1518, 0, -85, 500, 0, 0], [2500, 1431, 0, -89, 500, 0, 0], [2500, 1340, 0, -93, 500, 0, 0], [2500, 1246, 0, -96, 500, 0, 0], [2500, 1147, 0, -100, 500, 0, 0], [2500, 1045, 0, -104, 500, 0, 0], [2500, 940, 0, -108, 500, 0, 0], [2500, 830, 0, -111, 500, 0, 0], [2500, 717, 0, -115, 500, 0, 0], [2500, 600, 0, -119, 500, 0, 0], [2500, 479, 0, -122, 500, 0, 0], [2500, 355, 0, -126, 500, 0, 0], [2500, 227, 0, -130, 500, 0, 0]]

flat_surface = Surface([[0, 1000], [X_SCALE, 1000]])
flat_land = Segment((0, 1000), (X_SCALE, 1000))

plateau_surface = Surface([[0, 0], [X_SCALE/3, 1000], [2*X_SCALE/3, 1000], [X_SCALE, 0]])
slope_land = Segment((0, 0), (X_SCALE/3, 1000))
p = np.array([X_SCALE/3, 1000])
"""
Shape of plateau_surface
       _____________
      /
     /
    /
"""

##
#%%%

##
#%%


static_lander = Lander(x=3500, y=2000, h_speed=0, v_speed=0, fuel=0, rotate=0)


class TestEnvironment(unittest.TestCase):
    def test_dynamic_free_fall(self):
        with open("./data/maps/level_one_cg.json", "r") as json_file:
            initial_parameters = json.load(json_file) 
        points = initial_parameters.get('points')
        surface = Surface(list(map(lambda point: Point(*point), points)))
        initial_state = initial_parameters.get('lander_state')
        test_lander = Lander(**initial_state)        

        environment = Environment(surface, initial_state)

        with open('./data/dynamic_states/free_fall_level_one.jsonl', 'r',encoding='utf-8') as result_file:
            states = []
            for json_state in result_file:
                states.append(json.loads(json_state))
        if states[0] != initial_state:
            raise Exception("Test error : initial state is not the same as the one in the test file")

        for state in states:
            if abs(state['y'] - environment.lander.y) > 1:
                print(state['y'], environment.lander.y)
            
            for key in state.keys():
                self.assertAlmostEqual(int(getattr(environment.lander, key)), int(state[key]), delta=1)
            environment.step(Action(0, 0))

    # def test_dynamic_power_fall(self):
    #     with open("./data/maps/level_one_cg.json", "r") as json_file:
    #         initial_parameters = json.load(json_file) 
    #     points = initial_parameters.get('points')
    #     surface = Surface(list(map(lambda point: Point(*point), points)))
    #     initial_state = initial_parameters.get('lander_state')
    #     test_lander = Lander(**initial_parameters.get('lander_state'))        

    #     environment = Environment(surface, initial_state)
    #     actions = [Action(0, 1), Action(0, 2)] + [Action(0, 3)]*100
    #     with open('./data/dynamic_states/power_fall_level_one.jsonl', 'r') as result_file:
    #         states = []
    #         for json_state in result_file:
    #             states.append(json.loads(json_state))
    #     for action, state in zip(actions, states):
    #         test_lander.update(**state)
    #         environment.step(action)
    #         self.assertEqual(environment.lander, test_lander)

    def test_collision(self):
        with open("./data/maps/flat_surface.json", "r") as json_file:
            flat_surface = json.load(json_file)

        surface = Surface(list(map(lambda point: Point(*point), flat_surface.get('points'))))
        lander_initial_state = flat_surface.get('lander_state')
        map_y = surface.landing_area[0].y
        lander_initial_state['y'] = map_y + 1
        environment = Environment(surface, lander_initial_state)
        
        # Collision : 
        environment.lander.update(h_speed = -10)
        environment.step(Action(0, 0))
        self.assertTrue(environment.landing_on_site())
        self.assertEqual(environment.lander.rotate, 0)
        self.assertEqual(environment.lander.power, 0)
        environment.reset()

        # Crash
        environment.lander.update(h_speed = -100)
        environment.step(Action(0, 0))
        self.assertFalse(environment.successful_landing())
        environment.reset()

        # Exit
        environment.lander.update(x=6800, y=map_y+1000, h_speed = 0, v_speed = 10000) 
        environment.step(Action(0, 0))
        self.assertFalse(environment.landing_on_site())
        self.assertTrue(environment.exit_zone())
        