from utils.point import Point
class Segment:
    """Define a segment in space
        point_a : Point
        point_b : Point
    """
    @staticmethod
    def ccw(A : Point, B : Point, C : Point) -> bool:
        return (C.y - A.y) * (B.x - A.x) > (B.y - A.y) * (C.x - A.x)

    def __init__(self, point_a : Point, point_b : Point ):
        self.point_a = point_a
        self.point_b = point_b
    
    def __iter__(self):
        return iter([self.point_a, self.point_b])

    def __next__(self):
        return next(self)

    def __eq__(self, other) -> bool:
        return self.point_a == other.point_a and self.point_b == other.point_b

    def __str__(self) -> str:
        return f"{self.point_a} | {self.point_b}"

    def lenght(self) -> float:
        return self.point_a.distance(self.point_b)

    def collision(self, other) -> bool:
        """Look if the segment self and [other.point_a, other.point_b] segment's intersect"""
        return Segment.ccw(self.point_a, other.point_a,other.point_b) != Segment.ccw(self.point_b, other.point_a, other.point_b) \
            and Segment.ccw(self.point_a, self.point_b, other.point_a) != Segment.ccw(self.point_a, self.point_b, other.point_b)
    
    