import numpy as np
import pyqtgraph as pg
import spidev
import struct
from pyqtgraph.Qt import QtCore


# Definir arrays de datos
T_ARRAY = np.linspace(0, 50, 1000)  # 50s, Ts = 50ms (20 muestras por segundo)
X_ARRAY = np.random.rand(1000) * 100
# Apuntador de muestra y datos a enviar
SAMPLE = 0
T_TO_SEND, X_TO_SEND = 0, 0
# Objeto spi
spi = spidev.SpiDev()
# Abrir SPI en bus 0, equipo 0
spi.open(0, 0)

def float_to_hex(val):
    return hex(struct.unpack('<I', struct.pack('<f', val))[0])


def update():
    global SAMPLE, T_TO_SEND, X_TO_SEND
    # Muestrear datos
    T_TO_SEND = float_to_hex(T_ARRAY[SAMPLE])
    X_TO_SEND = float_to_hex(X_ARRAY[SAMPLE])
    # Enviar datos con SPI
    spi.xfer2([T_TO_SEND, X_TO_SEND])
    # Probar tambien con este
    #spi.writebytes([T_TO_SEND, X_TO_SEND])
    SAMPLE += 1


def main():
    global SAMPLE, T_TO_SEND, X_TO_SEND
    
    try:
        # Inicializar timer
        qtimer = QtCore.QTimer()
        # Conectar timeout a la funcion update
        qtimer.timeout.connect(update)
        # Iniciar timer con intervalo de 50ms
        qtimer.start(50)
        pg.exec()
    except KeyboardInterrupt:
        spi.close()



if __name__ == '__main__':
    main()
