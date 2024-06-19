#ifndef _EXP2_H
#define _EXP2_H

#include <stdint.h>

const uint32_t TIMER_SIZE = 1L << 16;

volatile uint8_t count_overflow = 0;
volatile int8_t interval_idx = -1;

uint32_t interval[2], result[N];
uint8_t last_overflows_irc1 = 0;
uint8_t run = 0;
uint16_t last_icr1 = 0;
int8_t interval_idx_tmp = 0;
boolean finished = false;

ISR(TIMER1_OVF_vect) {
  count_overflow++;  // overflows a cada 0.5us
}

ISR(TIMER1_CAPT_vect) {
  noInterrupts();

  last_icr1 = ICR1;  // captura o pulso de 1Hz na porta 8
  last_overflows_irc1 = count_overflow;

  interval_idx++;

  interrupts();
}

void setup() {
  for (int i = 0; i < N; i++)
    result[i] = 0;
  interval[0] = interval[1] = 0;

  Serial.begin(9600);

  noInterrupts();

  TCCR1A = 0;
  TCCR1B = 0;
  TCNT1 = 0;

  // Setup Noise Canceler, Input Capture and prescaler 8 (0.5us resolution)
  TCCR1B = (1 << ICNC1) | (1 << ICES1) | (1 << CS11);

  // Setup Timer Input Capture Interrupt and Overflow
  TIMSK1 = (1 << ICIE1) | (1 << TOIE1);

  interrupts();
}

void loop() {
  if (finished) {
    return;
  }

  interval_idx_tmp = interval_idx;

  if (interval_idx_tmp < 0) {
    return;
  }

  if (interval[interval_idx_tmp]) {  // garante não sobrescrever se já foi
                                     // preenchido
    return;
  }
  // (overflow * 2^16 + t) / 2
  // divide por 2 para ter o resultado em micros
  interval[interval_idx_tmp] =
    (TIMER_SIZE * last_overflows_irc1 + last_icr1) >> 1;

  if (interval_idx_tmp == 1) {
    result[run++] = interval[1] - interval[0];

    // reseta os intervalos e o overflow
    noInterrupts();

    interval[0] = interval[1] = 0;
    interval_idx = -1;
    count_overflow = 0;

    interrupts();
  }

  if (run >= N) {
    for (int i = 0; i < N; i++)
      Serial.println(result[i]);

    finished = true;
  }
}

#endif
