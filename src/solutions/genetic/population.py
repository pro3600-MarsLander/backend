import random


from solutions.genetic.chromosomes.abstract_chromosome import AbstractChromosome
from solutions.genetic.config import GRADED_RETAIN_PERCENT, NONGRADED_RETAIN_PERCENT, POPULATION_SIZE, CHROMOSOME_SIZE
from solutions.genetic.chromosomes.action_chromosome import ActionChromosome

chromosome_type=ActionChromosome

class Population:
    """Represent a population of chromosome
    This population can evolve with different function
        * Selection
        * Mutation
        * Crossover
    
    """
    chromosomes : list[AbstractChromosome]

    def __init__(self, chromosomes: list[AbstractChromosome]):
        self.chromosomes = chromosomes
        self.chromosomes_score = [0]*len(chromosomes)
        self.population_size = len(chromosomes)
        self.chromosome_size = chromosomes[0].get_length


    @staticmethod
    def generator(population_size: int=POPULATION_SIZE, chromosome_size=CHROMOSOME_SIZE, **kargs):
        
        chromosomes = [ActionChromosome.generator(identifier=identifier, chromosome_size=chromosome_size) for identifier in range(population_size)]
        return Population(chromosomes=chromosomes)
    
    @property
    def get_length(self) -> int:
        return len(self.chromosomes)
    
    def reset(self):
        for index in range(self.get_length):
            self.chromosomes[index].reset()
    
    def __iter__(self):
        return iter(self.chromosomes)
    
    def __next__(self):
        return next(self)

    def selection(self):
        """ Do the population go trought a selection process
        - Take a part of the population by the score
        - Choose in the leftover randomly some chromosome
        """

        #Extract the population sorted by score of each chromosome
        self.chromosomes.sort(
            key=lambda chromosome: chromosome.score,
            reverse=False
        )
        #Take the size_skipped best
        best_chromosome = self.chromosomes[0]
        return best_chromosome

    
    def cumulative_wheel(self, initial_index, final_index) -> GeneratorExit(list[AbstractChromosome]):
        """
        Generate with the cumulative wheel algorithm, random pair of chromosome
        """
        total_score = sum(map(lambda chromosome: chromosome.score, self.chromosomes))
        cumulative_scores = list()
        cumulative_score = 0
        for identifier in range(self.get_length):
            cumulative_score += self.chromosomes[identifier].score / total_score 
            cumulative_scores.append(cumulative_score)
            
        paired = False
        
        while initial_index < final_index:
                random_percent = min(0.999, random.random() + cumulative_scores[initial_index])
                i = initial_index
                while cumulative_scores[i] < random_percent : i+=1
                if not paired:
                    chromosome_parent0 = self.chromosomes[i]
                    paired = True
                else:
                    yield [chromosome_parent0, self.chromosomes[i]]
                    initial_index+=2
                    paired = False

    def mutate(self):
        """Create a new population by making them mutate and mixing together"""
        final_index = int(self.get_length*(1 - GRADED_RETAIN_PERCENT))
        i0, i1 = 0, 1
        new_chromosomes = []
        for parent0, parent1 in self.cumulative_wheel(0, final_index):               
            child0, child1 = parent0.crossover(parent1)
            child0.mutate()
            child1.mutate()
            new_chromosomes.append(child0)
            new_chromosomes.append(child1)

            # self.chromosomes[i0] = child0
            # self.chromosomes[i1] = child1 
            # i0 +=1
            # i1 +=1
        self.chromosomes = new_chromosomes.copy()

    def fill_with_new_chromosome(self):
        """Create new random chromosome"""
        for identifier in range(self.population_size - len(self.chromosomes)):
            self.chromosomes.append(
                ActionChromosome.generator(identifier=identifier, chromosome_size=CHROMOSOME_SIZE)
            )

    def population_switch(self):
        """Switch between two slots of population
        It have the goal to save performances. Not implemented yiet
        """
        self.chromosomes = [
            c for c in self.new_chromosomes
        ]
        self.new_chromosomes = []

    def set_score(self, index, score):
        """Set the score of a chromosome"""
        self.chromosomes[index].score += score
        # identifier = self.chromosomes[index].identifier
        # self.chromosomes_score[identifier] += score
        #self.chromosomes_score[index] += score

    def evolution(self):
        """Make the population evolve"""
        #self.generate_score()
        best_chromosome = self.selection()
        self.mutate()
        self.fill_with_new_chromosome()
        #self.population_switch()
        self.reset()
        return best_chromosome




