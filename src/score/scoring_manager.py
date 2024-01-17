from numpy import sqrt

from environment.environment import Environement
from environment.entities.lander import Lander
from environment.surface import Surface
from environment.utils.constants import X_SCALE, Y_SCALE
from utils.point import Point
from utils.segment import Segment

from score.utils.constants import (
    SCORE_MAX_LANDING_OFF_SITE, SCORE_MIN_LANDING_ON_SITE,
    MAX_SPEED, SCORING_H_SPEED, SCORING_V_SPEED, SCORING_SPEED
)

class ScoringManager:
    """
    This class will permit to compute the score from the environments and the lander.
    """

    def landing_distance(self, surface: Surface, lander: Lander, collision_land: Segment):
        """ Compute the distance by "walke" of the collision to the landing site
        To do so, it browse the list of points that composed the map.
        If it encounters the collision point first, it starts calculating the distance from the collision point to the runway. 
        If not, it encounters the runway first and calculates the distance to the collision point.
        """
        if collision_land is None:
            return X_SCALE*Y_SCALE
        
        if collision_land == surface.landing_area:
            return 0.0

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
        """Compute the score of the distance from the landing site
        
        If it lands on it, his score will be above a certain level. 
        Otherwise it depends of the distance with a lower maximum level.
        """
        distance = self.landing_distance(
            surface=kargs.get("surface"), lander=kargs.get("lander"), collision_land=kargs.get("collision_land")
            )
        if distance == 0:
            return SCORE_MIN_LANDING_ON_SITE
        
        return max(0, round(SCORE_MAX_LANDING_OFF_SITE*(1 - abs(distance)/kargs.get("surface").length)))

    def scoring_speed(self, environment: Environement):
        """Compute speed score
        If it lands on site, it compute a score by taking vertical and horizontal speed differently

        Otherwise, it take the norm of the speed to calculate the score
        """
        if environment.landing_on_site():
            score = max(0, SCORING_V_SPEED*(1 - abs(environment.lander.v_speed)/MAX_SPEED))
            score += max(0, SCORING_H_SPEED*(1 - abs(environment.lander.h_speed)/MAX_SPEED))
        else:
            abs_speed = sqrt(environment.lander.v_speed**2 + environment.lander.h_speed**2)
            score = max(0, round(SCORING_SPEED*(1 - abs_speed/150))) # 150 : max speed estimated
            score = 0
        return score

    def compute_score(self, environment: Environement):
        """Compute the global score"""
        on_site = environment.landing_on_site()
        if on_site:
            distance_score = SCORE_MIN_LANDING_ON_SITE
        else:
            distance_score = self.scoring_distance(
                surface=environment.surface,
                lander=environment.lander,
                collision_land=environment.collision_area
            )
        speed_score = self.scoring_speed(environment)
        return distance_score + speed_score

