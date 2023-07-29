from src.tools.point import Point
from src.tools.segment import Segment

class Surface:
    lands : list[Segment]
    landing_area : Segment

    def __init__(self, points: list[Point]):
        self.lands = []
        for i in range(len(points)-1):
            self.lands.append(Segment(points[i], points[i+1]))
            if points[i].y == points[i+1].y:
                self.landing_area = [points[i], points[i+1]]
                

    def is_landing_area(self, segment):
        if segment:
            return segment.point_a.y == segment.point_b.y
        return False
    

    def they_collide(self, trajectory: Segment) -> bool:
        for land in self.lands:
            if trajectory.collision(land):
                return land
        return None
    
    

