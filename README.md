# Sudoku Solver using a Genetic Algorithm 

- The solver can take in a hard coded board or a randomly generated board 
- Utilizes Uniform Crossover and Tournament Selection to optimize performance 
- Mutatation rate = 0.2


Overall Process: 
1) Generate n solutions (population)
2) Generate m new solutions (children) (reproduction)
    - Choose parents
    - Crossover + mutation
3) Choose N of the N+m solutions for new population (survival)
4) Repeat


Resources:
- Sorting population by fitness : https://stackoverflow.com/questions/58973242/deap-sorting-individuals-by-fitness
- Choosing Mutation and Crossover Ratios for Genetic:  https://www.mdpi.com
- Pretty Printing Board: https://github.com/brian-rieder/genetic-sudoku/blob/master/sudoku.py


Output Example: https://www.youtube.com/watch?v=pWT4RYaDYDI
