import RPi.GPIO as GPIO
import time
import MyLibraries.Freenove_DHT as DHT
from multiprocessing import shared_memory
import sys

# Definir pines que se van a usar
LED_PIN0 = 38    # GPIO 20, blue
LED_PIN1 = 40    # GPIO 21, red
BTN_PIN = 12     # GPIO 18
HYT_PIN = 11     # GPIO 17

# Constantes globales
MEMORY_NAME = "shm_temp_humidity"
MEMORY_SIZE = 2048

# Varibales globales 
RED = True
STOP_THREADS = False


def setup():
    """
    Setup function that initializes GPIO pins and assigns them their corresponding
    functions. It also sets up the button to enable interruptions and initializes 
    the shared memory.
    :returns: None
    """
    # Usar nombres fisicos
    GPIO.setmode(GPIO.BOARD)
    # Conectar con LEDs
    GPIO.setup(LED_PIN0, GPIO.OUT)
    GPIO.setup(LED_PIN1, GPIO.OUT)
    # Conectar boton y añadir interrupcion
    GPIO.setup(BTN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BTN_PIN, GPIO.FALLING, 
                          callback=btn_pressed, bouncetime=200)
    # Inicializar memoria compartida
    try:
        shm_a = shared_memory.SharedMemory(name=MEMORY_NAME, create=False,
                                           size=MEMORY_SIZE)
        shm_a.unlink()
        shm_a = shared_memory.SharedMemory(name=MEMORY_NAME, create=True,
                                       size=MEMORY_SIZE)
    except FileNotFoundError:
        shm_a = shared_memory.SharedMemory(name=MEMORY_NAME, create=True,
                                       size=MEMORY_SIZE)

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
    # Global params
    global RED, STOP_THREADS
    # Local params
    buf_pos = 0

    # Inicializar LEDs
    GPIO.output(LED_PIN1, GPIO.HIGH) # red high
    GPIO.output(LED_PIN0, GPIO.LOW) # blue low
    # Inicializar el higrotermometro
    dht_termo = DHT.DHT(HYT_PIN)
    # Conectar con memoria compartida
    shm = shared_memory.SharedMemory(name=MEMORY_NAME, create=False,
                                     size=MEMORY_SIZE)
    # Bucle principal
    try:
        while not STOP_THREADS:
            # 15 intentos de lectura (internos)
            data_check = dht_termo.readDHT11()
            if data_check is not dht_termo.DHTLIB_OK:
                continue
            # Guardar datos en memoria
            data_to_write = [dht_termo.temperature, dht_termo.humidity]
            for i in range(len(data_to_write)):
                # Temperatura es float
                if type(data_to_write[i]) == float:
                    numb = data_to_write[i]
                    # Temp -> 1) temp_entero, 2) temp_decimal
                    numb_to_write = [int(numb), int(10*(numb % 1))]
                    data_to_write.pop(i)
                    [data_to_write.insert(i + j, numb_to_write[j]) for j in range(len(numb_to_write))]
            for i in range(len(data_to_write)):
                shm.buf[buf_pos + i] = data_to_write[i]
            #data_to_write = bytearray(data_to_write)
            #shm.buf[:MEMORY_SIZE] = data_to_write # endpoint derecho del slice OBLIGTAORIO
            #read_bytes = bytes(shm.buf)
            #print(read_bytes[:30])
            if RED:
                print("Lectura de temperatura: ", dht_termo.temperature)
            else:
                print("Lectura de humedad: ", dht_termo.humidity)
            buf_pos += int(1*len(data_to_write)) # buf_pos += 3
            time.sleep(1)
    except KeyboardInterrupt:
        STOP_THREADS = True
        GPIO.cleanup()
        shm.unlink()
        sys.exit("\nPrograma finalizado")
    except Exception as err:
        STOP_THREADS = True
        GPIO.cleanup()
        shm.unlink()
        sys.exit(f"Programa finalizado con error {err}")



if __name__ == "__main__":
    setup()
    main()

