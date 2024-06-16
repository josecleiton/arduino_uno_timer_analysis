#ifndef _EXP1_H
#define _EXP1_H

#include <stdint.h>

volatile uint16_t current_counter = 0;
uint16_t counter_tmp = 0, result[N];
uint8_t run = 0;
boolean can_write = false, finished = false;

ISR(TIMER1_COMPA_vect) {
  noInterrupts();

  counter_tmp = current_counter;
  current_counter = 0;
  can_write = true;

  interrupts();
}

ISR(TIMER1_CAPT_vect) {
  current_counter++;
}

void setup() {
  for (int i = 0; i < N; i++) result[i] = 0;

  Serial.begin(115200);

  noInterrupts();

  TCCR1A = 0;
  TCNT1 = 0;

  // Configura Noise Canceler, Input Capture, Compare Match and prescaler as 1024
  TCCR1B = (1 << ICNC1) | (1 << ICES1) | (1 << WGM12) | (1 << CS12) | (1 << CS10);

  // Configura Input Capture Interrupt e Compare Match
  TIMSK1 = (1 << ICIE1) | (1 << OCIE1A);

  // Configura limiar para interrupção do Compare Match
  OCR1A = F_CPU / 1024L - 1;  // 16MHz/(1Hz*prescaler) - 1

  interrupts();
}

void loop() {
  if (finished) {
    return;
  }
  if (!can_write) {
    return;
  }

  can_write = false;
  result[run++] = counter_tmp;

  if (run >= N) {
    for (uint8_t i = 0; i < N; i++) Serial.println(result[i]);

    finished = true;
  }
}

#endif