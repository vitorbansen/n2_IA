import numpy as np
import random

# Definindo parâmetros do algoritmo genético
POPULATION_SIZE = 50
GENERATIONS = 100
MUTATION_RATE = 0.1
TOURNAMENT_SIZE = 5
NUM_RULES = 14  # Número de regras

# Função de fitness
def evaluate_fitness(rules):
    # Simulação com as regras fornecidas e retorno de um valor de fitness
    total_time = simulate_pendulum(rules)
    return total_time

def simulate_pendulum(rules):
    # Aqui você deve incluir a lógica de simulação do pêndulo usando as regras
    # Exemplo de uma simulação simples que retorna o tempo até a estabilização
    # (Esta função deve ser implementada de acordo com seu sistema)
    return random.uniform(10, 100)  # Valor fictício para a simulação

# Criação da população inicial
def initialize_population():
    return [create_random_rules() for _ in range(POPULATION_SIZE)]

# Criação de regras aleatórias
def create_random_rules():
    return [random.uniform(-1, 1) for _ in range(NUM_RULES)]  # Ajustar os limites conforme necessário

# Seleção
def tournament_selection(population):
    tournament = random.sample(population, TOURNAMENT_SIZE)
    return min(tournament, key=evaluate_fitness)

# Cruzamento
def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    return parent1[:point] + parent2[point:]

# Mutação
def mutate(individual):
    for i in range(len(individual)):
        if random.random() < MUTATION_RATE:
            individual[i] = random.uniform(-1, 1)  # Ajustar conforme necessário

# Algoritmo Genético
def genetic_algorithm():
    population = initialize_population()
    
    for generation in range(GENERATIONS):
        new_population = []
        
        for _ in range(POPULATION_SIZE):
            parent1 = tournament_selection(population)
            parent2 = tournament_selection(population)
            child = crossover(parent1, parent2)
            mutate(child)
            new_population.append(child)
        
        population = new_population
    
    # Melhor indivíduo após as gerações
    best_individual = min(population, key=evaluate_fitness)
    return best_individual

# Executar o Algoritmo Genético
best_rules = genetic_algorithm()
print(f"Melhores regras encontradas: {best_rules}")
