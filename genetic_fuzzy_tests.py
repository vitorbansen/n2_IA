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
    total_time = simulate_pendulum(rules)
    return total_time

def simulate_pendulum(rules):
    # Simulação fictícia que deve ser implementada
    # Retorna um valor baseado nas regras, simule o comportamento do pêndulo
    return random.uniform(10, 100)  # Exemplo fictício

# Criação da população inicial
def initialize_population():
    return [create_random_rules() for _ in range(POPULATION_SIZE)]

# Criação de regras aleatórias
def create_random_rules():
    return [random.uniform(-1, 1) for _ in range(NUM_RULES)]  # Ajustar limites conforme necessário

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
    
    best_individual = min(population, key=evaluate_fitness)
    return best_individual

# Integração das regras genéticas no sistema FIS
def fuzzy_control_with_genetic_rules(theta_val, omega_val, rules):
    # Use as regras otimizadas aqui para o controle
    # Implementar a lógica para o controle com as regras
    # Aqui você deve aplicar as regras ao sistema fuzzy
    v_output = sum(rules)  # Placeholder; substituir pela lógica real
    return v_output

# Teste do sistema otimizado
def test_genetic_fuzzy_system(best_rules):
    theta_test = 15  # Exemplo de ângulo
    omega_test = 5   # Exemplo de velocidade angular
    v_output = fuzzy_control_with_genetic_rules(theta_test, omega_test, best_rules)
    print(f"Controle do carro (Genético-Fuzzy): {v_output}")

# Executar o Algoritmo Genético
best_rules = genetic_algorithm()

# Executar teste
test_genetic_fuzzy_system(best_rules)
