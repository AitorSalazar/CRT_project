import spidev
import time

# Inicializar el objeto spidev
spi = spidev.SpiDev()
spi.open(0, 0)  # Bus 0, dispositivo 0
spi.max_speed_hz = 1000000  # 1 MHz

def enviar_datos_spi(datos):
    # Enviar datos por SPI
    spi.xfer2(datos)

try:
    while True:
        # Generar datos (aquí puedes modificar para tus necesidades)
        datos = [0x01, 0x02, 0x03, 0x04, 0x05]
        print(datos)
        # Enviar los datos por SPI
        enviar_datos_spi(datos)
        
        # Esperar un tiempo antes de enviar de nuevo
        time.sleep(1)

except KeyboardInterrupt:
    spi.close()  # Cerrar el objeto SPI al finalizar
