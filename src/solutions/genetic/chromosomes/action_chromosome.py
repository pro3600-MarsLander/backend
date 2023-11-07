import random
from solutions.genetic.chromosomes.abstract_chromosome import AbstractChromosome
from solutions.genetic.genes.action_gene import ActionGene
from solutions.genetic.utils.constants import CHROMOSOME_MUTATION_PROBABILITY

class ActionChromosome(AbstractChromosome):

    def __init__(self, genes_: list[ActionGene], identifier: int = 0):
        super().__init__(genes_=genes_, identifier=identifier)
        self.iterator = 0
    @staticmethod
    def generator(identifier: int, chromosome_size: int):    
        genes = [ActionGene.generator() for _ in range(chromosome_size)]
        return ActionChromosome(identifier=identifier, genes_=genes)


    def mutate(self):
        for gene in self.genes:
            if random.random() < CHROMOSOME_MUTATION_PROBABILITY:
                gene.mutate()

    @property
    def get_lenght(self):
        return len(self.genes)
    
    def reset(self):
        self.iterator = 0

    def use(self):
        if self.iterator >= self.get_lenght():
            return None
        action = self.genes[self.iterator]
        self.iterator +=1
        return action
    