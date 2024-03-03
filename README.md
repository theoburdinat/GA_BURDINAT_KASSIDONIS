# Genetic Algorithm - Burdinat Théo & KASSIDONIS Anne-Zoé

We developped a generic and reusable code module that can solve a lot of problems using Genetic Algorithm, 
with examples of use for two problems provided by our teachers.

## The different files 

- ga_solver.py : The main file. This is the generic module to solve problems with Genetic algorithms
- mastermind_problem.py : The specific script to define the methods to solve the mastermind game, as an example
- mastermind.py : The program of the mastermind game provided by our teachers
- tsp_problem.py : The specific script to define the methods to solve the TSP problem, as an example
- cities.py : The program of the TSP problem provided by our teachers
- cities.txt : The list of cities with their coordinates for the TSP problem

For both examples we created some problem-specific methods to show different ways to use our code module.

## How to use it ?

Our code in the file ga_solver.py permits to do the generic parts of "genetic algorithm" and doesn't require changes when applied to a different problem.
In this file we defined an abstract class "GAProblem" to prepare the problem-specific methods.

All you have to do is to create a file for your problem, and implement these methods in a child class of "GAProblem".
Methods that should be defined in your specific file are :
- problem_chromosome (In your case, what's your chromosome ?) 
- problem_fitness (In your case, how do you measure the quality of the chromosome ?)
- reproduction (In your case, how do you want to merge old chromosomes to make new ones ?)
- mutation (In your case, how do you want the mutation of your new chromosomes to happen ?)

The files masterming_problem.py and tsp_problem.py should be of great help to better understand how to define the methods !

You can also change other parameters like the selection_rate, the mutation_rate (in the __innit__ method of the class GASolver), or the pop_size in the reset_population method. 
You can also define a treshold value for fitness, or change the max number of generations in the evolve_until method. 
All those parameters are in the GASolver class

