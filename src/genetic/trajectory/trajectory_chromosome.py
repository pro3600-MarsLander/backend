import random
from src.environment.action import Action
from src.genetic.gene import Gene
from src.environment.action import Action

class TrajectoryChromosome:
    genes : list[Action] = []
    score : float | int = 0

    def __init__(self):
        self.index = 0

    @staticmethod
    def get_score(chromosome):
        return chromosome.score

    def use(self, **kargs) -> Action:
        self.index+=1
        if self.index > len(self.genes):
            return 
        return self.genes[self.index-1]

    def mutation(self, mutation_probability):
        if random.random() > mutation_probability:
            return
        