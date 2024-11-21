import machine
import time

# Configuração do pino do sensor de gás
sensor_gas = machine.ADC(0)  # Conecte o MQ-8 ao pino A0


# Função para ler o sensor de gás
def ler_sensor_gas():
    return sensor_gas.read()  # Lê o valor do sensor


# Função principal para monitorar o sensor de gás
def monitorar_gas():
    while True:
        valor_gas = ler_sensor_gas()
        print('Valor do sensor de gás:', valor_gas)
        time.sleep(1)  # Atraso de 1 segundo entre leituras


# Iniciar o monitoramento do sensor de gás
monitorar_gas()
