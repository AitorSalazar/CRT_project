import numpy as np
import struct
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui

"""test_array_1 = np.zeros((2, 2))
test_array_2 = np.arange(4).reshape(2, 2)
test_array_3 = np.linspace(0, 2 * np.pi, 100)"""
test_f_3 = np.zeros(100)
f = 1 / 10
dc = 0.5

count_length = int(len(test_f_3) * f)
cycles = int(1 / f)
high, low = int(count_length * dc), int(count_length * (1 - dc))
for i in range(cycles):
    i_scaled = i * count_length
    test_f_3[i_scaled: i_scaled + low - 1] = 0
    test_f_3[i_scaled + low: i_scaled + low + high] = 1

"""x = np.linspace(0, 10, 100)
y = test_f_3
# Crear ventana de ploteo
MyPlot = pg.plot()
# Graficar arrays x, y
MyPlot.plot(x, y)
# Codigo para inicializar Event Loop del GUI de PyQT
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QGuiApplication.instance().exec_()"""


def float_to_hex(f):
    return hex(struct.unpack('<I', struct.pack('<f', f))[0])


def list_of_bytes(v_hex):
    v_bytearray = bytes.fromhex(v_hex[2:])
    byte_list = []
    for i in range(len(v_bytearray)):
        byte_list.append("0x" + "{:02x}".format(v_bytearray[i]))
    return byte_list


val = 1.25
val_hex = float_to_hex(val)
print(type(val_hex))
print(val_hex)
val_bytes = bytes.fromhex(val_hex[2:])
print(type(val_bytes))
print(val_bytes)
val_bytearray = bytearray.fromhex(val_hex[2:])
print(type(val_bytearray))
print(val_bytearray)
print("{:02x}".format(val_bytearray[0]))
b_list = list_of_bytes(val_hex)
b_list.extend(['1', 2])
