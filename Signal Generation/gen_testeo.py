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


def init():
    # Iniciar app (necesario?)
    qapp = QtWidgets.QApplication(sys.argv)
    # Inicializar timer
    qtimer = QtCore.QTimer()
    interval_ms = 50
    qtimer.setInterval(interval_ms)
    # Conectar timeout a la funcion update
    qtimer.timeout.connect(update)
    return qtimer, qapp


def update():
    global SAMPLE, T_TO_SEND, X_TO_SEND, curva, DATA #UPDATE_FLAG
    T_TO_SEND = T_ARRAY[SAMPLE]
    X_TO_SEND = X_ARRAY[SAMPLE]
    curva.setData(DATA[:SAMPLE + 1])
    SAMPLE += 1
    #UPDATE_FLAG = True


def main():
    global SAMPLE, T_TO_SEND, X_TO_SEND, UPDATE_FLAG, curva
    t_arr, x_arr = np.zeros(1000), np.zeros(1000)

    # Iniciar app
    qapp = QtWidgets.QApplication(sys.argv)
    plot_window = pg.GraphicsLayoutWidget(show=True)
    plot1 = plot_window.addPlot(title="Señal captada")
    # plot1.plot(x=T_ARRAY, y=X_ARRAY) esto funciona
    curva = plot1.plot(pen='y')

    # Inicializar timer
    qtimer = QtCore.QTimer()
    #interval_ms = 50
    #qtimer.setInterval(interval_ms)
    # Conectar timeout a la funcion update
    qtimer.timeout.connect(update)
    qtimer.start(50)
    pg.exec()

    """while not UPDATE_FLAG:  # Wait for the first update
        QtCore.QCoreApplication.processEvents()

    try:
        while True:
            if UPDATE_FLAG:
                # Graficar arrays x, y
                UPDATE_FLAG = False
                t_arr[SAMPLE] = T_TO_SEND
                x_arr[SAMPLE] = X_TO_SEND
                plot1.plot(t_arr[:SAMPLE + 1], x_arr[SAMPLE + 1])
                qapp.processEvents()
    except KeyboardInterrupt:
        sys.exit("Programa finalizado")"""


if __name__ == '__main__':
    main()

"""if __name__ == '__main__':
    main()
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QGuiApplication.instance().exec_()"""
