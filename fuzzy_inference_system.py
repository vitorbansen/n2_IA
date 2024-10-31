import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

# Definição do universo de discurso
theta = np.linspace(-180, 180, 360)  # Ângulo do pêndulo
omega = np.linspace(-60, 60, 360)    # Velocidade angular
x = np.linspace(-10, 10, 360)        # Posição do carro
v = np.linspace(-10, 10, 360)        # Velocidade do carro

# Conjuntos de pertinência para o ângulo
theta_ng = fuzz.trimf(theta, [-180, -180, 0])
theta_nm = fuzz.trimf(theta, [-180, 0, 180])
theta_z = fuzz.trimf(theta, [-10, 0, 10])
theta_pm = fuzz.trimf(theta, [0, 180, 180])
theta_pg = fuzz.trimf(theta, [0, 180, 180])

# Conjuntos de pertinência para a velocidade angular
omega_n = fuzz.trimf(omega, [-60, -60, 0])
omega_z = fuzz.trimf(omega, [-10, 0, 10])
omega_p = fuzz.trimf(omega, [0, 60, 60])

# Conjuntos de pertinência para a posição do carro
x_n = fuzz.trimf(x, [-10, -10, 0])
x_z = fuzz.trimf(x, [-1, 0, 1])
x_p = fuzz.trimf(x, [0, 10, 10])

# Conjuntos de pertinência para a velocidade do carro
v_n = fuzz.trimf(v, [-10, -10, 0])
v_z = fuzz.trimf(v, [-1, 0, 1])
v_p = fuzz.trimf(v, [0, 10, 10])

# Avaliação das regras
def fuzzy_control(theta_val, omega_val, x_val):
    # Fuzzificação
    theta_level_ng = fuzz.interp_membership(theta, theta_ng, theta_val)
    theta_level_nm = fuzz.interp_membership(theta, theta_nm, theta_val)
    theta_level_z = fuzz.interp_membership(theta, theta_z, theta_val)
    theta_level_pm = fuzz.interp_membership(theta, theta_pm, theta_val)
    theta_level_pg = fuzz.interp_membership(theta, theta_pg, theta_val)
    
    omega_level_n = fuzz.interp_membership(omega, omega_n, omega_val)
    omega_level_z = fuzz.interp_membership(omega, omega_z, omega_val)
    omega_level_p = fuzz.interp_membership(omega, omega_p, omega_val)

    # Fuzzificação para a posição do carro
    x_level_n = fuzz.interp_membership(x, x_n, x_val)
    x_level_z = fuzz.interp_membership(x, x_z, x_val)
    x_level_p = fuzz.interp_membership(x, x_p, x_val)

    # Aplicando as regras
    rule1 = np.fmin(x_level_n, np.fmin(theta_level_ng, omega_level_p))  # Regras para quando o carro está na esquerda e indo para a direita
    rule2 = np.fmin(x_level_n, np.fmin(theta_level_ng, omega_level_z))  # Regras para quando o carro está na esquerda e parado
    rule3 = np.fmin(x_level_n, np.fmin(theta_level_ng, omega_level_n))  # Regras para quando o carro está na esquerda e indo para a esquerda
    rule4 = np.fmin(x_level_z, np.fmin(theta_level_nm, omega_level_p))  # Regras para quando o carro está centralizado e indo para a direita
    rule5 = np.fmin(x_level_z, np.fmin(theta_level_nm, omega_level_z))  # Regras para quando o carro está centralizado e parado
    rule6 = np.fmin(x_level_z, np.fmin(theta_level_nm, omega_level_n))  # Regras para quando o carro está centralizado e indo para a esquerda
    rule7 = np.fmin(x_level_p, np.fmin(theta_level_pm, omega_level_n))  # Regras para quando o carro está na direita e indo para a esquerda
    rule8 = np.fmin(x_level_p, np.fmin(theta_level_pm, omega_level_z))  # Regras para quando o carro está na direita e parado
    rule9 = np.fmin(x_level_p, np.fmin(theta_level_pm, omega_level_p))  # Regras para quando o carro está na direita e indo para a direita

    # Conjuntos de saída para a velocidade do carro
    output_n = np.fmax(rule1, np.fmax(rule3, np.fmax(rule7, rule8)))
    output_z = np.fmax(rule2, np.fmax(rule4, np.fmax(rule5, rule6)))
    output_p = np.fmax(rule9, np.fmax(rule1, np.fmax(rule2, rule3)))

    # Defuzzificação
    v0 = fuzz.defuzz(v, output_n, 'centroid')
    v1 = fuzz.defuzz(v, output_z, 'centroid')
    v2 = fuzz.defuzz(v, output_p, 'centroid')
    
    return v0, v1, v2

# Teste do sistema FIS
theta_test = 15  # exemplo de ângulo
omega_test = 5   # exemplo de velocidade angular
x_test = -5      # exemplo de posição do carro
v_outputs = fuzzy_control(theta_test, omega_test, x_test)
print(f"Controle do carro: {v_outputs}")

# Visualização das funções de pertinência
plt.figure(figsize=(10, 8))
plt.subplot(2, 2, 1)
plt.title("Ângulo do Pêndulo")
plt.plot(theta, theta_ng, 'b', label='NG')
plt.plot(theta, theta_nm, 'g', label='NM')
plt.plot(theta, theta_z, 'r', label='Z')
plt.plot(theta, theta_pm, 'y', label='PM')
plt.plot(theta, theta_pg, 'm', label='PG')
plt.legend()

plt.subplot(2, 2, 2)
plt.title("Velocidade Angular")
plt.plot(omega, omega_n, 'b', label='N')
plt.plot(omega, omega_z, 'g', label='Z')
plt.plot(omega, omega_p, 'r', label='P')
plt.legend()

plt.subplot(2, 2, 3)
plt.title("Posição do Carro")
plt.plot(x, x_n, 'b', label='N')
plt.plot(x, x_z, 'g', label='Z')
plt.plot(x, x_p, 'r', label='P')
plt.legend()

plt.subplot(2, 2, 4)
plt.title("Velocidade do Carro")
plt.plot(v, v_n, 'b', label='N')
plt.plot(v, v_z, 'g', label='Z')
plt.plot(v, v_p, 'r', label='P')
plt.legend()

plt.tight_layout()
plt.show()
