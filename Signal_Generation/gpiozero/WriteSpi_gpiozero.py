from gpiozero import SPI
from time import sleep

spi = SPI(clock_pin=11, MOSI_pin=10, MISO_pin=9, select_pin=8, clock_mode=0, max_speed_hz=1000000)

try:
    while True:
        datos = [0x01, 0x02, 0x03, 0x04, 0x05]
        spi.send_bytes(*datos)
        sleep(1)

except KeyboardInterrupt:
    spi.close()
