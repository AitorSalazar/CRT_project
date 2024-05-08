import RPi.GPIO as GPIO
import time
import MyLibraries.Freenove_DHT as DHT
import sys

# Definir pines que se van a usar
LED_PIN0 = 38    # GPIO 20, blue
LED_PIN1 = 40    # GPIO 21, red

BTN_PIN = 12     # GPIO 18

HYT_PIN = 11     # GPIO 17


def setup():
    # Usar nombres fisicos
    GPIO.setmode(GPIO.BOARD)
    # Conectar con LEDs
    GPIO.setup(LED_PIN0, GPIO.OUT)
    GPIO.setup(LED_PIN1, GPIO.OUT)
    # Conectar boton
    GPIO.setup(BTN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def main():
    # Params
    red = True
    btn_pressed = False
    GPIO.output(LED_PIN1, GPIO.HIGH) # red high
    GPIO.output(LED_PIN0, GPIO.LOW) # blue low
    # Inicializar el higrotermometro
    dht_termo = DHT.DHT(HYT_PIN)

    # Bucle principal
    while(True):
        # 15 intentos de lectura (internos)
        data_check = dht_termo.readDHT11()
        if data_check is not dht_termo.DHTLIB_OK:
            continue
        if GPIO.input(BTN_PIN) == GPIO.LOW:
            btn_pressed = True
            if red:
                red = False
                GPIO.output(LED_PIN0, GPIO.HIGH) # blue high
                GPIO.output(LED_PIN1, GPIO.LOW) # red low
            else:
                red = True
                GPIO.output(LED_PIN0, GPIO.LOW) # blue low
                GPIO.output(LED_PIN1, GPIO.HIGH) # red high
        else:
            btn_pressed = False
        # ------------------------------
        if red:
            print("Lectura de temperatura: ", dht_termo.temperature)
        else:
            print("Lectura de humedad: ", dht_termo.humidity)    
        time.sleep(0.5)



if __name__ == "__main__":
    try:
        setup()
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
        sys.exit("\nPrograma finalizado")

