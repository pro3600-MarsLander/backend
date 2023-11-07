import json
import os
import sys

from environment.environment import Environement
from environment.surface import Surface
from utils.utils import load_map
from gui.gui_sr import Gui
from maps.map_path import FLAT_SURFACE, LEVEL_ONE, CAVE_REVERSED

from solutions.examples.solution_fall import SolutionFall
from solutions.genetic.genetic_algorithm import GeneticAlgorithm

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

map_path = os.path.join("data/maps", FLAT_SURFACE)

def main():
    points, initial_state = load_map(map_path)
    # with open(map_path, "r") as json_file:
    #     map = json.load(json_file)

    # points = map.get('points')
    # initial_state = map.get('lander_state')

    surface = Surface(points)
    environment = Environement(surface, initial_state)
    solution = GeneticAlgorithm()
    print(solution.best_chromosome)
    gui = Gui(environment, solution)
    gui.run()

if __name__ == "__main__":
    main()