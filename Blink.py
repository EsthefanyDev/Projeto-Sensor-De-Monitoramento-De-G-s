from machine import Pin
from time import sleep

# Configuração dos pinos
led_verde1 = Pin(2, Pin.OUT)  # D4
led_verde2 = Pin(0, Pin.OUT)  # D3
led_vermelho1 = Pin(16, Pin.OUT)  # D0
led_vermelho2 = Pin(15, Pin.OUT)  # D8

def pisca_leds():
    while True:
        # Acende os LEDs
        led_verde1(1)
        led_verde2(1)
        sleep(1)  # 1 segundo
        led_verde1(0)  # Apaga os LEDs
        led_verde2(0)  # Apaga os LEDs

        led_vermelho1(1)
        sleep(1)  # 1 segundo
        led_vermelho1(0)  # Apaga os LEDs
        led_vermelho2(1)
        sleep(1)  # 1 segundo
        led_vermelho2(0)  # Apaga os LEDs

        led_vermelho1(1)
        sleep(1)  # 1 segundo
        led_vermelho1(0)  # Apaga os LEDs
        led_vermelho2(1)
        sleep(1)  # 1 segundo
        led_vermelho2(0)  # Apaga os LEDs
# Iniciar a função de piscar
pisca_leds()
