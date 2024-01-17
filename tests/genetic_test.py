import unittest
import random

from src.solutions.genetic.genetic_solution import GeneticSolution
from src.solutions.genetic.population import Population
from src.solutions.genetic.chromosomes.action_chromosome import ActionChromosome
from src.solutions.genetic.chromosomes.abstract_chromosome import AbstractChromosome
from src.solutions.genetic.genes.action_gene import ActionGene
from src.environment.environment import Environment
from src.environment.action import Action
from src.environment.entities.lander import Lander
from src.environment.surface import Surface

class TestGenetic(unittest.TestCase):
    def test_population_generator(self):
        population = Population.generator(10, 100, ActionChromosome)
        self.assertEqual(len(population), 10)
        self.assertEqual(len(population[0].genes), 100)
        self.assertEqual(len(population[0].genes), len(population[1].genes))
        self.assertNotEqual(population[0].genes, population[1].genes)
        

    def test_cumulative_wheel(self):
        population = Population.generator(10, 100, ActionChromosome)

        # Set random score
        for index in range(len(population)):
            population[index].score = random.randint(0, 400)
        population.population_sort()

        cumulative_wheel = list(population.cumulative_wheel(10))
        
        cumulative_wheel2 = list(population.cumulative_wheel2(10))
        self.assertEqual(len(cumulative_wheel), 5)
        for childs in cumulative_wheel:
            self.assertEqual(len(childs), 2)
            self.assertIsInstance(childs[0], ActionChromosome)
            self.assertIsInstance(childs[1], ActionChromosome)
            self.assertNotEqual(childs[0].identifier, childs[1].identifier)

    def test_selection(self):
        population = Population.generator(10, 100, ActionChromosome)
        for index in range(len(population)):
            population[index].score = index
        population.population_sort()
        best_chromosome = population.selection()
        self.assertEqual(best_chromosome.score, 9)

    # def test_selection(self):
    #     population = Population.generator(10, 100, ActionChromosome)
    #     population.chromosomes_score = [i for i in range(10)]
    #     best_chromosome = population.selection()
    #     self.assertEqual(best_chromosome.score, 0)
    #     self.assertEqual(best_chromosome, population.best_chromosome)

    # def test_mutation(self):
    #     population = Population.generator(10, 100, ActionChromosome)
    #     population.mutation()
    #     self.assertEqual(len(population), 10)
    #     self.assertEqual(len(population[0].genes), 100)
    #     self.assertEqual(len(population[0].genes), len(population[1].genes))


    # def test_genetic(self):
    #     with open("./data/surfaces/level_one_cg.json", "r") as json_file:
    #         initial_parameters = json.load(json_file) 
    #     points = initial_parameters.get('points')
    #     surface = Surface(list(map(lambda point: Point(*point), points)))
    #     initial_state = initial_parameters.get('lander_state')
    #     lander = Lander(**initial_parameters.get('lander_state'))        

    #     environment = Environment(surface, initial_state)
    #     solution = GeneticSolution(environment)
    #     solution.evolution(environment)
    #     self.assertEqual(solution.best_chromosome, solution.population.best_chromosome)
    #     self.assertEqual(solutio