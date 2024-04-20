from gpiozero import SPI
from time import sleep

spi = SPI(clock_pin=11, MOSI_pin=10, MISO_pin=9, select_pin=8, clock_mode=0, max_speed_hz=1000000)

try:
    while True:
        datos_recibidos = spi.receive_bytes(5)
        print("Datos recibidos:", datos_recibidos)
        sleep(1)

except KeyboardInterrupt:
    spi.close()
