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


def tournament_selection(parents, x, y, survivor_percentage, tournament_size):
  population = parents
  winners = []
  # as long as we dont have enough survivors
  while(len(winners) < survivor_percentage * 100 * len(parents)):
    # print(f"winners length = {len(winners)} pop length = {len(population)}")
    # add random participants to tournament
    current_round = []
    for i in range(tournament_size):
      current_round.append(population[random.randrange(0,len(population))])

    # determine winner
    best_fitness = 0
    best_candidate = []
    for candidate in current_round:
      fitness = determine_fitness_xy(candidate, x, y)
      if(best_fitness == 0 or fitness < best_fitness):
        best_candidate = candidate
        best_fitness = fitness

    # add tournament winner to winners list
    winners.append(best_candidate)

    # delete winner from parents/population
    population.remove(best_candidate)

  return winners


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
  tsp_problem = "./tsplib/bier127.tsp"
  # tsplib problem
  x,y = tsplib_translator.xy_coords(tsp_problem)
  # number of nodes
  cities = 127
  # number of solutions
  specimen = 1000
  # survivors per selection as percentage of input
  survivors_percentage = 0.2
  # crossing points
  crossing_points = (45,55)
  # mutation chance
  mutation = 0
  # repetitions
  repetitions = 4
  # plus selection flag, 0 = comma selection
  plus_seleciton_flag = 1
  # tournament size
  tournament_size = 2

  population = random_start_population(cities, specimen)

  for i in range(repetitions):
    if(len(population) <= 4):
      break

    print(f" repetition = {i+1} population size = {len(population)}")

    # parent selection
    # population = parent_selection(population, x, y, survivors_percentage)
    population = tournament_selection(population, x, y, survivors_percentage, tournament_size)

    # delete last element if uneven size so we can have even amount of parents
    # kinda unnecessary as the zip - iterator also takes care of this
    # if(len(population) % 2 != 0):
      # del population[-1]

    # variation
    children = []
    for parent1, parent2 in zip(population[::2], population[1::2]):
      children.append(create_offspring(parent1, parent2, crossing_points, mutation))


    population = children + population * plus_seleciton_flag


  parent_fitness = {}

  # determine fitness for each parent
  for i in population:
    fitness = determine_fitness_xy(i, x, y)
    # parent path = key ||| fitness = value
    parent_fitness[str(i)] = fitness

  sorted_tuples = sorted(parent_fitness.items(), key=lambda item: item[1])
  sorted_dict = {k: v for k, v in sorted_tuples}

  print(list(sorted_dict.values())[0])


  timestr = time.strftime("%Y-%m-%d_%H-%M-%S")

  f = open(f"./results/tsp_run_{timestr}.txt", "w")
  f.write(f"TSP PROBLEM = {tsp_problem} \n\n")
  f.write(f"Starting population size = {specimen} \n")
  f.write(f"Survivors per selection in % = {survivors_percentage * 100} % \n")
  f.write(f"Crossing points = {crossing_points} \n")
  f.write(f"Mutation chance = {mutation * 100} % \n")
  f.write(f"Generations = {repetitions} \n")
  f.write(f"Plus selection flag = {plus_seleciton_flag} \n")
  f.write(f"tournament size per round = {tournament_size}")
  f.write("\nRESULT: \n\n")
  f.write(f"Fitness = {list(sorted_dict.values())[0]} \nPath = {list(sorted_dict.keys())[0]} \n\n")

# genetic_algorithm()

loops = 1
for i in range(0,loops):
  genetic_algorithm()