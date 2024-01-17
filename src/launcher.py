import json
import os
import sys

from game.menue import menue
from environment.environment import Environment
from environment.surface import Surface
from utils.utils import load_map
from gui.gui_sr import Gui
from gui.gui_trajectory import GuiTrajectory

from solutions.examples.solution_fall import SolutionFall
from solutions.genetic.genetic_solution import GeneticSolution
from solutions.manual.manual_solution import ManualSolution

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

MAP_PATH = "./data/maps/"
map_list = []
for map_json_name in os.listdir(MAP_PATH):
    map_path = os.path.join(MAP_PATH, map_json_name)
    with open(map_path, "r") as json_file:
        map_dict = json.load(json_file)
        map_list.append(map_dict)


def main():
    """main function
    Launch menue, simulation, ... 
    """
    map, solution = menue(map_list)

    points, initial_state = map.get('points'), map.get('lander_state')
    surface = Surface(points)   
    environment = Environment(surface, initial_state)

    if solution == "Manual":
        solution_algorithm = ManualSolution()
        gui = Gui(environment, solution_algorithm)
    else:
        solution_algorithm = GeneticSolution(environment)
        gui = GuiTrajectory(environment, solution_algorithm)
    gui.run()

if __name__ == "__main__":
    main()