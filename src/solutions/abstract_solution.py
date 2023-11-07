from abc import abstractmethod

from environment.action import Action
class AbstractSolution:
    
    @property
    def get_parameters(self) -> dict:
        pass

    @abstractmethod
    def use(self, environment) -> Action:
        pass