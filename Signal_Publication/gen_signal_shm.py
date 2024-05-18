import sys
import numpy as np
import pyqtgraph as pg
import struct
import array
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication
from multiprocessing import shared_memory
import signal

MEMORY_NAME = "shm_temp_humidity"
MEMORY_SIZE = 2048

STOP_THREADS = False

# Define arrays of data
T_ARRAY = np.linspace(0, 1, 2)  # 50s, Ts = 50ms (20 samples per second)
X_ARRAY = np.zeros(2)
# Sample pointer and data to send
SAMPLE = 0
Temperature = 0.0
Humidity = 0 
Time = 0
SampleTime = 0.2

DATAHum = np.vstack((T_ARRAY, X_ARRAY)).T
DATATemp = np.vstack((T_ARRAY, X_ARRAY)).T

def float_to_hex(val):
    return hex(struct.unpack('<I', struct.pack('<f', val))[0])

def update():
    global shm, curvaHum, curvaTemp, SAMPLE, Temperature,Humidity,Time ,DATAHum,DATATemp
    
    Time = 1.0 + (SAMPLE * SampleTime)
    
    Humidity = shm.buf[0]
    newDataHum   = np.array([[Time,Humidity]])
    DATAHum = np.concatenate((DATAHum,newDataHum),axis = 0)
    curvaHum.setData(DATAHum[:SAMPLE + 1])
    
    Temperature = float(shm.buf[4])+ (float(shm.buf[8])/100.0)
    newDataTemp  = np.array([[Time,Temperature]])
    DATATemp = np.concatenate((DATATemp,newDataTemp),axis = 0)
    curvaTemp.setData(DATATemp[:SAMPLE + 1])
    
    SAMPLE = (SAMPLE + 1)

def setup_shared_memory():
    try:
        shm_a = shared_memory.SharedMemory(name=MEMORY_NAME, create=False, size=MEMORY_SIZE)
        shm_a.unlink()
        shm_a = shared_memory.SharedMemory(name=MEMORY_NAME, create=True, size=MEMORY_SIZE)
    except FileNotFoundError:
        shm_a = shared_memory.SharedMemory(name=MEMORY_NAME, create=True, size=MEMORY_SIZE)
    return shm_a

def cleanup():
    global STOP_THREADS, qtimer, shm
    STOP_THREADS = True
    qtimer.stop()
    print("Timer stopped")
    shm.unlink()
    print("Shared memory unlinked")

def signal_handler(sig, frame):
    cleanup()
    sys.exit(0)

def main():
    global shm, curvaHum, curvaTemp, SAMPLE, qtimer ,DATAHum ,DATATemp

    # Set up shared memory
    shm = setup_shared_memory()

    # Create QApplication instance
    app = QApplication(sys.argv)
    
    plot_window = pg.GraphicsLayoutWidget(show=True)
    plot1 = plot_window.addPlot(title="Señal Humedad")
    curvaHum = plot1.plot(pen='b')
    plot2 = plot_window.addPlot(title="Señal Temperatura")
    curvaTemp = plot2.plot(pen='r')
    # Initialize timer
    qtimer = QTimer()
    qtimer.timeout.connect(update)
    
    # Start timer with interval of 50ms
    qtimer.start(1000)
    
    print("Timer started")

    # Ensure cleanup is called on exit
    app.aboutToQuit.connect(cleanup)

    # Set up signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    # Execute application
    try:
        sys.exit(app.exec_())
    except Exception as err:
        cleanup()
        sys.exit(f"Program terminated with error: {err}")

if __name__ == '__main__':
    main()
