import time
import network
import urequests
import machine
from machine import Pin

# # Informações da rede Wi-Fi
# ssid = 'NORTE GASES'
# password = 'NG271185'

ssid = 'ESTACIO-VISITANTES'
password = 'estacio@2014'

# ssid = 'Online.Rodrigo'
# password = 'Rodrigo21*'

# Informações para envio da mensagem
phone_number = '559185045312'
api_key = '7872715'

# Função para enviar mensagem via WhatsApp
def enviar_mensagem():
    url = f'https://api.callmebot.com/whatsapp.php?phone={phone_number}&text=VAZAMENTO+DE+GAS+DETECTADO&apikey={api_key}'
    try:
        response = urequests.get(url)
        if response.status_code == 200:
            print('Mensagem enviada com sucesso!')
        else:
            print('Erro no envio da mensagem:', response.status_code)
        response.close()
    except Exception as e:
        print('Erro ao enviar a mensagem:', e)

# Função para conectar ao Wi-Fi
def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Conectando ao WiFi...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            time.sleep(0.5)
            print('.', end='')
    print('\nConexão estabelecida, IP:', wlan.ifconfig()[0])

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
    valor_bruto = sensor_gas.read()
    valor_convertido = (valor_bruto / 1023) * 100  # Converte para percentual
    return valor_convertido

# Função para piscar LEDs vermelhos em alerta
def piscar_vermelho1():
    led_vermelho1.value(1)
    led_vermelho2.value(1)
    time.sleep(0.5)
    led_vermelho1.value(0)
    led_vermelho2.value(0)

# Função para piscar LEDs vermelhos em alerta muito perigoso
def piscar_vermelho2():
    led_vermelho1.value(1)
    time.sleep(0.5)
    led_vermelho1.value(0)
    led_vermelho2.value(1)
    time.sleep(0.5)
    led_vermelho2.value(0)

# Função para tocar o buzzer
def tocar_buzzer(frequencia=1000):
    buzzer.freq(frequencia)
    buzzer.duty(512)
    time.sleep(3)
    buzzer.duty(0)

# Função principal para monitorar o sensor de gás e controlar LEDs, buzzer e enviar alertas
def monitorar_gas():
    ultimo_envio = time.time()
    while True:
        valor_gas = ler_sensor_gas()
        print('Nível de gás detectado: {:.2f}%'.format(valor_gas))

        # Verifica se é hora de enviar os dados para o ThingSpeak (a cada 15 segundos)
        if time.time() - ultimo_envio >= 15:
            enviar_dados_thingspeak(valor_gas)
            ultimo_envio = time.time()

        # Limite ajustado para 40% de presença de gases inflamáveis ou fumaça
        if valor_gas > 40:
            print('Alerta: Nível perigoso de gás detectado!')
            enviar_mensagem()  # Envia alerta via WhatsApp
            piscar_vermelho1()
            tocar_buzzer()

            led_verde1.value(0)
            led_verde2.value(0)

            # Limite ajustado para 60% de presença de gases inflamáveis ou fumaça
            if valor_gas > 60:
                print('Alerta: Nível muito perigoso de gás detectado!')
                enviar_mensagem()
                piscar_vermelho2()
                tocar_buzzer()

        else:
            print('Nível de gás seguro.')
            led_verde1.value(1)
            led_verde2.value(1)
            led_vermelho1.value(0)
            led_vermelho2.value(0)

        time.sleep(3)

# Conectar ao Wi-Fi
conectar_wifi()

# Iniciar o monitoramento do sensor de gás
monitorar_gas()
