import time
import machine
import urequests
from machine import Pin

# Configuração do Wi-Fi
import network

ssid = 'Online.Rodrigo'
password = 'Rodrigo21'


def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Conectando ao WiFi...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print('Conexão estabelecida:', wlan.ifconfig())


# Configuração do pino do sensor de gás
sensor_gas = machine.ADC(0)  # Conecte o MQ-8 ao pino A0

# Configuração do buzzer (D5 - GPIO 14)
buzzer = machine.PWM(machine.Pin(14))  # D5 é GPIO 14 no ESP8266

# Configuração dos LEDs (D6 e D7)
led_verde1 = Pin(2, Pin.OUT)  # D4
led_verde2 = Pin(0, Pin.OUT)  # D3
led_vermelho1 = Pin(16, Pin.OUT)  # D0
led_vermelho2 = Pin(15, Pin.OUT)  # D8

# Configuração do ThingSpeak
THINGSPEAK_URL = "http://api.thingspeak.com/update"
CHANNEL_KEY = "TRY5MM6Z4GJSHFP8"


# Função para enviar dados ao ThingSpeak
def enviar_dados_thingspeak(valor_gas):
    try:
        resposta = urequests.get(THINGSPEAK_URL + "?api_key=" + CHANNEL_KEY + "&field1=" + str(valor_gas))
        print('Dados enviados ao ThingSpeak:', resposta.text)
        resposta.close()
    except Exception as e:
        print('Falha ao enviar dados:', e)


# Função para ler o sensor de gás
def ler_sensor_gas():
    valor_bruto = sensor_gas.read()  # Lê o valor do sensor
    # Converter o valor bruto para uma escala mais significativa (percentual)
    valor_convertido = (valor_bruto / 1023) * 100  # Converte para percentual
    return valor_convertido


# Função para piscar os LEDs vermelhos em alerta
def piscar_vermelho1():
    led_vermelho1.value(1)
    led_vermelho2.value(1)
    time.sleep(0.5)
    led_vermelho1.value(0)
    led_vermelho2.value(0)


# Função para piscar os LEDs vermelhos em alerta muito perigoso
def piscar_vermelho2():
    led_vermelho1.value(1)
    time.sleep(0.5)
    led_vermelho1.value(0)
    led_vermelho2.value(1)
    time.sleep(0.5)
    led_vermelho2.value(0)
    led_vermelho1.value(1)


# Função para tocar o buzzer
def tocar_buzzer(frequencia=1000):  # Frequência padrão de 1000 Hz
    buzzer.freq(frequencia)  # Define a frequência do buzzer
    buzzer.duty(512)  # Define a intensidade (valor entre 0 e 1023)
    time.sleep(3)  # O buzzer tocará por 3 segundos
    buzzer.duty(0)  # Desliga o buzzer


# Função principal para monitorar o sensor de gás e controlar LEDs e buzzer
def monitorar_gas():
    ultimo_envio = time.time()  # Marca o tempo do último envio
    while True:
        valor_gas = ler_sensor_gas()
        print('Nível de gás detectado: {:.2f}%'.format(valor_gas))

        # Verifica se é hora de enviar os dados para o ThingSpeak (a cada 15 segundos)
        if time.time() - ultimo_envio >= 15:
            enviar_dados_thingspeak(valor_gas)
            ultimo_envio = time.time()  # Atualiza o tempo do último envio

        # Limite ajustado para 25% de presença de gases inflamáveis ou fumaça
        if valor_gas > 40:  # Limite de alerta
            print('Alerta: Nível perigoso de gás detectado!')

            piscar_vermelho1()

            tocar_buzzer()  # Ativa o buzzer por 3 segundos

            led_verde1.value(0)  # Apaga o LED verde 1
            led_verde2.value(0)  # Apaga o LED verde 2

            # Limite ajustado para 35% de presença de gases inflamáveis ou fumaça
            if valor_gas > 60:  # Limite de alerta
                print('Alerta: Nível perigoso de gás detectado!')

                piscar_vermelho2()

                tocar_buzzer()  # Ativa o buzzer por 3 segundos

                led_verde1.value(0)  # Apaga o LED verde 1
                led_verde2.value(0)  # Apaga o LED verde 2

        else:
            print('Nível de gás seguro.')
            led_verde1.value(1)  # Acende o LED verde 1
            led_verde2.value(1)  # Acende o LED verde 2
            led_vermelho1.value(0)  # Apaga o LED vermelho 1
            led_vermelho2.value(0)  # Apaga o LED vermelho 2

        time.sleep(3)  # Atraso de 1 segundo entre leituras do sensor


# Conectar ao Wi-Fi
conectar_wifi()

# Iniciar o monitoramento do sensor de gás
monitorar_gas()
