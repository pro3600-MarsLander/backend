import unittest


from src.utils.point import Point   
from src.utils.segment import Segment

class TestUtils(unittest.TestCase):

    def test_point(self):
        point = Point(1, 2)
        self.assertEqual(point.x, 1)
        self.assertEqual(point.y, 2)
        self.assertEqual(point, Point(1, 2))
        self.assertEqual(point, [1, 2])

    def test_segment(self):
        segment = Segment([1, 2], [3, 4])
        self.assertEqual(segment.point_a, Point(1, 2))
        self.assertEqual(segment.point_b, Point(3, 4))
        self.assertEqual(segment, Segment([1, 2], [3, 4]))
        self.assertEqual(segment, [Point(1, 2), Point(3, 4)])

        self.assertEqual(segment[0], Point(1, 2))   
        self.assertTrue(Point(1, 2) in segment)
        
        self.assertEqual(segment.lenght(), 2.8284271247461903)
        self.assertTrue(segment.collision(Segment([2, 2], [2, 3])))
        self.assertFalse(segment.collision(Segment([2, 2], [2, 1])))
        
        