class Surface:
    points : list # list[Point]
    landing_area : list # Segment/Vector

    def __init__(self, points) -> bool:
        self.points = points
        for i in range(len(self.points)-1):
            if self.points[i].y == self.points[i+1].y:
                self.landing_area = [self.points[i], self.points[i+1]]
                return True
        return False


    def they_collide(self, segment) -> bool:
        pass

