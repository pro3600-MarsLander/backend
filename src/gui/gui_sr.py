##
#%%  



import pygame
import os
import sys
import time

from environment.environment import Environment
from environment.surface import Surface
from environment.entities.lander import Lander
from environment.utils.constants import X_SCALE, Y_SCALE

from solutions.abstract_solution import AbstractSolution
from solutions.manual.manual_solution import ManualSolution 
from solutions.genetic.genetic_solution import GeneticSolution

from utils.point import Point
from utils.segment import Segment

from gui.utils.constants import WINDOW_HEIGHT, WINDOW_WIDTH, FRAMES_PER_SECOND, WHITE, BLACK, BLUE, RED, GREEN, LANDERS_PATH
from gui.log import manual_gui_log, trajectory_gui_log

fx = lambda x : int(WINDOW_WIDTH * x / X_SCALE)
fy = lambda y : WINDOW_HEIGHT - int(WINDOW_HEIGHT * y / Y_SCALE)

lander_image_path = os.path.join(LANDERS_PATH, 'lander_0.png')

class Gui:

    def __init__(self, environment: Environment, solution : AbstractSolution):
        """Graphic User Interface
        Manage the graphics of the simulation
        
        Fields :
            * environment : Environment
            * solution : Solution
            * display : pygame.display
            * font : pygame.Font
        
        """
        self.environment = environment
        self.solution = solution
        self.env_iterator = 0
        if isinstance(solution, ManualSolution):
            print(manual_gui_log, file=sys.stderr)
        elif isinstance(solution, GeneticSolution):
            print(trajectory_gui_log, file=sys.stderr)
        # PYGAME INITIALIZER
        pygame.init()
        self.display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.font = pygame.font.Font(None, 36)
        self.lander_image = pygame.image.load(lander_image_path)

    def screen_reset(self):
        """Draw the environment"""
        self.display.fill(BLACK)
        self.draw_surface()
        
    def reset(self):
        """Reset all the environments"""
        self.environment.reset()
        self.trajectory = []

    def display_text(self, text, position):
        """Draw text on the screen at the position position."""
        id_text = self.font.render(text, True, (255, 255, 255))
        self.display.blit(id_text, position)

    def render_reset(self):  
        """Reset the render"""
        self.env_iterator +=1
        self.screen_reset()

    def draw_surface(self):
        """Draw all the segments that composed the surface"""
        surface : Surface= self.environment.surface
        for line in surface.lands:
            pygame.draw.line(
                self.display, 
                RED, 
                [fx(line.point_a.x), fy(line.point_a.y)],
                [fx(line.point_b.x), fy(line.point_b.y)]
            )

    # def draw_lander(self, lander: Lander):
    #     rotated_image = pygame.transform.rotate(self.lander_image, lander.rotate)
    #     new_rect = rotated_image.get_rect(center = self.lander_image.get_rect(center = (lander.x, lander.y)).center)
        
    #     self.display.blit(rotated_image, new_rect)

    # def draw_lander(self, lander: Lander):
    #     rotated_image = pygame.transform.rotate(self.lander_image, lander.rotate)
    #     new_rect = rotated_image.get_rect(center=self.lander_image.get_rect(center=(lander.x, lander.y)).center)

    #     surface = pygame.Surface((15 * 2, 15 * 2), pygame.SRCALPHA)
    #     surface.blit(rotated_image, new_rect)

    #     self.display.blit(surface, (lander.x - 15, lander.y - 15))

    def draw_lander(self, lander):
        """Draw the spaceship. It is represented here by a circle"""
        pygame.draw.circle(self.display, WHITE, (fx(int(lander.x)), fy(int(lander.y))), 15)
        

    def write_parameters(self, lander: Lander):
        """Draw the states of the lander"""
        self.display_text(
            "Parameters : ",
            (80, 100)
        )
        self.display_text(
            "Coordonates : ({}, {})".format(int(lander.x), int(lander.y)),
            (100, 130)
        )
        self.display_text(
            "Velocity : ({}, {})".format(int(lander.v_speed), int(lander.h_speed)),
            (100, 160)
        )
        self.display_text(
            "Power, angle : {}, {}".format(lander.power, lander.rotate),
            (100, 190)
        )
        self.display_text(
            "Fuel : {}".format(lander.fuel),
            (100, 220)
        )
        
    def step(self, dt=1):    
        """Compute an environment step"""    
        action = self.solution.use(environment = self.environment)
        done = self.environment.step(action, dt)
        lander_position = (fx(self.environment.lander.x), fy(self.environment.lander.y))
        self.trajectory.append(lander_position)
        #pygame.transform.rotate(self.lander_image,self.rotate)
        # pygame.draw.line(self.display, WHITE, lander_position, lander_position)
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
    
      
    def pygame_step(self, success):
        """Compute the pygame step"""
        self.write_parameters(self.environment.lander)
        self.draw_lander(self.environment.lander)

        def quit_gui():
            pygame.display.quit()
            pygame.quit()
            sys.exit()


        for event in pygame.event.get():
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


        pygame.display.flip()
        self.render_reset()

        
        # self.display_text(
        #     "Parameters : ",
        #     (400, 100)
        # )

        # for order, (name, value) in enumerate(self.solution.get_parameters().items()):
        #     self.display_text(
        #         f"{name} : {value}",
        #         (400, 130 + order*30)
        #     )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()

    def run(self):
        """Run the simulation"""
        done = False
        self.reset()
        self.render_reset()
        while not done:
            done = self.step(1/FRAMES_PER_SECOND)
            self.pygame_step(done)
            time.sleep(1/FRAMES_PER_SECOND)


