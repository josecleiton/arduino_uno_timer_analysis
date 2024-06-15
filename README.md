# Experimentos para analisar a exatidão e precisão do relógio interno do Arduíno

Utilizando o DS3231 como relógio de referência, devido a sua precisão de 2 partes por milhão (ppm) e compensação acerca da variação de temperatura, dois experimentos foram realizados para medir a precisão e exatidão da temporização do Arduíno Uno R3 em relação ao DS3231.

Ambos os experimentos utilizam características do TIMER1, um dos 3 relógios disponibilizados pelo microcontrolador Atmega328p acoplado ao Arduíno Uno R3.

## Experimento 1 (exp1.h)

Nele podem ser realizados `N` contagens de pulsos transmitidos pelo relógio DS3231 em 1 segundo. A saída 32KHz do DS3231 deve ser conectado na porta 8 do Arduíno, porque os pulsos são capturados através do (Input Capture Unit) ICU do TIMER1. Além do ICU é feita a configuração da interrupção por comparação (Compare Match) com pre-scaler de 1024, fazendo com que ela ocorra a cada 1s, momento em que a contagem encerra.

Caso a média das contagens seja abaixo de 32K, a temporização do Arduíno está adiantada em relação a referência.

## Experimento 2 (exp2.h)

Nele podem ser realizados `N` medições de intervalos de pulsos gerados pelo relógio DS3231 acoplado ao(s) contador(es) binário(s) que permitam o 32KHz ser dividido até 1Hz. Sendo assim, o pulso de 1Hz deve também ser conectado na porta 8 do Arduíno para o ICU. Além disso, o TIMER1 é configurado para overflow com pre-scaler de 8, fazendo com que cada overflow ocorra a 0,5us. Após a captura de dois pulsos, é calculada diferença entre o instante 0 e 1 que deve ser próxima dos
10^6us.

Caso a média dos intervalos seja acima de 10^6, a temporização do Arduíno está adiantada em relação a referência.

## Resultados

TBD
