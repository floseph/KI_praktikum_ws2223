import random

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

  #   print(f"from {value} to {path[i+1]} step-length: {step} subtotal: {total}")
  
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

# print(determine_fitness(x, matrix_one))

def parent_selection(parents, evaluation_matrix, survivor_count):

  parent_fitness = {}

  # determine fitness for each parent
  for i in parents:
    fitness = determine_fitness(i, evaluation_matrix)
    parent_fitness[str(i)] = fitness

  total_fitness = sum(parent_fitness.values())

  # replace fitness int with prob. (roulette selection)
  for i in parent_fitness:
    parent_fitness[i] /= total_fitness

  print(random.choices(parents, parent_fitness.values(), k = survivor_count))
  return parent_fitness


y = [x,[1,3,5,4,2,6,7,8,1]]

# parent_selection(y, matrix_one, 10)

def create_offspring(parent_one, parent_two, crossing_points, mutation_chance):
  
  return 0