import RPi.GPIO as GPIO
import time
import MyLibraries.Freenove_DHT as DHT
import sys

# Definir pines que se van a usar
LED_PIN0 = 38    # GPIO 20, blue
LED_PIN1 = 40    # GPIO 21, red

BTN_PIN = 12     # GPIO 18

HYT_PIN = 11     # GPIO 17

RED = True
STOP_THREADS = False


def setup():
    # Usar nombres fisicos
    GPIO.setmode(GPIO.BOARD)
    # Conectar con LEDs
    GPIO.setup(LED_PIN0, GPIO.OUT)
    GPIO.setup(LED_PIN1, GPIO.OUT)
    # Conectar boton y añadir interrupcion
    GPIO.setup(BTN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BTN_PIN, GPIO.FALLING, 
                          callback=btn_pressed, bouncetime=200)

def btn_pressed(arg=None):
    global RED

    if RED:
        RED = False
        GPIO.output(LED_PIN0, GPIO.HIGH) # blue high
        GPIO.output(LED_PIN1, GPIO.LOW) # red low
    else:
        RED = True
        GPIO.output(LED_PIN0, GPIO.LOW) # blue low
        GPIO.output(LED_PIN1, GPIO.HIGH) # red high

def main():
    global RED, STOP_THREADS
    # Params
    GPIO.output(LED_PIN1, GPIO.HIGH) # red high
    GPIO.output(LED_PIN0, GPIO.LOW) # blue low
    # Inicializar el higrotermometro
    dht_termo = DHT.DHT(HYT_PIN)

    # Bucle principal
    while not STOP_THREADS:
        # 15 intentos de lectura (internos)
        data_check = dht_termo.readDHT11()
        if data_check is not dht_termo.DHTLIB_OK:
            continue
        # ------------------------------
        if RED:
            print("Lectura de temperatura: ", dht_termo.temperature)
        else:
            print("Lectura de humedad: ", dht_termo.humidity)    
        time.sleep(1)



if __name__ == "__main__":
    try:
        setup()
        main()
    except KeyboardInterrupt:
        STOP_THREADS = True
        GPIO.cleanup()
        sys.exit("\nPrograma finalizado")

