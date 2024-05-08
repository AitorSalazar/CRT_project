import RPi.GPIO as GPIO
import time
import MyLibraries.Freenove_DHT as DHT
import sys
from ctypes import *


PTHREAD_STACK_MIN = 131072

SCHED_FIFO = 1

TIMER_ABSTIME = 1
CLOCK_REALTIME = 0
CLOCK_MONOTONIC_RAW	= 4

NSEC_PER_SEC = 1000000000

interval = 500000000

# Definir pines que se van a usar
LED_PIN0 = 38    # GPIO 20, blue
LED_PIN1 = 40    # GPIO 21, red

BTN_PIN = 12     # GPIO 18

HYT_PIN = 11     # GPIO 17

# Flags globales
BTN_PRESSED = False
RED = True
STOP_THREADS = False


#lc = CDLL('libc.so.6', mode=RTLD_GLOBAL)
lc = CDLL('libc.so.6')
#lc = CDLL('libSystem.dylib')

class pthread_attr_t(Union):
    _fields_ = [('__size', c_char*64),
                ('__aling', c_int)]

class sched_param(Structure):    
    _fields_ = [('sched_priority', c_int)]

class timeval(Structure):
    _fields_ = [('t_sec', c_long),
                ('t_nsec', c_long)]

#attr = pthread_attr_t()
#param = sched_param()
#thread = c_void_p()
#t_read = timeval()

def tsnorm(ts):
    while(ts.t_nsec >= NSEC_PER_SEC):
        ts.t_nsec = ts.t_nsec-NSEC_PER_SEC
        ts.t_sec = ts.t_sec+1
    return ts


