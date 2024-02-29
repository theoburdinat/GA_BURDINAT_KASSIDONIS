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
        """Initializes an instance of a ga_solver for a given GAProblem

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
            chromosome = self._problem.problem_chromosome() #We create a chromosome
            fitness = self._problem.problem_fitness(chromosome) #Then we calculate its fitness
            new_individual = Individual(chromosome, fitness) #We create the new Individual
            self._population.append(new_individual) #We update the population list

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
        #Sort the population & Selection
        self._population.sort(reverse=True)
        selected_population=self._population[:round(len(self._population)*self._selection_rate)]

        # While the size of the population is less than the initial size of the population
        while len(selected_population) < len(self._population):
            #a and b are the two parents of the new Individual - chosen randomly
            a=random.choice(selected_population)
            b=random.choice(selected_population)
            #If a and b are the same chromosome we take other parents, it doesn't make a lot of sense
            if a==b:
                continue

            #Reproduction (problem-specific)
            new_chrom=self._problem.reproduction(a, b)

            #Mutation (The mutation activation criterion is general (random event). However, the way to modify the chromosome is different for each problem)
            number = random.random()
            if number<self._mutation_rate:
                new_chrom=self._problem.mutation(new_chrom, len(a.chromosome))

            # Calculation of the fitness of the new chromosome, and creation of the Individual - update of the population
            fitness=self._problem.problem_fitness(new_chrom)
            new_individual=Individual(new_chrom, fitness)
            selected_population.append(new_individual)
        
        # When the new population has the good number of Individuals inside itself, the old population is changed to the new population
        self._population = selected_population

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
        for i in range(max_nb_of_generations):
            self.evolve_for_one_generation()
            if self.get_best_individual().fitness == threshold_fitness:
                break