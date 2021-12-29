# importing libraries 
import numpy as np
import random 
import sys

# passing hard coded sudoku grid
sudoku =[[7,8,0, 4,0,0, 1,2,0],
		[6,0,0, 0,7,5, 0,0,9],
		[0,0,0, 6,0,1, 0,7,8],
		[0,0,7, 0,4,0, 2,6,0],
		[0,0,1, 0,5,0, 9,3,0],
		[9,0,4, 0,6,0, 0,0,5],
		[0,7,0, 3,0,0, 0,1,2],
		[1,2,0, 0,0,7, 4,0,0],
		[0,4,9, 2,0,6, 0,0,7]]

sudoku2 = [[0,4,3, 0,8,0, 2,5,0],
       [6,0,0, 0,0,0, 0,0,0],
       [0,0,0, 0,0,1, 0,9,4],
       [9,0,0, 0,0,4, 0,7,0],
       [0,0,0, 6,0,8, 0,0,0],
       [0,1,0, 2,0,0, 0,0,3],
       [8,2,0, 5,0,0, 0,0,0],
       [0,0,0, 0,0,0, 0,0,5],
       [0,3,4, 0,9,0, 7,1,0]]

# one of the hardest sudoku boards ever 
sudoku3 =[[8,0,0, 0,0,0, 0,0,0],
		[0,0,3, 6,0,0, 0,0,0],
		[0,7,8, 0,9,0, 2,6,0],
		[0,5,0, 0,0,7, 0,0,0],
		[0,0,0, 8,4,5, 7,0,0],
		[0,0,0, 1,2,0, 0,3,0],
		[0,0,1, 0,0,0, 0,6,8],
		[0,8,5, 4,1,9, 0,1,0],
		[0,9,0, 0,0,0, 4,0,0]]

# printing board 
# code from: https://github.com/brian-rieder/genetic-sudoku/blob/master/sudoku.py

def pretty_print(grid):
    side = len(grid)
    bottom = int(side ** 0.5)
    expand_line = lambda line : line[0]+line[5:9].join([line[1:5]*(bottom-1)]*bottom)+line[9:13]
    # line zero 
    l_0 = expand_line("╔═══╤═══╦═══╗")
    # line one 
    l_1 = expand_line("║ . │ . ║ . ║")
    # line two
    l_2 = expand_line("╟───┼───╫───╢")
    # line three
    l_3 = expand_line("╠═══╪═══╬═══╣")
   # line four  
    l_4 = expand_line("╚═══╧═══╩═══╝")
    symb = " 1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    numbers = [[""] + [symb[n] for n in row] for row in grid]
    print(l_0)
    for r in range(1, side + 1):
        print("".join(n + s for n, s in zip(numbers[r - 1], l_1.split("."))))
        print([l_2, l_3, l_4][(r % side == 0) + (r % bottom == 0)])

# pretty_print(new_grid)

# NOT CHECKING FOR DIAGONALS HERE 
def create_board(h, w):
    # no duplicates in each row
    board = [[(i + k) % 9 + 1 for i in range(1, h + 1)] for k in range(w)] 
    # shuffling the board on row side
    random.shuffle(board) 
    # reads each row and puts it into a column
    board = [[board[x][y] for x in range(9)] for y in range(9)]
    # Shuffles the board on column side
    random.shuffle(board)
    return board
board = create_board(9,9)
# pretty_print(board)

# able to remove how many ever values as the user wants
def remove_numbers(board, num_remove):
    h, w, r = len(board), len(board[0]), []
    spaces = [[x, y] for x in range(h) for y in range(w)]
    for k in range(num_remove):
        r = random.choice(spaces)
        board[r[0]][r[1]] = 0
        spaces.remove(r)
    return board
new_grid = remove_numbers(board,30)
# pretty_print(new_grid)

def initialize_population(grid, population_size):
	return [filler(grid) for _ in range(population_size)]

# trying randomly input numbers wherever there is a zero 
# each population will look different (the numbers will be shuffled in different ways)
# this will serve in helping intializing a random population 

def filler(grid):
	# empty list
	mutated_grid = []
	for i in range(9):
		# these are the sudoku values for the grid (no zeros)
		values = [1,2,3,4,5,6,7,8,9]
		# fulling in and appending these values into the grid 
		mutated_grid.append(list(grid[i]))
		for j in range(9):
    # if the value needs to be solved for (aka it is zero)
			if (mutated_grid[i][j] == 0):
				# setting value 
				is_correct_value = False
        # while the value needs to be solved for 
				while(is_correct_value == False):
          # randomly choosing values from 1-9
					value_chosen = random.choice(values)
          # making sure it's not already in the list 
					if(value_chosen not in mutated_grid[i]):
						mutated_grid[i][j] = value_chosen
						values.remove(value_chosen)
						is_correct_value = True
					else:
						# removing value chosen if value is already there 
						values.remove(value_chosen)
	return mutated_grid

# filling in input values (not checking for dups here)
filler(new_grid)

def select_parents(population, fitness_population, population_size):
  # for key https://stackoverflow.com/questions/58973242/deap-sorting-individuals-by-fitness
  # sorting the population by their fitness
	sort_by_fitness_pop = sorted(zip(population, fitness_population),key = lambda x: x[1])
 
  # Choosing Mutation and Crossover Ratios for Genetic https://www.mdpi.com
  # mutation rate: 0.5
  # changed mutation rate after presentation to 0.2

	mutation_rate = 0.2
	return [ individual for individual, fitness in sort_by_fitness_pop[int(population_size * mutation_rate):]]

