from multiprocessing import shared_memory
import struct
import random


MEMORY_NAME = "shm_temp_humidity"
MEMORY_SIZE = 32
"""
La memoria más pequeña que se puede generar es de 16kB (16.384, 2^14).
Si se le pones que la memoria tenga 32 bytes, te genera una de 16kB y 
se reserva solo los primeros 32 bytes.
"""


def do_child_work():
    """
    This process accesses an existing shared memory and writes data on it.
    :returns: 0 if data is written successfully, 1 otherwise.
    """
    # Acceder a la memoria
    shm_a = shared_memory.SharedMemory(name=MEMORY_NAME, create=False, size=MEMORY_SIZE)
    # Escribir bytes
    rand_byte_int = random.getrandbits(4)
    #data_array = bytearray([rand_byte_int for i in range(MEMORY_SIZE)])
    data_list = [21, 3, 50]
    j = 0
    for i in range(len(data_list)):
        if 0 <= data_list[i] < 8:
            shm_a.buf[i + j] = data_list[i]
            j += 1
            continue
        shm_a.buf[i + j] = data_list[i]
        read_mem = bytes(shm_a.buf)
    #shm_a.buf[:MEMORY_SIZE] = data_array
    # Write single byte
    #shm_a.buf[0] = 255
    print("Datos escritos")


def main():
    """
    Main function of module
    :return: None
    """
    # Inicializar memoria compartida
    shm = shared_memory.SharedMemory(name=MEMORY_NAME, create=True, size=MEMORY_SIZE)
    try:
        # Llamar a la funcion para escrbir bytes
        do_child_work()
        # Leer bytres
        read_bytes = bytes(shm.buf)
        print(f"Byte leído: {read_bytes[0]}")
        shm.unlink()
    except KeyboardInterrupt:
        shm.unlink()


if __name__ == "__main__":
    main()

