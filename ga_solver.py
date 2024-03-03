# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 2024

@authors: BURDINAT Théo and KASSIDONIS Anne Zoé
From a template made by tdrumond & agademer

EPF MDE P2025 DEA2
Generic genetic algorithm module - applicable to any problem solvable with a genetic algorithm
"""
import random

class Individual:
    """Represents an Individual for a genetic algorithm (chromosome & fitness)"""

    def __init__(self, chromosome: list, fitness: float):
        """Initializes an Individual for a genetic algorithm

        Args:
            chromosome (list[]): a list representing the individual's
            chromosome
            fitness (float): the individual's fitness (the higher the value,
            the better the fitness)
        """
        self.chromosome = chromosome
        self.fitness = fitness

    def __lt__(self, other):
        """Implementation of the less_than comparator operator to be able to compare two Individuals"""
        return self.fitness < other.fitness

    def __repr__(self):
        """Representation of the object for print calls"""
        return f'Indiv({self.fitness:.1f},{self.chromosome})' #fitness is rounded for ease of reading


class GAProblem:
    """
    Defines a Genetic algorithm problem to be solved by ga_solver.
    It's an abstract class, we have to create a child class that inherits from this class for each problem we want to solve.
    All methods here have to be implemented in the child class, they are problem-specific.
    """
    def problem_chromosome(self):
        """Definition of the "chromosome" for the genetic algorithm"""
        pass
    
    def problem_fitness(self, chromosome):
        """Define the way to calculate the fitness
        
        Args:
            chromosome (array): The chromosome whose fitness is to be calculated
        """
        pass

    def reproduction(self, a, b):
        """Define the process of reproduction for the genetic algorithm problem

        Args:
            a (array): A random chromosom from the population that will become one of the parent of the new chromosome
            b (array): A random chromosom from the population that will become the other parent of the new chromosome
        """
        pass

    def mutation(self, new_chrom, len_chromosome):
        """Define the process of mutation for the genetic algorithm problem
        
        Args:
            new_chrom (array): the newborn chromosome
            len_chromosome (int): the length of a chromosome
        """
        pass



class GASolver:
    def __init__(self, problem: GAProblem, selection_rate=0.5, mutation_rate=0.1):
        """Initialize an instance of a ga_solver for a given GAProblem

        Args:
            problem (GAProblem): GAProblem to be solved by this ga_solver
            selection_rate (float, optional): Selection rate between 0 and 1.0. Defaults to 0.5.
            mutation_rate (float, optional): mutation_rate between 0 and 1.0. Defaults to 0.1.
        """
        self._problem = problem
        self._selection_rate = selection_rate
        self._mutation_rate = mutation_rate
        self._population = []

    def reset_population(self, pop_size=50):
        """ Initialize the population with pop_size random Individuals 
        - The chromosome and the fitness definitions depend of the problem, we get them from GAProblem methods
        
        Args:
            pop_size (int, optional): number of Individuals initialized
        """
        for i in range(pop_size):
            chromosome = self._problem.problem_chromosome() #Call problem_chromosome to create a chromosome (problem-specific)
            fitness = self._problem.problem_fitness(chromosome) #Calculate fitness of th chromosome
            new_individual = Individual(chromosome, fitness) #Create a new individual
            self._population.append(new_individual) #Update the population list

    def evolve_for_one_generation(self):
        """ Apply the process for one generation : 
            -	Sort the population (Descending order)
            -	Selection: Remove x% of population (less adapted)
            -   Reproduction: Recreate the same quantity by crossing the 
                surviving ones 
            -	Mutation: For each new Individual, mutate with probability 
                mutation_rate i.e., mutate it if a random value is below   
                mutation_rate
        """
        self._population.sort(reverse=True) #Sort the population
        selected_population=self._population[:round(len(self._population)*self._selection_rate)] #Select the best adapted part of the population

        while len(selected_population) < len(self._population): #Iteration until the size of population back to its initial size
            a=random.choice(selected_population) #Chose randomly a parent "a"
            b=random.choice(selected_population) #Chose randomly a parent "b"
            if a==b: #Check is parent "a" is same as "b"
                continue #Skip the iteration for these parents

            new_chrom=self._problem.reproduction(a, b) #Call reproduction (problem-specific)

            number = random.random() #Get a random number between 0 and 1.0
            if number<self._mutation_rate: #Check if the number is smaller than the mutation rate
                new_chrom=self._problem.mutation(new_chrom, len(a.chromosome)) #Call mutation (problem-specific)

            fitness=self._problem.problem_fitness(new_chrom) #Call the problem_fitness (problem-specific) 
            new_individual=Individual(new_chrom, fitness) #Create a new individual
            selected_population.append(new_individual) #Update the population with the new individual
        
        self._population = selected_population #Replace the old population by the new one

    def show_generation_summary(self):
        """ Print some debug information on the current state of the population """
        print(self._population)
        print(len(self._population))
        print(self._problem)
        
    def get_best_individual(self):
        """ Return the best Individual of the population - best fitness is the best Individual (see Individual.__lt__ method)"""
        self._population.sort(reverse=True)
        return self._population[0]

    def evolve_until(self, max_nb_of_generations=500, threshold_fitness=None):
        """ Launch the evolve_for_one_generation function until one of the two condition is achieved : 
            - Max nb of generation is achieved
            - The fitness of the best Individual is greater than or equal to
              threshold_fitness
        """
        for i in range(max_nb_of_generations): #Iteration until the max nb of generation is reached
            self.evolve_for_one_generation() #Call evolve_for_one_generation
            if self.get_best_individual().fitness == threshold_fitness: #Check if the best individual is goog enough
                break #End the solving