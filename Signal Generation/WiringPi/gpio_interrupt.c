#include <stdio.h>
#include <wiringPi.h>


#define BTN_PIN 12  // GPIO 18
#define LED0_PIN 38 // GPIO 20, blue
#define LED1_PIN 40 // GPIO 21, red


int BTN_STATE = 0;  // 0 -> red, 1 -> blue


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

