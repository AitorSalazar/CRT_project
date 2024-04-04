import pigpio
import numpy as np
from PyQt5 import QtWidgets 
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore

# Inicializar pigpio
pi = pigpio.pi()

# Configuración de la señal
frequency = 1000  # Frecuencia de la señal en Hz
sampling_rate = 10000  # Tasa de muestreo en Hz
amplitude = 1.0  # Amplitud de la señal

# Generar la señal sinusoidal
t = np.arange(0, 1, 1/sampling_rate)
signal = amplitude * np.sin(2 * np.pi * frequency * t)
s = 0
# Configurar la comunicación SPI
spi_channel = 0
spi_speed = 1000000  # Velocidad de la comunicación SPI en Hz
spi = pi.spi_open(spi_channel, spi_speed)
print("SPI channel opened")
# Publicar la señal utilizando SPI

# Configuración de la ventana de visualización

MyPlot = pg.plot()
MyPlot.plot(t,signal)
print(len(signal))
print(len(t))

# Función para actualizar la señal en la ventana de visualización
def update():
    global signal
    global s
    send_sample (signal[s])
    print(signal[s])

def send_sample(sample):
    data = (int(127.5 * (1.0 + sample))) # Convertir la señal a valores de 0-255
    pi.spi_xfer(spi, data)
    MyPlot.setData(sample)
    print("new Sample")

# Configurar un temporizador para actualizar la señal en la ventana de visualización
# timer = QtCore.QTimer()
# timer.timeout.connect(update)

# timer.start(500)  # Actualizar cada 50 ms

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QGuiApplication.instance().exec()

# Ejecutar la aplicación
# app.exec_()

# Detener la comunicación SPI y cerrar la conexión con pigpio
pi.spi_close(spi)
pi.stop()
