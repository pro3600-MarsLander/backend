import random

from typing import Union, Generic
from abc import abstractmethod
from environment.action import Action
from solutions.genetic.genes.abstract_gene import AbstractGene

class AbstractChromosome:

    def __init__(self, identifier: int, genes_):
        self.identifier = identifier
        self.genes = genes_
        self.score = 0
        
    @staticmethod
    @abstractmethod
    def generator(**kargs):
        pass


    @property
    def get_length(self):
        pass

    @abstractmethod
    def mutate(self):
        pass        

    @abstractmethod
    def use(self, **kargs):
        pass

    def reset(self):
        self.score = 0
