import numpy as np
import skfuzzy as fuzz
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split

# Definindo o universo de discurso e conjuntos de pertinência
def define_fuzzy_sets():
    theta = np.linspace(-180, 180, 360)
    omega = np.linspace(-60, 60, 360)
    
    # Conjuntos de pertinência para o ângulo do pêndulo
    theta_ng = fuzz.trimf(theta, [-180, -180, 0])
    theta_nm = fuzz.trimf(theta, [-180, 0, 180])
    theta_z = fuzz.trimf(theta, [-10, 0, 10])
    theta_pm = fuzz.trimf(theta, [0, 180, 180])
    theta_pg = fuzz.trimf(theta, [0, 180, 180])

    # Conjuntos de pertinência para a velocidade angular
    omega_n = fuzz.trimf(omega, [-60, -60, 0])
    omega_z = fuzz.trimf(omega, [-10, 0, 10])
    omega_p = fuzz.trimf(omega, [0, 60, 60])
    
    return theta, omega, theta_ng, theta_nm, theta_z, theta_pm, theta_pg, omega_n, omega_z, omega_p

# Função de controle fuzzy
def fuzzy_control(theta_val, omega_val):
    theta, omega, theta_ng, theta_nm, theta_z, theta_pm, theta_pg, omega_n, omega_z, omega_p = define_fuzzy_sets()

    # Fuzzificação
    theta_level_ng = fuzz.interp_membership(theta, theta_ng, theta_val)
    theta_level_nm = fuzz.interp_membership(theta, theta_nm, theta_val)
    theta_level_z = fuzz.interp_membership(theta, theta_z, theta_val)
    theta_level_pm = fuzz.interp_membership(theta, theta_pm, theta_val)
    theta_level_pg = fuzz.interp_membership(theta, theta_pg, theta_val)
    
    omega_level_n = fuzz.interp_membership(omega, omega_n, omega_val)
    omega_level_z = fuzz.interp_membership(omega, omega_z, omega_val)
    omega_level_p = fuzz.interp_membership(omega, omega_p, omega_val)

    # Aplicando as regras
    rule1 = np.fmin(theta_level_ng, omega_level_n)
    rule2 = np.fmin(theta_level_ng, omega_level_z)
    rule3 = np.fmin(theta_level_ng, omega_level_p)
    rule4 = np.fmin(theta_level_nm, omega_level_n)
    rule5 = np.fmin(theta_level_nm, omega_level_z)
    rule6 = np.fmin(theta_level_nm, omega_level_p)
    rule7 = np.fmin(theta_level_z, omega_level_n)
    rule8 = np.fmin(theta_level_z, omega_level_z)
    rule9 = np.fmin(theta_level_z, omega_level_p)
    rule10 = np.fmin(theta_level_pm, omega_level_n)
    rule11 = np.fmin(theta_level_pm, omega_level_z)
    rule12 = np.fmin(theta_level_pm, omega_level_p)
    rule13 = np.fmin(theta_level_pg, omega_level_n)
    rule14 = np.fmin(theta_level_pg, omega_level_z)

    # Conjuntos de saída para a velocidade do carro
    output_n = np.fmax(rule1, np.fmax(rule4, np.fmax(rule10, rule13)))
    output_z = np.fmax(rule2, np.fmax(rule5, np.fmax(rule8, rule11)))
    output_p = np.fmax(rule3, np.fmax(rule6, np.fmax(rule9, rule12)))

    # Defuzzificação
    v_output_n = fuzz.defuzz(omega, output_n, 'centroid')
    v_output_z = fuzz.defuzz(omega, output_z, 'centroid')
    v_output_p = fuzz.defuzz(omega, output_p, 'centroid')

    return v_output_n, v_output_z, v_output_p  # Retorna saídas

# Função para testar o sistema FIS com diferentes entradas
def test_fuzzy_system(test_cases):
    results = []
    for theta_test, omega_test in test_cases:
        v_outputs = fuzzy_control(theta_test, omega_test)
        results.append((theta_test, omega_test, v_outputs))
        print(f"Ângulo: {theta_test}, Velocidade Angular: {omega_test} => Controle do carro: {v_outputs}")

# Definindo casos de teste
test_cases = [
    (0, 0),
    (15, 5),
    (-30, -10),
    (45, 20),
    (90, -15),
    (-180, 60),
    (180, -60)
]

# Executar testes
test_fuzzy_system(test_cases)
