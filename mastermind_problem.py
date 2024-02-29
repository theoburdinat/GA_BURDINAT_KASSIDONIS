# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 2024

@authors: BURDINAT Théo and KASSIDONIS Anne Zoé
From a template made by tdrumond & agademer

EPF MDE P2025 DEA2
GA solving Mastermind example
"""
from ga_solver import GAProblem
import mastermind as mm
import random

class MastermindProblem(GAProblem):
    """Implementation of GAProblem for the mastermind problem - exemple of application of the Generic genetic algorithm module"""
    def __init__(self, match):
        """Initialize the Genetic algorithm problem to be solved by ga_solver, defining important variables specific to the mastermind problem
        
        Args:
            match (MastermindMatch) = Parameters of the mastermind game, plays the role of the codemaker
        """
        self.MATCH = match
        self.valid_colors = mm.get_possible_colors()

    def problem_chromosome(self):
        """Definition of the "chromosome" for the Mastermind problem"""
        return self.MATCH.generate_random_guess()
    
    def problem_fitness(self, chromosome):
        """Definition of the fitness for the Mastermind problem
        
        Args:
            chromosome (array): The chromosome whose fitness is to be calculated
        """
        return self.MATCH.rate_guess(chromosome)

    def reproduction(self, a, b):
        """
        Define the process of reproduction for the genetic algorithm problem
        Here the x_point(point that defines where parents are cut) is chosen randomly and it's possible to get colors repetition

        Args:
            a (array): A random chromosom from the population that will become one of the parent of the new chromosome
            b (array): A random chromosom from the population that will become the other parent of the new chromosome
        """
        x_point = random.randrange(1, len(a.chromosome)-1) #We can't cut on the first or the last element, the objective is to get a mix of the two parents.
        new_chrom = a.chromosome[0:x_point] + b.chromosome[x_point:]
        return new_chrom

    def mutation(self, new_chrom, len_chromosome):
        """Define the process of mutation for the genetic algorithm problem
        Here we change a random gene from the newborn chromosome for a new colour
        
        Args:
            new_chrom (array): the newborn chromosome
            len_chromosome (int): the length of a chromosome
        """
        new_gene = random.choice(self.valid_colors)
        pos = random.randrange(0, len_chromosome)
        new_chrom = new_chrom[0:pos] + [new_gene] + new_chrom[pos+1:]
        return new_chrom



if __name__ == '__main__':

    from ga_solver import GASolver

    match = mm.MastermindMatch(secret_size=6) 
    problem = MastermindProblem(match)
    solver = GASolver(problem)

    solver.reset_population()
    solver.evolve_until(threshold_fitness=match.max_score())

    best = solver.get_best_individual()
    print(f"Best guess {best.chromosome}")
    print(f"Problem solved? {match.is_correct(best.chromosome)}")