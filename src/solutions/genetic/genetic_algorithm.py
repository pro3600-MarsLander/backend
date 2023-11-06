from enum import Enum

from environment.environment import Environement

from solutions.genetic.chromosomes.action_chromosome import ActionChromosome
from solutions.genetic.genes.action_gene import ActionGene

class AlgoType(Enum):
    ACTION = 1

    def get_chromosome_type(algo_type: int):
        if algo_type == 1:
            return ActionChromosome
        
    def get_gene_type(algo_type: int):
        if algo_type == 1:
            return ActionGene

class GeneticAlgorithm:
    

    def __init__(self):
        self.algo_type = AlgoType.ACTION

