import os
import sys
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.point import Point

def load_map(map_path):
    with open(map_path, "r") as json_file:
        map = json.load(json_file)
    
    point_coords = map.get('points')
    initial_state = map.get('lander_state')
    points = [Point(x, y) for x, y in point_coords]

    return points, initial_state

