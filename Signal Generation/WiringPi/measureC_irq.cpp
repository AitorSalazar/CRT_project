#include <stdio.h>
#include <stdint.h>
#include <wiringPi.h>
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
extern int BTN_STATE;

// Funciones externas
extern void btn_handler(void);


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
        // 15 intentos de lectura (internos) 
        read_dht = dht_termo.readDHT11(HYT_PIN);
        if (read_dht != DHTLIB_OK) {
            continue;
        }

        if (BTN_STATE == 0) {
            printf("Lectura de temperatura: %.1fºC", dht_termo.temperature);
        } else {
            printf("Lectura de humedad: %.1f %%", dht_termo.humidity);
        }
        delay(500);
    }

    return 0;
}
