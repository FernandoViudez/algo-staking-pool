tiempo total: 3600 seg
porcentaje total de stake: 100%
stake total: 100 unidades

tiempoEnPoolEnSegundos = 1000 seg
porcentajeDeStake = 20

tiempoEnPoolEnSegundos = 120 seg
porcentajeDeStake = 50

tiempoEnPoolEnSegundos = 10 seg
porcentajeDeStake = 30

unidadesQueTenes = tiempoEnPoolEnSegundos / (tiempoTotal / stakeTotal)

// por cada unidad va el %(procentajeDeStake) para esa persona
// es decir, si tenes 27 unidades, va el 50% de esas 27 unidades para vos

// unidadesQueTenes ----- 100%
// unidadesQueVanParaVos ----- porcentajeDeStake

reward = procentajeDeStake \* unidadesQueTenes / 100

// reward a: 13.88 unidades
// reward b: 1.6 unidades
// reward c: 0.08 unidades

// solo se pueden retirar unidades enteras.

cada Int(duracionDelPoolEnSegs / totRewards) segs, se mintea una unidad

if totRewards == 0
no hay rewards

de los n participantes del pool, se calcula el stake percent de cada uno.
si el 100% es la unidad que se acaba de mintear, cada participante recibe el porcentaje de stake que tiene en base
a la unidad minteada

por ej,
participante a: 20% del pool
1 TT-RWD --- 100% -> FIXED_RATE
0.2 TT-RWD --- 20%

0.2 será la cantidad de rewards que reciba el participante a
