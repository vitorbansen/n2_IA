import numpy as np
import skfuzzy as fuzz
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split

# Definindo o universo de discurso e conjuntos de pertinência
def define_fuzzy_sets():
    # Definindo os conjuntos de pertinência
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

# Função para aplicar regras fuzzy
def some_fuzzy_rule(theta_val, omega_val):
    # Lógica para determinar a saída com base nas regras fuzzy
    if theta_val < -10:
        return -5  # Exemplo de saída para ângulo negativo
    elif theta_val > 10:
        return 5   # Exemplo de saída para ângulo positivo
    else:
        return 0   # Exemplo de saída para ângulo neutro

# Função para criar conjuntos de dados com Lógica Fuzzy
def create_dataset(num_samples):
    theta, omega, _, _, _, _, _, _, _, _ = define_fuzzy_sets()
    inputs = []
    outputs = []
    
    for _ in range(num_samples):
        # Geração de dados aleatórios para ângulo e velocidade
        theta_val = np.random.uniform(-180, 180)
        omega_val = np.random.uniform(-60, 60)
        
        # Fuzzificação
        v_output = some_fuzzy_rule(theta_val, omega_val)
        
        inputs.append([theta_val, omega_val])
        outputs.append(v_output)
    
    return np.array(inputs), np.array(outputs)

# Treinamento da Rede Neural
def train_neuro_fuzzy_model():
    X, y = create_dataset(1000)  # Geração de dados
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = MLPRegressor(hidden_layer_sizes=(10, 10), max_iter=1000, random_state=42)
    model.fit(X_train, y_train)

    score = model.score(X_test, y_test)
    print(f"Precisão do modelo: {score}")
    
    return model

# Função para testar o sistema Neuro-Fuzzy
def test_neuro_fuzzy_system(model, theta_test, omega_test):
    input_data = np.array([[theta_test, omega_test]])
    v_output = model.predict(input_data)
    print(f"Ângulo: {theta_test}, Velocidade Angular: {omega_test} => Controle do carro: {v_output[0]}")

# Executar o treinamento
neuro_fuzzy_model = train_neuro_fuzzy_model()

# Testar o sistema com um exemplo
test_neuro_fuzzy_system(neuro_fuzzy_model, 15, 5)  # Exemplo de ângulo e velocidade
