# -*- coding: utf-8 -*-
"""Renan_Santos_Atividade_2_GA.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1bcwsOgvjmWW9ecCw2S1kerDAWrrrjAVm

## Imports
"""

import random
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt

"""## GA Implementação"""

def generate_population(size, dimensions, boundaries):

    # Os indivíduos da população são organizados como uma lista.
    population = []
    for i in range(size):
        
        individual = []

        for d in range(0,dimensions):
          # A função random.uniform gera um número aleatório segundo uma 
          # distribuição de probabilidades uniforme entre os limites informados.
          ind = random.uniform(boundaries[d][0], boundaries[d][1])
          individual.append(ind)
        
        population.append(individual)

    return population

def sort_population_by_fitness(population):
    return sorted(population, key=apply_function)

def choice_by_roulette(sorted_population, fitness_sum):
    offset = 0
    normalized_fitness_sum = fitness_sum

    # Ajuste dos fitnesses com os offsets, caso existam valores de fitnesses negativos.
    lowest_fitness = apply_function(sorted_population[0])
    if lowest_fitness < 0:
        offset = -lowest_fitness
        normalized_fitness_sum += offset * len(sorted_population)

    # Giro da roleta.
    draw = random.uniform(0, 1)

    # Escolha do indivíduo.
    accumulated = 0
    for individual in sorted_population:
        fitness = apply_function(individual) + offset
        probability = fitness / normalized_fitness_sum
        accumulated += probability

        if draw <= accumulated:
            return individual

    return random.choice(sorted_population)

def tournament_selection(pop, k):
  k = round(k)
  best = None
  better = None
  for i in range(k):
      ind = random.choice(pop)
      if best == None or apply_function(ind) > apply_function(best):
          best = ind
      else:
        if better == None or apply_function(ind) > apply_function(better):
          better = ind
      
      # pop.remove(ind)
      
  return better, best

def crossover(individual_a, individual_b):
  
    dim = len(individual_a)

    child = []

    for d in range(dim):
      child.append(random.choice([individual_a[d],individual_b[d]]))

    return child

def mutate(individual, boundaries, probability = 0.01, inc = 0.05):
    dim = len(individual)

    for d in range(dim):
      if random.random()<= probability:
        lower_boundary, upper_boundary = boundaries[d][0],boundaries[d][1]
        aux = individual[d] + random.uniform(-inc, inc)
        # Garantir que os indivíduos resultantes respeitem os limites estabelecidos para as variáveis
        individual[d]= min(max(aux, lower_boundary), upper_boundary) 

    return individual

def make_next_generation(previous_population,boundaries, n_elitismo = 1):
    next_generation = []
    sorted_by_fitness_population = sort_population_by_fitness(previous_population)
    population_size = len(previous_population)
    # fitness_sum = sum(apply_function(individual) for individual in previous_population)
  

    for i in range(population_size):
        # first_choice = choice_by_roulette(sorted_by_fitness_population, fitness_sum)
        # second_choice = choice_by_roulette(sorted_by_fitness_population, fitness_sum)
        first_choice, second_choice = tournament_selection(previous_population,
                                                           len(previous_population)*0.4)

        individual = crossover(first_choice, second_choice)
        individual = mutate(individual, boundaries)
        next_generation.append(individual)

    if n_elitismo>0:
      next_generation = sort_population_by_fitness(next_generation)
      next_generation = next_generation[n_elitismo:]
      next_generation.extend(sorted_by_fitness_population[(population_size-n_elitismo):])

    return next_generation

def RunGA(generations, dimensions, boundaries, positions= [], solutions = [], size=20):

  population = generate_population(size, dimensions=d, boundaries=boundaries)

  i = 1
  while True:
      if i%10==0: 
        print(f"🧬 GENERATION {i}")

      # for individual in population:
      #     print(individual, apply_function(individual))

      if i == generations:
          break

      i += 1

      population = make_next_generation(population, boundaries)

  best_individual = sort_population_by_fitness(population)[-1]
  positions.append(best_individual)
  best_solution = apply_function(best_individual)
  solutions.append(best_solution)

  print("\n🔬 FINAL RESULT")
  print(best_individual, best_solution)
  return positions, solutions

"""## Atividade 1

### 1.1 - Rastrigin
"""

def Rastrigin(x, A, n):
  soma = 0
  for i in range(len(x)):
    soma += (x[i]**2 - (x[i]**2 - A * np.cos(2 * np.pi * x[i])))
  f = A*n + soma
  return f

def apply_function(X):
  return -Rastrigin(X,10,10)

generations = 100
d=10
boundaries = [[-5.12,5.12]]*d
rodadas = 30

solutionsRastrigin = []
positionsRastrigin = []

for i in range(rodadas):
  print(f'Rodada {i+1}')
  RunGA(generations,d,boundaries, size = 20, positions = positionsRastrigin, solutions = solutionsRastrigin)

