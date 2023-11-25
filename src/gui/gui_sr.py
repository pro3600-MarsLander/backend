##
#%%  



import pygame
import os
import sys
import time

from environment.environment import Environement
from environment.surface import Surface
from environment.entities.lander import Lander
from environment.utils.constants import X_SCALE, Y_SCALE

from solutions.abstract_solution import AbstractSolution

from utils.point import Point
from utils.segment import Segment

from maps.basic_map_1 import MAP
from gui.utils.constants import WINDOW_HEIGHT, WINDOW_WIDTH, FRAMES_PER_SECOND, WHITE, BLACK, BLUE, RED, GREEN


fx = lambda x : int(WINDOW_WIDTH * x / X_SCALE)
fy = lambda y : WINDOW_HEIGHT - int(WINDOW_HEIGHT * y / Y_SCALE)


class Gui:
    def __init__(self, environment: Environement, solution : AbstractSolution):
        self.environment = environment
        self.solution = solution
        self.env_iterator = 0
        # PYGAME INITIALIZER
        pygame.init()
        self.display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.font = pygame.font.Font(None, 36)

    def screen_reset(self):
        self.display.fill(BLACK)
        self.draw_surface()
        
    def reset(self):
        self.environment.reset()
        self.trajectory = []

    def display_text(self, text, position):
        id_text = self.font.render(text, True, (255, 255, 255))
        self.display.blit(id_text, position)

    def render_reset(self):        
        self.env_iterator +=1
        self.screen_reset()

    def draw_surface(self):
        surface : Surface= self.environment.surface
        border_left = surface.lands[0].point_a
        border_right = surface.lands[-1].point_b
        for line in surface.lands:
            pygame.draw.line(
                self.display, 
                RED, 
                [fx(line.point_a.x), fy(line.point_a.y)],
                [fx(line.point_b.x), fy(line.point_b.y)]
            )


    def step(self):        
        action = self.solution.use(environment = self.environment)
        done = self.environment.step(action)
        lander_position = (fx(self.environment.lander.x), fy(self.environment.lander.y))
        self.trajectory.append(lander_position)
        #pygame.transform.rotate(self.lander_image,self.rotate)
        pygame.draw.line(self.display, WHITE, lander_position, lander_position)
        if done :
            if self.environment.successful_landing():
                self.env_iterator -=1
                self.render_reset()
                color = GREEN
                width_ = 5

            else:
                color = BLUE
                width_ = 1
            start_point = self.trajectory[0]
            for end_point in self.trajectory[1:]:
                pygame.draw.line(
                    self.display, 
                    color, 
                    start_point,
                    end_point,
                    width=width_
                )
                start_point = end_point

        return done
    
      
    def pygame_step(self, success, manual_step=False):
        
        pygame.display.flip()
        pygame.event.wait()

        def quit_gui():
            pygame.display.quit()
            pygame.quit()
            sys.exit()
        if manual_step:
            while True:
                event = pygame.event.wait()
                if event.type == pygame.KEYDOWN:
                    if success:
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                            success = False
                            break
                        elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                            quit_gui()

                    else:
                        if event.key == pygame.K_RIGHT:
                            break

                        
                        
                if event.type == pygame.QUIT:
                    quit_gui()

        self.render_reset()
        self.display_text(
            "Parameters : ",
            (400, 100)
        )
        for order, (name, value) in enumerate(self.solution.get_parameters()):
            self.display_text(
                f"{name} : {value}",
                (400, 130 + order*30)
            )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()

    def run(self):
        done = False
        self.reset()
        self.render_reset()
        while not done:
            done = self.step()
            self.pygame_step(done)
            time.sleep(1/FRAMES_PER_SECOND)


