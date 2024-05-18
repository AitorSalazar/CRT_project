#include <unistd.h>
#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <wiringPi.h>
#include <signal.h>
#include <string.h>
#include <sys/mman.h>
#include <fcntl.h>
#include "DHT.hpp"

// Numeracion de pines
#define BTN_PIN 12  // GPIO 18
#define LED0_PIN 38 // GPIO 20, blue
#define LED1_PIN 40 // GPIO 21, red
#define HYT_PIN 11 // GPIO 17

// Parametros de memoria
#define MEMORY_NAME "/shm_temp_humidity"
#define MEMORY_SIZE 2048

// Variables globales
int BTN_STATE = 0;  // 0 -> red, 1 -> blue

int CHECK_SHM;
void *mem_ptr;

using namespace std;

/**
 * @brief Button interruption handler
 * 
 * This function is called whenever the button is pressed. It reads the global
 * variable BTN_STATE and depending on its state it switches red and blue LEDs
 * on and off. It then changes the value of BTN_STATE to its opposite.
 * This function takes no arguments and returns void.
 */
void btn_handler(void) {

    if (BTN_STATE == 0) {
        digitalWrite(LED1_PIN, LOW);
        digitalWrite(LED0_PIN, HIGH);
    } else {
        digitalWrite(LED0_PIN, LOW);
        digitalWrite(LED1_PIN, HIGH);
    }
    BTN_STATE = !BTN_STATE;
}

/**
 * @brief ^C interruption handler
 * 
 * This function is called to terminate execution whenever a keyboard interrupt is
 * called.
 * 
 * @param signum Signal integer state
 * @return void
 */
void signal_callback_handler(int signum) {
    // Deslinkar y apagar pines
    pinMode(BTN_PIN, PM_OFF);
    digitalWrite(LED0_PIN, LOW);
    pinMode(LED0_PIN, PM_OFF);
    digitalWrite(LED1_PIN, LOW);
    pinMode(LED1_PIN, PM_OFF);
    pinMode(HYT_PIN, PM_OFF);

    // Desmapear y deslinkar memoria
    munmap(mem_ptr, MEMORY_SIZE);
    close(CHECK_SHM);
    shm_unlink(MEMORY_NAME);
    //cout << "\nPrograma finalizado\n" << endl;
    printf("\nPrograma finalizado.\n");
    // Terminate program
    exit(signum);
}

/**
 * @brief Initial set up function
 * 
 * This function is used to make the initial set up of the GPIOs and the 
 * creation of the shared memory object. If the shared memory is not opened 
 * correctly it exits the program with error code 1.
 * This function takes no arguments and returns void.
 */
void setup(void) {
    // Iniciar con numeracion fisica
    wiringPiSetupPhys();

    // Configurar pines
    pinMode(LED0_PIN, OUTPUT);
    pinMode(LED1_PIN, OUTPUT);
    pinMode(BTN_PIN, INPUT);
    pullUpDnControl(BTN_PIN, PUD_UP);
    wiringPiISR(BTN_PIN, INT_EDGE_FALLING, &btn_handler);

    // Inicializar memoria compartida
    CHECK_SHM = shm_open(MEMORY_NAME, O_CREAT | O_RDWR, 0666);
    if (CHECK_SHM == -1) {
        perror("shm_open");
        exit(1);
    }
    // Definir tamaño de memoria
    ftruncate(CHECK_SHM, MEMORY_SIZE);

    // Mapear memoria al espacio de direcciones de este proceso
    mem_ptr = mmap(NULL, MEMORY_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, CHECK_SHM, 0);
    if (mem_ptr == MAP_FAILED) {
        perror("mmap");
        exit(1);
    }
    printf("Memoria abierta sin problemas\n");
}

/**
 * @brief Main function
 * 
 * This is the main function of this source. It initializes the GPIOs and 
 * the shared memory by calling setup(). It reads the data from the sensor 
 * and writes it into the already initialized shared memory. Dependinf on 
 * the value of the global variable BTN_STATE it prints out temperature or 
 * humidity information.
 * 
 * @return int 
 */
int main(void) {
    // Parametros locales
    int read_dht;
    DHT dht_termo;
    int tempt_e = 0;
    int tempt_d = 0;
    int humdt = 0;
    int val_array[] = {0, 0, 0};
    //int *mem_intArray;
    

    // Setup
    setup();

    // Inicializar LEDs
    digitalWrite(LED1_PIN, HIGH);
    digitalWrite(LED0_PIN, LOW);
    
    // Bucle principal
    //mem_intArray = (int *)mem_ptr;
    while (1) {
        signal(SIGINT, signal_callback_handler);
        // 15 intentos de lectura (internos) 
        read_dht = dht_termo.readDHT11(HYT_PIN);
        if (read_dht != DHTLIB_OK) {
            continue;
        }

        // Escribir datos en memoria compartida
        val_array[0] = (int) dht_termo.humidity;
        val_array[1] = (int) dht_termo.temperature;
        val_array[2] = (int) (100 * (dht_termo.temperature) - val_array[1]*100);
        //printf("iteracion %d dir mem_intArray: %x val_array: %i\n" val_array[i] );
        memcpy(mem_ptr, val_array,sizeof(int)*3);

        if (BTN_STATE == 0) {
	    //cout << "Lectura de temperatura : %.1f C" << dht_termo.temperature << endl;
            printf("Lectura de temperatura: %.1fºC\n", dht_termo.temperature);
	        fflush(stdout);
        } else {
	    //cout << "Lectura de humedad: %.1f %%" << dht_termo.humidity << endl;
            printf("Lectura de humedad: %.1f %%\n", dht_termo.humidity);
	        fflush(stdout);
        }
        delay(500);
    }

    return 0;
}