def crossover_individual(parent1, parent2):
  crossover_list1=[]
  for child in zip(parent1, parent2):
    crossover_list1.append(list(random.choice(child)))
  # returning the child
  return crossover_list1

# each bit is chosen from either parent with equal probability
def uniform_crossover(population, population_size):
	crossover_list2=[]
	for i in range(population_size):
		# roulette selection
		crossover_list2.append(crossover_individual(random.choice(population), random.choice(population)))
	return crossover_list2

def mutate_grid(mutated_grid, grid):
	# setting mutation rate 
	mutation_rate = 0.1
	for i in range(9): 
    # [0.0, 1.0)
		if (random.random() < mutation_rate):
      # if grid isn't mutated yet 
			isMutated = False
			while(isMutated == False):
        # randomly generate # between 0-8
				rand1 = random.randint(0,8)
		 		# randomly generate # between 0-8
				rand2 = random.randint(0,8)
				if (grid[i][rand1] == 0 and grid[i][rand2] == 0):
          #  grid needs to be mutated
					mutated_grid[i][rand1] = mutated_grid[i][rand2]
          #  grid needs to be mutated
					mutated_grid[i][rand2] = mutated_grid[i][rand1]
					isMutated = True
  # mutated grid 
	return list(mutated_grid)

def mutate_child(population, grid):
  # The mutated population
	return [ mutate_grid(individual, grid) for individual in population ]

def populationFitness(population, generation=0):
	# fitness of population 
	return [calculate_fitness(fitness) for fitness in population]

# fitness of the grid by going through each row and column 
# originally i had gone through each column and each indivudal cell (all 9) but 
# the fitness was lower when i did it that way 

def calculate_fitness(grid):
	# initialize fitness to 0 
	fitness = 0

# fitness for each row
	for i in range(9):
		solutions = []
		for j in range(9):
			# going through each row
			solutions.append(grid[i][j])
		for num in range(9):
			if (solutions[num] in solutions[num+1:]) == False:
				fitness += 1

# fitness for each column
	for i in range(9):
		solutions = []
		for j in range(9):
			# going through each column
			solutions.append(grid[j][i])
		for num in range(9):

			if (solutions[num] in solutions[num+1:]) == False:
				fitness += 1

	# needs to be out of 162 (81 numbers on the board * 2)
	# if we place solved equal to 81 it will have fitness values over 1
	solved = fitness/162

	# checking whether a solution is found
	if (solved == 1.0):
		print()
    # printing the solved board
		print("Final Board: ")
		pretty_print(grid)
		sys.exit()
	
	return solved

def tournament_selection(population,population_size):
  solutionsarray = []
  for i in range(population_size):
    ind1 = random.randint(0,len(population)-1)
    ind2 = random.randint(0,len(population)-1)

    solution1 = population[ind1]
    solution2 = population[ind2]
    
    fitness1 =  calculate_fitness(solution1)
    fitness2 =  calculate_fitness(solution2)

    if fitness1 > fitness2:
      solutionsarray.append(solution1)
    elif fitness1 < fitness2:
      solutionsarray.append(solution2)
    
  return solutionsarray

def ga(grid, population_size):
	# setting iteration to 0 
	iteration = 0
	# setting maxima_stuck to 0
	maxima_stuck = 0
	# population --> initialize_population
	population = initialize_population(grid, population_size)
	# fitness_population --> populationFitness
	fitness_population = populationFitness(population)

	# the maximum number of iterations i saw went up to around 70 so 100 seemed like a good number to choose 
	while (iteration <= 1000):
		# each time it goes through the loop increase the iteration by 1 
		iteration += 1
		# setting the maxima limit to 25 so it can restart at generation 0 from a new point
		maxima_limit = 25
		# parent_population --> select_parents
		parent_population = select_parents(population, fitness_population, population_size)
		# child_population --> uniform_crossover
		child_population = uniform_crossover(parent_population, population_size)
		# population --> mutate_child
		population = mutate_child(child_population, grid)
		# sorting to get the most recent fitness population 
		last_fitness = sorted(fitness_population)[-1]
		fitness_population = populationFitness(population, iteration)
		tournament = tournament_selection(population,population_size)

		# if the last fitness is the same as the last fitness of the population then increase
		# minima stuck by 1 each time
		if (last_fitness == sorted(fitness_population)[-1]):
			maxima_stuck += 1
      		# once the fitness is the same 25 times, generation starts back at 0 
			if maxima_stuck == maxima_limit:

				# resetting maxima_stuck back to 0 once limit is hit 
				maxima_stuck = 0
				# resetting iteration back to 0 once limit is hit 
				iteration = 0
				
				# printing each time it has gotten stuck 25 times and is restarting
				print("")
				print("Stuck at local maxima! ")
				print("Restarting at Generation: 0")
				print("")

				# reinitialize 
				fitness_population = populationFitness(population)
				population = initialize_population(grid, population_size)
				tournament = tournament_selection(population,population_size)
			
		else:
      # not stuck at minima 
			minima_stuck = 0

		print("Generation:", iteration)
		print("Fitness %.3f" % sorted(fitness_population)[-1])
		print("")

print("Original Board:")
pretty_print(new_grid)
print("")
solved_grid = ga(new_grid, 1000)
print(check_sudoku(solved_grid))
