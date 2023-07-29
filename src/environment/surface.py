from src.tools.point import Point
from src.tools.segment import Segment

class Surface:
    lands : list[Segment]
    landing_area : Segment

    def __init__(self, points: list[Point]):
        self.lands = []
        for i in range(len(self.points)-1):
            self.lands.append(Segment(points[i], points[i+1]))
            if self.points[i].y == self.points[i+1].y:
                self.landing_area = [self.points[i], self.points[i+1]]
                

    def is_landing_area(self, segment):
        return segment.point_a.y == segment.point_b.y

    def they_collide(self, trajectoire: Segment) -> bool:
        for land in self.lands:
            if trajectoire.collision(land):
                return land
        return None
    
    

