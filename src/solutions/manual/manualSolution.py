import pygame
from solutions.abstract_solution import AbstractSolution
from environment.action import Action
class ManualSolution(AbstractSolution):
    @property
    @abstractmethod
    def get_parameters(self) -> dict:
        return {}

    @abstractmethod
    def use(self, environement=None) -> Action:
        """
        By given some parameters, use return the next action the lander have to make
        """
        event = pygame.event.wait()
        action = Action()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            action.rotate = 5
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            action.rotate = -5
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            action.power = 1
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            action.power = -1
            
        return action

    def set_parameters(self, **kargs):
        """
        Will be used for the settings windows on pygame
        """
        for key, value in kargs:
            self.__setattr__(key, value)

