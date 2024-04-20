import spidev
import time

# Inicializar el objeto spidev
spi = spidev.SpiDev()
spi.open(0, 0)  # Bus 0, dispositivo 0
spi.max_speed_hz = 1000000  # 1 MHz

def recibir_datos_spi():
    # Recibir datos por SPI
    datos_recibidos = spi.readbytes(5)  # 5 bytes, ajustar según la cantidad de datos esperados
   
    return datos_recibidos

try:
    while True:
        # Esperar a recibir datos por SPI
        datos_recibidos = recibir_datos_spi()
        
        # Mostrar los datos recibidos
        print("Datos recibidos:", datos_recibidos)
        time.sleep(1)
        # Realizar cualquier procesamiento adicional aquí
        
except KeyboardInterrupt:
    spi.close()  # Cerrar el objeto SPI al finalizar
