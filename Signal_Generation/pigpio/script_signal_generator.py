import pigpio
import sys
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore,QtWidgets 


################### Funciones auxiliares ####################

def build_signal ():

    # Configuración de la señal
    frequency = 1000  # Frecuencia de la señal en Hz
    amplitude = 1.0  # Amplitud de la señal
    X_ARRAY =  amplitude * np.sin(2 * np.pi * frequency * T_ARRAY)
    return X_ARRAY

def update():
    global SAMPLE, T_TO_SEND, X_TO_SEND, curva, DATA #UPDATE_FLAG
    #Coger un valor de los arrays y meterlo en el plot y enviarlo
    T_TO_SEND = T_ARRAY[SAMPLE]
    X_TO_SEND = X_ARRAY[SAMPLE]
    curva.setData(DATA[:SAMPLE + 1])
    SAMPLE += 1
    print(SAMPLE)
    pi.spi_xfer(spi, "hello")
    # pi.spi_xfer(spi, T_TO_SEND)
    # pi.spi_xfer(spi, X_TO_SEND)
#################### Función pricipal ##########################

T_ARRAY = np.linspace(0, 50, 1000)  # 50s, Ts = 50ms (20 muestras por segundo)
X_ARRAY = build_signal()
SAMPLE = 0
T_TO_SEND, X_TO_SEND = 0, 0

DATA = np.vstack((T_ARRAY, X_ARRAY)).T 
#el .T es para la traspuestas entonces son como :
# X_Array -- T_Array
#     x0         t0
#     x1         t1
#     x2         t2
#     x3         t3


pi = pigpio.pi()
# Configurar la comunicación SPI
spi_channel = 0
spi_speed = 1000000  # Velocidad de la comunicación SPI en Hz
spi = pi.spi_open(spi_channel, spi_speed)

def main():
    #Definir variables globales
    global SAMPLE, T_TO_SEND, X_TO_SEND,curva,spi
    #iniciar la ventana
    myApp = QtWidgets.QApplication(sys.argv)
    plot_widget = pg.GraphicsLayoutWidget(show=True)
    myPlot = plot_widget.addPlot(title = "Señal captada")
    curva = myPlot.plot(pen='y')

    #iniciar Qtimer
    qTimer = QtCore.QTimer()
    qTimer.timeout.connect(update)
    qTimer.start(50) 
    #Ejecutar programa
    pg.exec()

if __name__ == "__main__":
    main()

# Detener la comunicación SPI y cerrar la conexión con pigpio
pi.spi_close(spi)
pi.stop()