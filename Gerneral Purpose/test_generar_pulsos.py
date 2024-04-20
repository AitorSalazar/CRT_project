from gpiozero import LED
import time

# Define el número del pin GPIO que estás utilizando
pin = 2 #gpio2 pin 3

# Crea un objeto LED para el pin especificado
led = LED(pin)

print("Generando pulsos cada 0.5 segundos en el pin GPIO {}...".format(pin))

try:
    while True:
        led.on()  # Enciende el LED
        time.sleep(0.1)  # Mantiene el LED encendido durante 0.1 segundos
        print("led on")
        led.off()  # Apaga el LED
        time.sleep(0.4)  # Espera 0.4 segundos hasta el próximo pulso
        print("led off")

except KeyboardInterrupt:
    led.off()  # Apaga el LED al presionar Ctrl+C para terminar el script
    print("\nScript detenido por el usuario.")