display(solutionsRastrigin)

med = np.mean(solutionsRastrigin)
std = np.std(solutionsRastrigin)

print(f'O custo médio das soluções foi de {med}. \nO desvio padrão do custo foi de {std}.')

plt.boxplot(solutionsRastrigin)

df = pd.DataFrame(data = {'x':[x[0] for x in positionsRastrigin], 
                          'y':[x[1] for x in positionsRastrigin],
                          'solution':solutionsRastrigin})
df.sort_values('solution', ascending=False).head(3)

"""### 1.2 - Rosenbrook"""

def Rosenbrock(x, a, b):
  f = (a - x[0]) ** 2 + b * (x[1] - x[0] ** 2) ** 2
  return f

def apply_function(x):
  return -Rosenbrock(x,1,100)

#NESTA SOLUÇÃO UTILIZOU-SE ESCOLHA POR TORNEIO

generations = 500
d=2
boundaries = [[-30,30]]*d
rodadas = 30

solutionsRosenbrock = []
positionsRosenbrock = []

for i in range(rodadas):
  RunGA(generations,d,boundaries, size = 100, positions = positionsRosenbrock, solutions = solutionsRosenbrock)

display(solutionsRosenbrock)

plt.boxplot(solutionsRosenbrock)

#Melhores Soluções
df = pd.DataFrame(data = {'x':[x[0] for x in positionsRosenbrock], 
                          'y':[x[1] for x in positionsRosenbrock],
                          'solution':solutionsRosenbrock})
df.sort_values('solution', ascending=False).head(3)

med = np.mean(solutionsRosenbrock)
std = np.std(solutionsRosenbrock)

print(f'O custo médio das soluções foi de {med}. \nO desvio padrão do custo foi de {std}.')

"""### 1.3 - Esfera"""

def apply_function(x):
  soma = 0
  for i in range(len(x)):
    soma+= x[i]**2
  return -soma

generations = 500
d=10
boundaries = [[-100,100]]*d
rodadas = 30

positionsEsfera = []
solutionsEsfera = []

for i in range(rodadas):
  RunGA(generations,d,boundaries, size = 100, positions = positionsEsfera, solutions = solutionsEsfera)

display(solutionsEsfera)

#Melhores Soluções
df = pd.DataFrame(data = {
                          # 'x':[x[0] for x in positionsEsfera], 
                          # 'y':[x[1] for x in positionsEsfera],
                          'solution':solutionsEsfera})
display(positionsEsfera[21])
df.sort_values('solution', ascending=False).head(3)

med = np.mean(solutionsEsfera)
std = np.std(solutionsEsfera)

print(f'O custo médio das soluções foi de {med}. \nO desvio padrão do custo foi de {std}.')

plt.boxplot(solutionsEsfera)

"""## Atividade 2 - Problema da Mochila"""

ds = np.load('/content/tcellsxldl.npy')
ds[i][0]

def CustoMochila(c,ds):
  a = c[0]
  b = c[1]
  rms_sum = 0

  for i in range(len(df)):
    y_pred = a*ds[i][0] + b
    rms = (y_pred - ds[i][1])**2
    rms_sum += rms

  return np.sqrt(rms_sum/len(df))

def apply_function(x):
  return -CustoMochila(x,ds)

len(df)

import time
generations = 10
d=2
boundaries = [[-1,1]]*d
rodadas = 5

positionsMochila = []
solutionsMochila = []

for i in range(rodadas):
  print('Rodada número: ',i+1)
  time1 = time.time()

  RunGA(generations=generations, dimensions=d, boundaries=boundaries,
        positions=positionsMochila, solutions=solutionsMochila,size=20)
  # # RunGA(gene,d,boundaries, size = 1, positions = positionsMochila, solutions = solutionsMochila)
  time2 = time.time()
  print('Iteração foi executada em ', time2-time1, ' segundos.')
display(positionsMochila, solutionsMochila)

plt.boxplot(solutionsMochila)

med = np.mean(solutionsMochila)
std = np.std(solutionsMochila)

print(f'O custo médio das soluções foi de {med}. \nO desvio padrão do custo foi de {std}.')

#Melhores Soluções
df = pd.DataFrame(data = {'x':[x[0] for x in positionsMochila], 
                          'y':[x[1] for x in positionsMochila],
                          'solution':solutionsMochila})

df.sort_values('solution', ascending=False).head(3)

df = np.load('/content/tcellsxldl.npy')
df = pd.DataFrame(df,columns = ['T', 'LDL'])

xmin, xmax = -0.15, 0.2

pos = [0.9612072888940817, 0.0068310648700784515] 

func = np.array([[xmin, pos[0]*xmin + pos[1]],
        [xmax, pos[0]*xmax + pos[1]]])

plt.scatter(np.array(df['T']),np.array(df['LDL']))
plt.plot(func[:,0], func[:,1], color='r')
plt.show()