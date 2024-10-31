import numpy as np
import neuro_fuzzy_model

# Teste do sistema Neuro-Fuzzy
def test_neuro_fuzzy_system(model):
    # Teste com novos valores
    theta_test = 15
    omega_test = 5
    
    input_data = np.array([[theta_test, omega_test]])
    v_output = model.predict(input_data)
    print(f"Controle do carro (Neuro-Fuzzy): {v_output}")

# Executar teste
test_neuro_fuzzy_system(neuro_fuzzy_model)
