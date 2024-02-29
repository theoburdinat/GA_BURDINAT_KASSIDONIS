# Genetic Algorithm - Burdinat Théo & KASSIDONIS Anne-Zoé

We developed a generic and reusable code module that can solve a lot of problems using Genetic Algorithm.

## The different files 

- ga_solver.py : The most important file here. This is the generic module to solve problems with Genetic algorithms
- mastermind_problem.py : An exemple of application of our module with a mastermind game
- mastermind.py : Program of the mastermind game
- tsp_problem.py : An exemple of application of our module with a TSP problem
- cities.py : Program of the TSP problem
- cities.txt : list of cities with their coordinates for the TSP problem

For the both examples here we created some problem-specific methods to show you how it could look.

## How to use it ?

As you can see we defined an abstract class "GAProblem" in the ga_solver.py file. All the code of this file permit to do the generic parts of "generic algorithm", but in this methods we prepared the problem-specific methods.

All you have to do is to create a file for your problem, and implement these method in a chil class of "GAProblem".
Methods that have to be redefined are :
	- problem_chromosome (In your case, what's your chromosome ?) 
	- problem_fitness (In your case, how do you measure the quality of the chromosome)
	- reproduction (In your case, hwo do you want to merge old chromosomes to make new ones)
	- mutation ( In you case, how do you want to see your new chromosomes mutating)

You can also change some parameters, like the selection rate or the mutation_rate (in the __innit__ method of the class GASolver), or change the pop_size in the reset_population method.
You can aslo defind a treshold value for fitness, or change the max number of generations in the evolve_until method.
All those parameters are in the GASolver class

