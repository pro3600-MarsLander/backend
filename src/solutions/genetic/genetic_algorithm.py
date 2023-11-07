from enum import Enum

from environment.environment import Environement

from score.scoring_manager import ScoringManager

from solutions.abstract_solution import AbstractSolution

from solutions.genetic.population import Population
from solutions.genetic.chromosomes.abstract_chromosome import AbstractChromosome
from solutions.genetic.chromosomes.action_chromosome import ActionChromosome
from solutions.genetic.genes.action_gene import ActionGene
from solutions.genetic.utils.constants import POPULATION_SIZE, CHROMOSOME_SIZE, MAXIMUM_EPOCH



class AlgoType(Enum):
    ACTION = 1

    def get_chromosome_type(algo_type: int):
        if algo_type == 1:
            return ActionChromosome
        
    def get_gene_type(algo_type: int):
        if algo_type == 1:
            return ActionGene


class GeneticAlgorithm(AbstractSolution):
    def __init__(self, 
                population_size: int = POPULATION_SIZE, 
                chromosome_size: int = CHROMOSOME_SIZE
                ):
        self.population_size = population_size
        self.chromosome_size = chromosome_size
        self.algo_type = AlgoType.ACTION
        self.population = Population.generator(
            population_size=population_size,
            chromosome_type=AlgoType.get_chromosome_type(self.algo_type)
        )
        self.epoch = 0
        self.best_chromosome : AbstractChromosome = None
        self.scoring_manager = ScoringManager()
        self.evolution()

    def get_parameters(self) -> dict:
        return {
            "Population size": self.population_size,
            "Chromosome size": self.chromosome_size,
            "Epoch number" : self.epoch
        }
    
    def use(self, environment: Environement):
        action = self.best_chromosome.use()
        return action
    
    def evolution(self, environment: Environement):
        while self.epoch<MAXIMUM_EPOCH and not done:
            done = self.one_evolution(environment)
            self.epoch +=1
            

    def one_evolution(self, environment: Environement):
        if self.epoch == MAXIMUM_EPOCH:
            raise Exception("The maximum epoch has been reached")
        self.population.reset()
        for chromosome_index in range(self.population_size):
            done = False
            while not done:
                action = self.population.chromosomes[chromosome_index].use()
                done = environment.step(action)
            if environment.successful_landing():
                self.best_chromosome = self.population.chromosomes[chromosome_index]
                self.best_chromosome.reset()
                return True
            score = self.scoring_manager.compute_score(environment)
            self.population.set_score(chromosome_index, score)
            environment.reset()

        self.best_chromosome = self.population.evolution()
        self.population.reset()
        return False

