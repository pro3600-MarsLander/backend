from abc import abstractmethod

from environment.action import Action
class AbstractSolution:
    
    @property
    @abstractmethod
    def get_parameters(self) -> dict:
        pass

    @abstractmethod
    def use(self, **kargs) -> Action:
        """
        By given some parameters, use return the next action the lander have to make
        """
        pass