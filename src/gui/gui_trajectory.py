import pygame
import os
import sys
import time

from environment.environment import Environement
from environment.surface import Surface
from environment.entities.lander import Lander
from environment.utils.constants import X_SCALE, Y_SCALE

from gui.gui_sr import Gui
from gui.log import trajectory_gui_log

from solutions.abstract_solution import AbstractSolution

from utils.point import Point
from utils.segment import Segment

from maps.basic_map_1 import MAP
from gui.utils.constants import WINDOW_HEIGHT, WINDOW_WIDTH, WHITE, BLACK, BLUE, RED, GREEN

FRAMES_PER_SECOND = 2   
fx = lambda x : int(WINDOW_WIDTH * x / X_SCALE)
fy = lambda y : WINDOW_HEIGHT - int(WINDOW_HEIGHT * y / Y_SCALE)


class GuiTrajectory:
    
    def __init__(self, environment: Environement, solution : AbstractSolution):
        self.environment = environment
        self.solution = solution
        self.env_iterator = 0
        print(trajectory_gui_log, file=sys.stderr)
        # PYGAME INITIALIZER
        pygame.init()
        self.display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.font = pygame.font.Font(None, 36)
        

    def screen_reset(self):
        self.display.fill(BLACK)
        self.draw_surface()
        
    def reset(self):
        self.environment.reset()
        self.trajectories = []

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

    def draw_trajectory(self, trajectory, color, width):
        for index in range(len(trajectory)-1):
            point_a = trajectory[index]
            point_b = trajectory[index+1]
            pygame.draw.line(
                self.display,
                color,
                [fx(point_a[0]), fy(point_a[1])],
                [fx(point_b[0]), fy(point_b[1])],
                width=width
            )
            
    def step(self):        
        """
        This is a step for each evolution
        """
        done, trajectories = self.solution.one_evolution(environment=self.environment)
        #pygame.transform.rotate(self.lander_image,self.rotate)
        if done :
            self.render_reset()
            color_ = GREEN
            width_ = 5
            trajectory = trajectories[self.solution.get_index_best]
            self.draw_trajectory(trajectory, color_, width_)
        else:
            color_ = BLUE
            width_ = 1
            for trajectory in trajectories:
                self.draw_trajectory(trajectory, color_, width_)
            
        return done
    
    def draw_parameters(self):
        self.display_text(
            "Parameters : ",
            (80, 100)
        )
        for order, (name, value) in enumerate(self.solution.get_parameters().items()): # parameter = [name, value]
            self.display_text(
                f"{name} : {value}",
                (100, 130 + order*30)
            )

    def pygame_step(self, success, manual_step=True):
        def quit_gui():
            pygame.display.quit()
            pygame.quit()
            sys.exit()
        pygame.display.flip()
        pygame.event.wait()
        if manual_step:
            while True:
                event = pygame.event.wait()
                if success:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        success = False
                        break
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                        quit_gui()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        break
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    quit_gui()
        self.render_reset()
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
            self.draw_parameters()
            done = self.step()
            self.pygame_step(done)
            time.sleep(1/FRAMES_PER_SECOND)


