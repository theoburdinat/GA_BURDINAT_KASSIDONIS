# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 2024

@authors: BURDINAT Théo and KASSIDONIS Anne Zoé
From a template made by tdrumond & agademer

EPF MDE P2025 DEA2
GA solving TSP example

The file to specify all elements of the resolution of the TSP problem, that are not generic.
"""
from ga_solver import GAProblem
import cities
import random

class TSProblem(GAProblem):
    """Implementation of GAProblem for the traveling salesperson problem - exemple of application of the Generic genetic algorithm module"""
    def __init__(self, city_dict):
        """Initialize the Genetic algorithm problem to be solved by ga_solver, defining important variables specific to the TSP problem
        
        Args:
            city_dict (Array[String]) = List of cities with their coordinates
        """
        self.possible_cities = cities.default_road(city_dict) #Get the possible cities for the problem

    def problem_chromosome(self):
        """Definition of the "chromosome" for the TSP problem"""
        chromosome = cities.default_road(city_dict) #Get the list of the cities
        random.shuffle(chromosome) #Shuffle the names of the cities to create a chromosome
        return chromosome
    
    def problem_fitness(self, chromosome):
        """Definition of the fitness for the TSP problem
        
        Args:
            chromosome (array): The chromosome whose fitness is to be calculated
        """
        return -cities.road_length(city_dict, chromosome) #Get the fitness and invert it bc we are looking for the shortest way/fitness

    def reproduction(self, a, b):
        """
        Define the process of reproduction for the genetic algorithm problem
        Here the x_point(point that defines where parents are cut) is at the middle of parents chromosomes and it's not possible to have cities repetetion (we have to have all the cities one and no more than one time)

        Args:
            a (array): A random chromosom from the population that will become one of the parent of the new chromosome
            b (array): A random chromosom from the population that will become the other parent of the new chromosome
        """
        x_point = len(a.chromosome)//2 #Get half the length of the chromosome (list of cities)
        new_chrom = a.chromosome[0:x_point] #Add the first half of parent "a" to the new chromosome
        for city in range(x_point,len(b.chromosome)): #Iteration among the second half of parent "b"
            if b.chromosome[city] not in new_chrom: #Chech if the city is not already in the newborn gene
                new_chrom.append(b.chromosome[city]) #Add the city
        if len(new_chrom) < len(a.chromosome): #Check if the length of the new chromosome is right
            for i in range(len(self.possible_cities)): #Iterate throught all cities
                if self.possible_cities[i] not in new_chrom: #Check if a city is missing from the new chromosome
                    new_chrom.append(self.possible_cities[i]) #Add the city
        return new_chrom

    def mutation(self, new_chrom, len_chromosome):
        """Define the process of mutation for the genetic algorithm problem
        Here we switch two random cities positions
        
        Args:
            new_chrom (array): the newborn chromosome
            len_chromosome (int): the length of a chromosome
        """
        pos_a = random.randrange(0,len_chromosome) #Chose randomly a position in the length of the chromosome
        pos_b = random.randrange(0,len_chromosome) #Chose randomly another position in the length of the chromosome
        new_chrom[pos_a], new_chrom[pos_b] = new_chrom[pos_b], new_chrom[pos_a] #Invert the cities on those positions
        return new_chrom

if __name__ == '__main__':

    from ga_solver import GASolver

    city_dict = cities.load_cities("cities.txt")
    problem = TSProblem(city_dict)
    solver = GASolver(problem)
    solver.reset_population()
    solver.evolve_until(max_nb_of_generations=5000)
    best=solver.get_best_individual()
    cities.draw_cities(city_dict, best.chromosome)
    print(best)