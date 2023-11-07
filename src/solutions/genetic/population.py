import random

from solutions.genetic.chromosomes.abstract_chromosome import AbstractChromosome
from solutions.genetic.utils.constants import GRADED_RETAIN_PERCENT, NONGRADED_RETAIN_PERCENT, POPULATION_SIZE, CHROMOSOME_SIZE


class Population:
    chromosomes : list[AbstractChromosome]

    def __init__(self, chromosomes: list(AbstractChromosome)) -> None:
        self.chromosomes = chromosomes
        self.chromosomes_score = [0]*len(chromosomes)

    @staticmethod
    def generator(population_size: int=POPULATION_SIZE, chromosome_size=CHROMOSOME_SIZE, chromosome_type=AbstractChromosome):
        chromosomes = [chromosome_type.generator(identifier=identifier, chromosome_size=chromosome_size) for identifier in range(population_size)]
        return Population(chromosomes=chromosomes)
    
    @property
    def get_length(self) -> int:
        return len(self.chromosomes)
    
    def reset(self):
        for index in range(self.get_length):
            self.chromosomes_score[index] = 0
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
            key=lambda chromosome: self.scores[chromosome.identifier],
            reverse=True
        )
        #Take the size_skipped best
        best_chromosome = self.chromosomes[0]
        return best_chromosome

    
    def cumulative_wheel(self, initial_index, final_index) -> GeneratorExit(list[AbstractChromosome]):
        total_score = sum(self.chromosomes_score)
        cumulative_scores = list()
        cumulative_score = 0
        for chromosome in self:
            cumulative_score += chromosome.score / total_score 
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

    def mutation(self):
        final_index = int(self.get_length()*(1 - GRADED_RETAIN_PERCENT))
        i0, i1 = 0, 1
        for parent0, parent1 in self.cumulative_wheel(0, final_index):               
            child0, child1 = parent0.crossover(parent1)
            child0.mutation()
            child1.mutation()
            self.chromosomes[i0] = child0
            self.chromosomes[i1] = child1 
            i0 +=1
            i1 +=1

    def population_switch(self):
        self.chromosomes = [
            c for c in self.new_chromosomes
        ]
        self.new_chromosomes = []

    def set_score(self, index, score):
        self.chromosomes_score[index] += score

    def evolution(self):
        #self.generate_score()
        best_chromosome = self.selection()
        self.mutation()
        #self.population_switch()
        return best_chromosome




