import random

from src.genetic.chromosome import Chromosome

GRADED_RETAIN_PERCENT = 0.1    # percentage of retained best fitting individuals
NONGRADED_RETAIN_PERCENT = 0.2  # percentage of retained remaining individuals (randomly selected)
MUTATION_PROBABILITY = 0.01

class Population:
    chromosomes : list[Chromosome]

    def __init__(self) -> None:
        pass

    def get_length(self) -> int:
        return len(self.chromosomes)

    def selection(self):
        """ Do the population go trought a selection process
        - Take a part of the population by the score
        - Choose in the leftover randomly some chromosome
        """

        #Extract the population sorted by score of each chromosome
        self.chromosomes = list(
            sorted(self.chromosomes, key=Chromosome.get_score)
        )
        #Take the size_skipped best
        best_chromosome = self.chromosomes[-1]


        return best_chromosome

    
    def cumulative_wheel(self, initial_index, final_index) -> GeneratorExit(list[Chromosome]):
        total_score = sum(map(Chromosome.get_score, self.chromosomes))
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
            child0.mutation(MUTATION_PROBABILITY)
            child1.mutation(MUTATION_PROBABILITY)
            self.chromosomes[i0] = child0
            self.chromosomes[i1] = child1 
            i0 +=1
            i1 +=1

    def population_switch(self):
        self.chromosomes = [
            c for c in self.new_chromosomes
        ]
        self.new_chromosomes = []

    def evolution(self):
        #self.generate_score()
        best_chromosome = self.selection()
        self.mutation()
        #self.population_switch()
        return best_chromosome




