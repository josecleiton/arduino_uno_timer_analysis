# Experimentos para analisar a exatidão e precisão do relógio interno do Arduíno

Utilizando o DS3231 como relógio de referência, devido a sua precisão de 2 partes por milhão (ppm) e compensação acerca da variação de temperatura, dois experimentos foram realizados para medir a precisão e exatidão da temporização do Arduíno Uno R3 em relação ao DS3231.

Ambos os experimentos utilizam características do TIMER1, um dos 3 relógios do microcontrolador Atmega328p acoplado ao Arduíno Uno R3.

## Experimento 1 (exp1.h)

Nele podem ser realizadas `N` contagens de pulsos transmitidos pelo relógio DS3231 em 1 segundo. A saída 32KHz do DS3231 deve ser conectada na porta 8 do Arduíno, porque os pulsos são capturados através do Input Capture Unit (ICU) do TIMER1. Também, é configurada a interrupção por comparação (Compare Match) com pre-scaler de 1024, fazendo com que ela ocorra a cada 1s, momento em que a contagem encerra.

Caso a média das contagens seja abaixo de 32K, a temporização do Arduíno está adiantada em relação à referência.

## Experimento 2 (exp2.h)

Nele podem ser realizados `N` medições de intervalos de pulsos gerados pelo relógio DS3231 acoplado ao(s) contador(es) binário(s) que permitam o 32KHz ser dividido até 1Hz. Sendo assim, o pulso de 1Hz deve também ser conectado na porta 8 do Arduíno para o ICU. Além disso, o TIMER1 é configurado para overflow com pre-scaler de 8, fazendo com que cada overflow ocorra a 0,5us. Após a captura de dois pulsos, é calculada diferença entre o instante 0 e 1 que deve ser próxima dos
10^6us.

Caso a média dos intervalos seja acima de 10^6, a temporização do Arduíno está adiantada em relação a referência.

## Conclusões

O uso de microcontroladores nos experimentos didáticos, como os acoplados nas placas Arduino, auxiliam na demonstração de fenômenos e podem ser apetrechos notáveis no ensino dos conceitos da Física. No entanto, as inexatidões e imprecisões desses dispositivos precisam ser consideradas na análise dos resultados.

O presente trabalho avaliou o impacto potencial da imprecisão e inexatidão do relógio interno do Arduino sobre experimentos didáticos de Física com base em um dispositivo de referência. O procedimento metodológico para essa avaliação seguiram as etapas de concepção e construção de dois experimentos complementares, codificação da rotina experimental e análise dos resultados. A etapa de codificação foi aperfeiçoada para garantir uma maior estabilidade dos dados capturados, gerando duas baterias experimentais.

A análise dos dados expôs que as placas Arduino Uno R3 apresentam variações significativas de inexatidão mesmo num mesmo. Enquanto a maioria das placas apresentou relógios mais lentos que o DS3231, a placa 5 teve um relógio mais rápido. Na média, o tempo em relação à referência foi de $1,000658 \pm 0,000337$ segundos, desconsiderando as placas *outliers* 5 e 11. Essa inexatidão teve um impacto reduzido em experimentos como a medição da velocidade do som em barras de aço, mas foi significativa em experimentos de queda livre , ou seja, o impacto da inexatidão da temporização do Arduino varia conforme os requisitos temporais de cada experimento.

Em relação à precisão, as placas demonstraram alta precisão, apesar da falta de homogeneidade nas variâncias, conforme indicado pelo teste de Levene. Essa alta precisão pode ser útil para que os professores e/ou alunos apliquem ajustes matemáticos, especialmente para placas menos exatas, como a placa 11.

Algumas limitações foram identificadas, como: o número restrito de placas, limitando a análise a dois lotes do modelo Uno R3; a falta de controle rigoroso da temperatura durante os experimentos, realizados em laboratório regulado por um ar-condicionado convencional; a realização dos experimentos em ambiente que pode não refletir condições reais de salas de aulas. Além disso, a distribuição dos dados não seguiu uma curva gaussiana, sugerindo a necessidade de mais placas na etapa experimental.

Sendo assim, concluiu-se que o objetivo deste trabalho foi alcançado, na medida que o impacto potencial da inexatidão e imprecisão do relógio interno do Arduino sobre experimentos didáticos de Física foi analisado, fornecendo informações sobre como é realizada a temporização nas placas Arduino e identificando experimentos didáticos típicos de Física.

Este trabalho atingiu seus objetivos, mas há espaço para aprofundamento em trabalhos futuros, com análises comparativas com outras placas de prototipação, por exemplo, Raspberry Pi Pico; análise do impacto de variações de temperatura e umidade; criação de procedimentos para ajustar matematicamente os resultados experimentais com base na inexatidão da frequência do oscilador da placa Arduino.
