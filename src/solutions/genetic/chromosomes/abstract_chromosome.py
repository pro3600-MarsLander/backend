import random

from typing import Union, Generic
from abc import abstractmethod
from environment.action import Action
from backend.src.solutions.genetic.genes.abstract_gene import AbstractGene

class AbstractChromosome:

    def __init__(self, genes_: Generic(AbstractGene) = Generic()):
        self.genes = genes_

    @staticmethod
    @abstractmethod
    def generator():
        pass

    @abstractmethod
    def mutate(self):
        pass        

    @abstractmethod
    def use(self, **kargs):
        pass