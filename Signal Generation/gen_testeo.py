import sys
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets

# Definir los BIGASS ARRAYS
T_ARRAY = np.linspace(0, 50, 1000)  # 50s, Ts = 50ms (20 muestras por segundo)
X_ARRAY = np.random.rand(1000) * 100

UPDATE_FLAG = False
SAMPLE = 0
T_TO_SEND, X_TO_SEND = 0, 0

DATA = np.vstack((T_ARRAY, X_ARRAY)).T
t_arr, x_arr = np.zeros(1000), np.zeros(1000)


def update():
    global SAMPLE, T_TO_SEND, X_TO_SEND, curva, DATA #UPDATE_FLAG
    T_TO_SEND = T_ARRAY[SAMPLE]
    X_TO_SEND = X_ARRAY[SAMPLE]
    curva.setData(DATA[:SAMPLE + 1])
    t_arr[SAMPLE] = T_TO_SEND
    x_arr[SAMPLE] = X_TO_SEND
    SAMPLE += 1
    #UPDATE_FLAG = True


def main():
    global SAMPLE, T_TO_SEND, X_TO_SEND, UPDATE_FLAG, curva

    plot_window = pg.GraphicsLayoutWidget(show=True)
    plot1 = plot_window.addPlot(title="Señal captada")
    # plot1.plot(x=T_ARRAY, y=X_ARRAY) esto funciona
    curva = plot1.plot(pen='y')

    # Inicializar timer
    qtimer = QtCore.QTimer()
    # Conectar timeout a la funcion update
    qtimer.timeout.connect(update)
    # Iniciar timer con intervalo de 50ms
    qtimer.start(50)
    pg.exec()
    print(t_arr, "\n", x_arr)


if __name__ == '__main__':
    main()

"""if __name__ == '__main__':
    main()
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QGuiApplication.instance().exec_()"""
