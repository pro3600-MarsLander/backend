import random
from environment.action import Action
from solutions.genetic.chromosomes.abstract_chromosome import AbstractChromosome
from solutions.genetic.genes.action_gene import ActionGene
from solutions.genetic.utils.constants import CHROMOSOME_MUTATION_PROBABILITY


class ActionChromosome(AbstractChromosome):

    def __init__(self, genes_: list[ActionGene], identifier: int = 0):
        super().__init__(genes_=genes_, identifier=identifier)
        self.iterator = 0

    def __iter__(self):
        return iter(self.genes)
    
    def __next__(self):
        return next(self)

    @staticmethod
    def generator(identifier: int, chromosome_size: int):    
        genes = [ActionGene.generator() for _ in range(chromosome_size)]
        return ActionChromosome(identifier=identifier, genes_=genes)
    
    @property
    def get_lenght(self):
        return len(self.genes)

    def mutate(self):
        for gene in self.genes:
            if random.random() < CHROMOSOME_MUTATION_PROBABILITY:
                gene.mutate()

    def reset(self):
        self.iterator = 0

    def use(self):
        if self.iterator >= self.get_lenght:
            return Action(0, 0)
        action = self.genes[self.iterator]
        self.iterator +=1
        return action
    
    def crossover(self,other):
        random_percent = random.random()
        child0,child1 = [], []

        for g0,g1 in zip(self, other):
            rotate0 = round(random_percent * g0.rotate + (1-random_percent) * g1.rotate)
            rotate1 = round(random_percent * g1.rotate + (1-random_percent) * g0.rotate)
            power0 = round(random_percent * g0.power + (1-random_percent) * g1.power)
            power1 = round(random_percent * g1.power + (1-random_percent) * g0.power)
            child0.append(ActionGene(power=power0, rotate=rotate0))
            child1.append(ActionGene(power=power1, rotate=rotate1))

        return ActionChromosome(child0), ActionChromosome(child1)
    