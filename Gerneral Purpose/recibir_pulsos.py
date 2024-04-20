from gpiozero import Button
import time

# Define el número del pin GPIO que estás utilizando
pin = 11

# Crea un objeto Button para el pin especificado
button = Button(pin)

print("Esperando señal en el pin GPIO {}...".format(pin))

while True:
    if button.is_pressed:
        print("Se recibió una señal en el pin GPIO {}".format(pin))
        time.sleep(0.2)  # Espera 0.5 segundos para evitar impresiones múltiples por una sola señal
    time.sleep(0.1)  # Espera corta para evitar consumir demasiada CPU