def setup():
    # Usar nombres fisicos
    GPIO.setmode(GPIO.BOARD)
    # Conectar con LEDs
    GPIO.setup(LED_PIN0, GPIO.OUT)
    GPIO.setup(LED_PIN1, GPIO.OUT)
    # Conectar boton
    GPIO.setup(BTN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def measure(arg=None):
    global BTN_PRESSED, RED, STOP_THREADS
    # Inicializar LEDs
    GPIO.output(LED_PIN1, GPIO.HIGH) # red high
    GPIO.output(LED_PIN0, GPIO.LOW) # blue low
    # Inicializar el higrotermometro
    dht_termo = DHT.DHT(HYT_PIN)

    # Bucle principal
    while not STOP_THREADS:
        try:
            # 15 intentos de lectura (internos)
            data_check = dht_termo.readDHT11()
            if data_check is not dht_termo.DHTLIB_OK:
                continue
            # ------------------------------
            if RED:
                print("Lectura de temperatura: ", dht_termo.temperature)
                BTN_PRESSED = False
            else:
                print("Lectura de humedad: ", dht_termo.humidity)
                BTN_PRESSED = False 
            time.sleep(1)
        except KeyboardInterrupt:
            break
    print('Termina el hilo measure')


def btn_event(arg=None):
    global BTN_PRESSED, RED, STOP_THREADS
    """
    Detect if button has been pressed. If so, it activates a flag.
    """
    while not STOP_THREADS:
        try:
            if (GPIO.input(BTN_PIN) == GPIO.LOW and not BTN_PRESSED):
                BTN_PRESSED = True
                if RED:
                    RED = False
                    GPIO.output(LED_PIN0, GPIO.HIGH) # blue high
                    GPIO.output(LED_PIN1, GPIO.LOW) # red low
                else:
                    RED = True
                    GPIO.output(LED_PIN0, GPIO.LOW) # blue low
                    GPIO.output(LED_PIN1, GPIO.HIGH) # red high
            else:
                pass
        except KeyboardInterrupt:
            break
    
    print('Termina el hilo btn_event')

def main():
    global STOP_THREADS
    #  Lock memory */
    #/*if(mlockall(MCL_CURRENT|MCL_FUTURE) == -1) {
    #        printf("mlockall failed: %m\n");
    #        exit(-2);
    #}*/
    # Initialize attributes and params
    attr_btn = pthread_attr_t()
    attr_dht = pthread_attr_t()
    param_btn = sched_param()
    param_dht = sched_param()
    thread_btn = c_void_p()
    thread_dht = c_void_p()

    #/* Initialize pthread attributes (default values) */
    ret_btn = lc.pthread_attr_init(byref(attr_btn))
    ret_dht = lc.pthread_attr_init(byref(attr_dht))
    if (ret_btn != 0 or ret_dht != 0):
        print("init pthread attributes failed\n")
        return ret_btn, ret_dht

    #/* Set a specific stack size  */
    ret_btn = lc.pthread_attr_setstacksize(byref(attr_btn), PTHREAD_STACK_MIN)
    ret_dht = lc.pthread_attr_setstacksize(byref(attr_dht), PTHREAD_STACK_MIN)
    if (ret_btn != 0 or ret_dht != 0):
        print("pthread setstacksize failed\n")
        return ret_btn, ret_dht

    #/* Set scheduler policy and priority of pthread */
    ret_btn = lc.pthread_attr_setschedpolicy(byref(attr_btn), SCHED_FIFO)
    ret_dht = lc.pthread_attr_setschedpolicy(byref(attr_dht), SCHED_FIFO)
    if (ret_btn != 0 or ret_dht != 0):
        print("pthread setschedpolicy failed\n")
        return ret_btn, ret_dht

    param_btn.sched_priority = 90
    param_dht.sched_priority = 80
    ret_btn = lc.pthread_attr_setschedparam(byref(attr_btn), byref(param_btn))
    ret_dht = lc.pthread_attr_setschedparam(byref(attr_dht), byref(param_dht))
    if (ret_btn != 0 or ret_dht != 0):
        print("pthread setschedparam failed\n")
        return ret_btn, ret_dht

    ret_btn = lc.pthread_attr_getschedparam(byref(attr_btn), byref(param_btn))
    ret_dht = lc.pthread_attr_getschedparam(byref(attr_dht), byref(param_dht))
    print("Param %d", param_btn.sched_priority)
    print("Param %d", param_dht.sched_priority)
    if (ret_btn != 0 or ret_dht != 0):
        print("pthread getschedparam failed\n")
        return ret_btn, ret_dht

    #/* Use scheduling parameters of attr */
    ret_btn = lc.pthread_attr_setinheritsched(byref(attr_btn), 1) #PTHREAD_EXPLICIT_SCHED);
    ret_dht = lc.pthread_attr_setinheritsched(byref(attr_btn), 1)
    if (ret_btn != 0 or ret_dht != 0):
        print("pthread setinheritsched failed\n")
        return ret_dht, ret_dht

    #/* Create a pthread with specified attributes */
    thread_btn_ptr = CFUNCTYPE(None, c_void_p)(btn_event)
    thread_dht_ptr = CFUNCTYPE(None, c_void_p)(measure)
    ret_btn = lc.pthread_create(byref(thread_btn), byref(attr_btn), thread_btn_ptr, None)
    ret_dht = lc.pthread_create(byref(thread_dht), byref(attr_dht), thread_dht_ptr, None)
    if (ret_btn != 0 or ret_dht != 0):
        print("create pthread failed\n")
        GPIO.cleanup()
        return ret_btn, ret_dht

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        STOP_THREADS = True
        #/* Join the thread and wait until it is done */
        ret_btn = lc.pthread_join(thread_btn, None)
        ret_dht = lc.pthread_join(thread_dht, None)
        if (ret_btn != 0 or ret_dht != 0):
            print("join pthread failed: %m\n")
        else:
            GPIO.cleanup()
            sys.exit("\nPrograma finalizado")

    return ret_btn, ret_dht


if __name__ == "__main__":
    setup()
    print(main())
    

