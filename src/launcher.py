import json
import os
import sys

from environment.environment import Environement
from environment.surface import Surface
from utils.utils import load_map
from gui.gui_sr import Gui
from gui.gui_trajectory import GuiTrajectory
from maps.map_path import FLAT_SURFACE, LEVEL_ONE, CAVE_REVERSED

from solutions.examples.solution_fall import SolutionFall
from solutions.genetic.genetic_algorithm import GeneticAlgorithm

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def main():
    points, initial_state = load_map(LEVEL_ONE)
    # with open(map_path, "r") as json_file:
    #     map = json.load(json_file)

    # points = map.get('points')
    # initial_state = map.get('lander_state')

    surface = Surface(points)
    environment = Environement(surface, initial_state)
    solution = GeneticAlgorithm(environment)
    print(solution.best_chromosome)
    gui = GuiTrajectory(environment, solution)
    gui.run()

if __name__ == "__main__":
    main()