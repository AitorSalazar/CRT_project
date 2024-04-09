import spidev
import time
import sys

# Crear objeto SPI
spi = spidev.SpiDev()

# Abrir bus 0, dispositivo 0
spi.open(0, 0)

# Elegir modo y frecuencia
# spi.max_speed_hz = 500000
spi.mode = 0

try:
    while True:
        # Protocolo handshake
        spi.xfer2([0xff])
        time.sleep(0.1)
        # Enviar datos
        data = [0xfa, 0xaa, 0x40]
        spi.writebytes(data)
        print(data)

        # Esperar
        time.sleep(0.1)
except KeyboardInterrupt:
    print('\n')
    spi.close()
    sys.exit()
