#include <unistd.h>
#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <wiringPi.h>
#include <signal.h>
#include "DHT.hpp"

// Numeracion de pines
#define BTN_PIN 12  // GPIO 18
#define LED0_PIN 38 // GPIO 20, blue
#define LED1_PIN 40 // GPIO 21, red
#define HYT_PIN 11 // GPIO 17

// Parametros de memoria
#define MEMORY_NAME "/shm_temp_humidity"
#define MEMORY_SIZE 2048

// Variables externas
//extern int BTN_STATE;

// Funciones externas
//extern void btn_handler(void);

int BTN_STATE = 0;  // 0 -> red, 1 -> blue

using namespace std;

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


void signal_callback_handler(int signum) {
    pinMode(BTN_PIN, PM_OFF);  // PM_OFF no funciona
    digitalWrite(LED0_PIN, LOW);
    pinMode(LED0_PIN, PM_OFF);
    digitalWrite(LED1_PIN, LOW);
    pinMode(LED1_PIN, PM_OFF);
    pinMode(HYT_PIN, PM_OFF);
    //cout << "\nPrograma finalizado\n" << endl;
    printf("\nPrograma finalizado.\n");
    // Terminate program
    exit(signum);
}


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
    //...
}


int main(void) {
    // Parametros locales
    int buf_pos = 0;
    int read_dht;
    DHT dht_termo;

    // Setup
    setup();

    // Inicializar LEDs
    digitalWrite(LED1_PIN, HIGH);
    digitalWrite(LED0_PIN, LOW);
    
    // Bucle principal

    while (1) {
        signal(SIGINT, signal_callback_handler);
        // 15 intentos de lectura (internos) 
        read_dht = dht_termo.readDHT11(HYT_PIN);
        if (read_dht != DHTLIB_OK) {
            continue;
        }

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
