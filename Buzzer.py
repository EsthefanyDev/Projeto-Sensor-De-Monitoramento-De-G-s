import machine
import time

# Configura o pino D5 como PWM
buzzer = machine.PWM(machine.Pin(14))  # D5 é GPIO 14 no ESP8266

def tocar_buzzer(frequencia=1000):  # Frequência padrão de 1000 Hz
    buzzer.freq(frequencia)  # Define a frequência do buzzer
    buzzer.duty(100)  # Define a intensidade (valor entre 0 e 1023)
    time.sleep(3)  # O buzzer tocará por 10 segundos
    buzzer.duty(0)  # Desliga o buzzer


# Chama a função para tocar o buzzer
tocar_buzzer()
