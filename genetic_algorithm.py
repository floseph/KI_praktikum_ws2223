import random
import math
import time
import tsplib_translator

arrray = [1,4,3,5,2,1]

# start and end are always 1
def intialize_population(cities, specimen):
  specimen_list = []

  for i in range(specimen):
    random_parent = list(range(2,cities + 1))
    random.shuffle(random_parent)
    random_parent = [1] + random_parent + [1]
    specimen_list.append(random_parent)
  return specimen_list


# start and end are same number but random every time
def random_start_population(cities, specimen):
  specimen_list = []

  for i in range(specimen):
    random_parent = list(range(1,cities + 1))
    random.shuffle(random_parent)
    random_parent = random_parent + [random_parent[0]]
    specimen_list.append(random_parent)
  return specimen_list


def determine_fitness(path, evaluation_matrix):

  total = 0

  for i, value in enumerate(path):
    if(i == len(path) - 1):
      break
    
    step = evaluation_matrix[value - 1][path[i+1] - 1]
    total += step

    # print(f"from {value} to {path[i+1]} step-length: {step} subtotal: {total}")
  
  # print(f"total: {total}")
  return total

def determine_fitness_xy(path, x, y):

  total = 0

  for i, value in enumerate(path):
    if(i == len(path) - 1):
      break
    
    x_distance = x[value - 1] - x[path[i+1] - 1]
    y_distance = y[value - 1] - y[path[i+1] - 1]
    # pythagoras theorem
    step = round(math.sqrt(x_distance * x_distance + y_distance * y_distance))
    total += step

    # print(f"from {value} to {path[i+1]} step-length: {step} subtotal: {total}")
  
  # print(f"total: {total}")
  return total


matrix_one = [
  [0,6,9,14,9,12,18,1],
  [6,0,3,8,3,6,12,7],
  [9,3,0,5,3,6,13,10],
  [14,8,5,0,8,7,18,15],
  [9,3,3,8,0,3,10,10],
  [12,6,6,7,3,0,13,13],
  [18,12,13,18,10,13,0,19],
  [1,7,10,15,10,13,19,0]
]

x = [1,3,4,5,2,6,7,8,1]

def parent_selection(parents, x, y, survivor_count):

  parent_fitness = {}
  parent_set = []

  for i in parents:
    if(i not in parent_set):
      parent_set.append(i)
  # determine fitness for each parent
  for parent in parent_set:
    fitness = determine_fitness_xy(parent, x, y)
    # parent path = key ||| fitness = value
    parent_fitness[str(parent)] = fitness

  total_fitness = sum(parent_fitness.values())

  # replace fitness int with prob. (roulette selection)
  for i in parent_fitness:
    parent_fitness[i] = 1 - parent_fitness[i] / total_fitness

  selected_pop = random.choices(parent_set, parent_fitness.values(), k = round(len(parent_set) * survivor_count))
  return selected_pop

# x,y = tsplib_translator.xy_coords("./tsplib/eil76.tsp")
# survivors = parent_selection(random_start_population(76,10),x, y, 0.74)
# print(survivors)
# print(len(survivors))


def create_offspring(parent_one, parent_two, crossing_points, mutation_chance):
  
  parent_one_substring = parent_one[crossing_points[0] : crossing_points[1]]
  

  parent_two_tail = parent_two[crossing_points[1]:]
  parent_two_head = parent_two[1:crossing_points[1]]

  parent_two_substring = parent_two_tail + parent_two_head

  parent_two_substring = list(filter(lambda e: e not in parent_one_substring, parent_two_substring))

  offspring_tail_length = len(parent_two) - crossing_points[1] - 1
  offspring_tail = parent_two_substring[:offspring_tail_length]
  offspring_head = parent_two_substring[offspring_tail_length :]

  offspring = offspring_head + parent_one_substring + offspring_tail 

  # mutation

  for i, value in enumerate(offspring):

    if(i == len(offspring)-1):
      break


    random_number = random.randint(0,100)

    if(random_number < mutation_chance * 100):
      print("mutate")
      second_spot = random.randint(1, len(offspring) - 1)
      temp = offspring[second_spot]
      offspring[second_spot] = value
      offspring[i] = temp

  return offspring + [offspring_head[0]]

# cross_p = (2,3)
# mutation = 0.01
# print(create_offspring([1,2,5,6,4,3,8,7,1],[1,4,2,3,6,5,7,8,1],cross_p,mutation))
# x,y = tsplib_translator.xy_coords("./tsplib/eil76.tsp")

# determine_fitness_xy(intialize_population(76,1)[0],x,y)

def genetic_algorithm():
  tsp_problem = "./tsplib/eil76.tsp"
  # tsplib problem
  x,y = tsplib_translator.xy_coords(tsp_problem)
  # number of nodes
  cities = 76
  # number of solutions
  specimen = 100000
  # survivors per selection as percentage of input
  survivors_percentage = 0.7
  # crossing points
  crossing_points = (23,53)
  # mutation chance
  mutation = 0
  # repetitions
  repetitions = 15
  # µ parents
  parent_mu = 0
  # lambda children
  children_lambda = 0.8

  population = random_start_population(cities, specimen)

  for i in range(repetitions):
    if(len(population) <= 4):
      break
    # parent selection
    population = parent_selection(population, x, y, survivors_percentage)

    # delete last element if uneven size so we can have even amount of parents
    # kinda unnecessary as the zip - iterator also takes care of this
    # if(len(population) % 2 != 0):
      # del population[-1]

    # variation
    children = []
    for parent1, parent2 in zip(population[::2], population[1::2]):
      children.append(create_offspring(parent1, parent2, crossing_points, mutation))

    # combine children + parents according to percentage
    
    # print(f"population: {population} ")
    # print(f"children: {children}")
    # population = children + population
    # print(f"new pop: {population}")

    parent_percentage = round(len(population) * parent_mu)
    children_percentage = round(len(children) * children_lambda)

    population = population[:parent_percentage] + children[:children_percentage]

  parent_fitness = {}

  # determine fitness for each parent
  for i in population:
    fitness = determine_fitness_xy(i, x, y)
    # parent path = key ||| fitness = value
    parent_fitness[str(i)] = fitness

  sorted_tuples = sorted(parent_fitness.items(), key=lambda item: item[1])
  sorted_dict = {k: v for k, v in sorted_tuples}

  print(sorted_dict)


  timestr = time.strftime("%Y%m%d-%H%M%S")

  f = open(f"./results/{timestr}.txt", "w")
  f.write(f"TSP PROBLEM = {tsp_problem} \n\n")
  f.write(f"Starting population size = {specimen} \n")
  f.write(f"Survivors per selection in % = {survivors_percentage * 100} % \n")
  f.write(f"Crossing points = {crossing_points} \n")
  f.write(f"Mutation chance = {mutation * 100} % \n")
  f.write(f"Generations = {repetitions} \n")
  f.write(f"Percentage of parents selected = {parent_mu * 100} % \n")
  f.write(f"Percentage of children selected = {children_lambda * 100} % \n")
  f.write("\nRESULTS: \n\n")

  for i in sorted_dict:
    f.write(f"Fitness = {sorted_dict[i]} \nPath = {i} \n\n")

genetic_algorithm()