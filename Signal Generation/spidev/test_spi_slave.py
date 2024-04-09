import spidev
import time
import sys


# Crear objeto spi
spi = spidev.SpiDev()

# Abrir bus 0, dispositivo 0
spi.open(0, 0)

# Elegir modo esclavo
spi.mode = 0

# Cantidad de bytes a leer
n = 3

try:
    while True:
        # Protocolo handshake
        handshake = spi.xfer2([0x00])
        
        if handshake == 0xff:
            # Recibir mensaje
            #resp = spi.readbytes(n)
            resp = spi.xfer2([0x00])
            print(f"Respuesta: {resp}")

        # Esperar
        #time.sleep(0.01)
except KeyboardInterrupt:
    print('\n')
    spi.close()
    sys.exit()

