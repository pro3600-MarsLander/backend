from utils.point import Point
from utils.segment import Segment

class Surface:
    lands : list[Segment]
    landing_area : Segment
    length : float

    def __init__(self, points: list[Point]):
        self.lands = []
        self.length = 0
        for i in range(len(points)-1):
            land = Segment(points[i], points[i+1])
            self.lands.append(land)
            self.length += land.lenght()
            if points[i].y == points[i+1].y:
                self.landing_area = land
                
    def is_landing_area(self, segment):
        if segment:
            return segment.point_a.y == segment.point_b.y
        return False
    

    def they_collide(self, trajectory: Segment) -> bool:
        for land in self.lands:
            if trajectory.collision(land):
                return land
        return None
    
    def get_points(self):
        yield self.lands[0].point_a
        for segment in self.lands:
            yield segment.point_b
    

