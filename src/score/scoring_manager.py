from numpy import sqrt

from environment.environment import Environement
from environment.entities.lander import Lander
from environment.surface import Surface
from utils.point import Point
from utils.segment import Segment

from score.utils.constants import SCORE_MAX_LANDING_OFF_SITE, SCORE_MIN_LANDING_ON_SITE

class ScoringManager:
    """
    This class will permit to compute the score from the environments and the lander.
    """

    def landing_distance(self, surface: Surface, lander: Lander, collision_land: Segment):
        """ Calculate the distance by "walke" of the collision to the landing site"""
        if collision_land == surface.landing_area:
            return 0

        point_lander = Point(lander.x, lander.y)
        run = False
        distance = 0
        for point in surface.get_points():
            if not run :
                if point == collision_land.point_a: # from left to the right 
                    point_from = point
                    point_to = collision_land.point_b
                    point_final = surface.landing_area.point_a
                    distance = point_lander.distance(collision_land.point_b)
                    run = True

                elif point == surface.landing_area.point_b: # from right to the left
                    point_from = surface.landing_area.point_a
                    point_to = point
                    point_final = collision_land.point_a
                    distance = collision_land.point_a.distance(point_lander)
                    run = True
                    
            else:
                point_from, point_to = point_to, point
                distance += point_from.distance(point_to)
                if point == point_final:
                    break
        return distance
    
    
    def scoring_distance(self, **kargs):
        distance = self.landing_distance(
            surface=kargs.get("surface"), lander=kargs.get("lander"), collision_land=kargs.get("collision_land"))
        
        return round(SCORE_MAX_LANDING_OFF_SITE*(1 - abs(distance)/kargs.get("surface").length))

    def scoring_speed(self, **kargs):
        if kargs.get("on_site"):
            score = max(0, 100*(1 - abs(kargs.get("lander").v_speed)/200))
            score += max(0, 80*(1 - abs(kargs.get("lander").h_speed)/200))
        else:
            abs_speed = sqrt(kargs.get("lander").v_speed**2 + kargs.get("lander").h_speed**2)
            score = max(0, round(20*(1 - abs_speed/150))) # 150 : max speed estimated
            score = 0
        return score

    def compute_score(self, environment: Environement):
        on_site = environment.landing_on_site()
        if on_site:
            distance_score = SCORE_MIN_LANDING_ON_SITE
        else:
            distance_score = self.scoring_distance(
                surface=environment.surface,
                lander=environment.lander,
                collision_land=environment.collision_area
            )
        speed_score = self.scoring_speed(
            lander=environment.lander
        )

