from time import sleep

import network
import time
from machine import Pin

# Configuração do LED
led = Pin(2, Pin.OUT)  # No ESP8266, o LED geralmente está no pino 2 (GPIO 2)

# Configuração da conexão Wi-Fi
ssid = 'Online.Rodrigo'
password = 'Rodrigo21'


# Função para conectar ao Wi-Fi
def conecta_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Conectando à rede...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            time.sleep(1)  # Aguarda um segundo para evitar loop rápido
    print('Conexão estabelecida. Endereço IP:', wlan.ifconfig())
    return wlan

# Função para piscar o LED
def piscar_led(wlan):
    while wlan.isconnected():  # Continua piscando enquanto conectado
        print('Conectado')
        sleep(1)
        led.value(not led.value())  # Inverte o estado do LED
        time.sleep(0.5)  # Atraso de 500ms
    led.off()  # Garante que o LED esteja desligado quando desconectar


# Conectar ao Wi-Fi
wlan = conecta_wifi()

# Piscar o LED enquanto estiver conectado
piscar_led(wlan)