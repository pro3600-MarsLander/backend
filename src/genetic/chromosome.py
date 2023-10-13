import random
from src.environment.action import Action
from src.genetic.gene import Gene

class Chromosome:
    genes : list[Gene] = []
    score : float | int = 0

    @staticmethod
    def get_score(chromosome):
        return chromosome.score

    def use(self, **kargs) -> Action:
        pass

    def mutation(self, mutation_probability):
        if random.random() > mutation_probability:
            return
        