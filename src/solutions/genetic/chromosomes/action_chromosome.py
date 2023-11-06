import random
from solutions.genetic.chromosomes.abstract_chromosome import AbstractChromosome
from solutions.genetic.genes.action_gene import ActionGene
from solutions.genetic.utils.constants import CHROMOSOME_MUTATION_PROBABILITY

class ActionChromosome(AbstractChromosome):

    def __init__(self, genes_: list(ActionGene)):
        super().__init__(genes_=genes_)

    @staticmethod
    def generator(gene_number: int):        
        genes = [ActionChromosome.generator() for _ in range(gene_number)]
        return ActionChromosome(genes_=genes)


    def mutate(self):
        for gene in self.genes:
            if random.random() < CHROMOSOME_MUTATION_PROBABILITY:
                gene.mutate()

    def use(self, iteration: int):
        return self.
    