<template>
  <div class="tournament-brackets">
    <div class="bracket">
      <div
        v-for="(round, roundIndex) in bracketRounds"
        :key="roundIndex"
        class="round"
        :class="['round-' + (roundIndex + 1)]"
      >
        <div
          v-for="(match, matchIndex) in round"
          :key="matchIndex"
          class="match"
        >
          <div class="match__content" :style="matchStyle">
            <div class="competitor">
              <span class="name">{{
                match.first_competitor?.name || "---"
              }}</span>
              <span class="score">{{ match.first_competitor?.score }}</span>
            </div>
            <div class="competitor">
              <span class="name">{{
                match.second_competitor?.name || "---"
              }}</span>
              <span class="score">{{ match.second_competitor?.score }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  {{ bracketRounds.length }}
</template>

<script setup>
import { computed } from "vue";

const pairs = defineModel({
  type: Object,
  default: () => ({ round1: [], byes: [] }),
});

const props = defineProps({
  bracketSize: {
    type: Number,
    default: 8,
    validator: (value) => {
      // Valida que el tamaño sea una potencia de 2 (e.g., 2, 4, 8, 16, 32...)
      return value > 0 && (value & (value - 1)) === 0;
    },
  },
  matchStyle: {
    type: Object,
    default: () => ({
      border: "1px solid #ccc",
      width: "180px",
      height: "60px",
    }),
  },
});

const roundsSize = computed(
  () =>
    2 **
    Math.ceil(
      Math.log2(pairs.value.round1.length + pairs.value.byes.length * 2)
    )
);

/**
 * Genera la estructura completa de la pirámide, incluyendo rondas vacías.
 */
const bracketRounds = computed(() => {
  if (roundsSize.value < 2) {
    return [];
  }

  // 1. Crear la estructura completa de la pirámide con partidas vacías
  const allRounds = [];
  let numberOfMatchesInRound = roundsSize.value;
  while (numberOfMatchesInRound >= 1) {
    const round = Array.from({ length: numberOfMatchesInRound }, () => ({
      first_competitor: null,
      second_competitor: null,
    }));
    allRounds.push(round);
    numberOfMatchesInRound /= 2;
  }

  // 2. Obtener los datos de las partidas y los byes desde el v-model
  const round1Matches = pairs.value?.round1 || [];
  const byeCompetitors = [...(pairs.value?.byes || [])]; // Copia para poder mutarla

  // 3. Poblar la primera ronda con las partidas definidas en `round1`
  for (let i = 0; i < round1Matches.length; i++) {
    if (allRounds[0] && allRounds[0][i]) {
      allRounds[0][i] = { ...round1Matches[i] };
    }
  }

  const nullIndexOnFirstRound = Math.floor(
    allRounds[0].findIndex((match) => match.first_competitor === null) / 2
  );

  byeCompetitors.forEach((competitor, index) => {
    if (allRounds[1] && allRounds[1][index]) {
      allRounds[1][nullIndexOnFirstRound + index] = competitor;
    }
  });

  // 4. Poblar la segunda ronda con los competidores "bye"
  // Un "bye" ocupa una plaza vacía en la primera ronda y avanza a la segunda.
  // if (allRounds.length >= 2) {
  //   const round2 = allRounds[1];
  //   for (let i = 0; i < round2.length; i++) {
  //     const matchInRound2 = round2[i];
  //     const firstFeederMatchIndex = i * 2;
  //     const secondFeederMatchIndex = i * 2 + 1;

  //     // console.log(matchInRound2, firstFeederMatchIndex, secondFeederMatchIndex);
  //     //
  //     // Revisa la primera partida que alimenta esta casilla de R2
  //     const firstFeederMatch = allRounds[0][firstFeederMatchIndex];
  //     if (!firstFeederMatch.first_competitor && byeCompetitors.length > 0) {
  //       matchInRound2.first_competitor = byeCompetitors.shift();
  //     }

  //     // Revisa la segunda partida que alimenta esta casilla de R2
  //     const secondFeederMatch = allRounds[0][secondFeederMatchIndex];
  //     if (!secondFeederMatch.first_competitor && byeCompetitors.length > 0) {
  //       matchInRound2.second_competitor = byeCompetitors.shift();
  //     }
  //   }
  // }

  // 5. Poblar el resto de la pirámide (futuras implementaciones podrían calcular ganadores aquí)
  // Por ahora, las rondas futuras permanecerán vacías como se solicitó.

  return allRounds;
});
</script>

<style>
*,
*::after,
*::before {
  box-sizing: border-box;
}

.bracket {
  display: flex;
  min-height: 400px; /* Altura mínima para visualizar pirámides pequeñas */
}

.round {
  display: flex;
  flex-grow: 1;
  flex-direction: column;
}

.round:first-child .match::before {
  display: none;
}

.round:first-child .match__content::before {
  display: none;
}

.round:last-child .match::after {
  display: none;
}

.match {
  display: flex;
  flex-direction: column;
  justify-content: center;
  margin: 0 10px;
  padding: 10px 0;
  flex-grow: 1;
  position: relative;
}

.match::before {
  content: "";
  display: block;
  min-height: 40px; /* Ajustado a la altura del padding del match */
  border-left: 2px solid #888;
  position: absolute;
  left: -10px;
  top: 50%;
  margin-top: -20px; /* Mitad de min-height */
  margin-left: -2px;
}

.match:nth-child(odd)::after {
  content: "";
  display: block;
  border: 2px solid transparent;
  border-top-color: #888;
  border-right-color: #888;
  height: 50%;
  position: absolute;
  right: -10px;
  width: 73px;
  top: 50%;
}

.match:nth-child(even)::after {
  content: "";
  display: block;
  border: 2px solid transparent;
  border-bottom-color: #888;
  border-right-color: #888;
  height: 50%;
  position: absolute;
  right: -10px;
  width: 73px;
  bottom: 50%;
}

.match__content {
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  padding: 5px 10px;
  background-color: #f9f9f9;
  font-family: sans-serif;
  font-size: 0.85rem;
}

.match__content::before {
  content: "";
  display: block;
  width: 10px;
  border-bottom: 2px solid #888;
  margin-left: -2px;
  position: absolute;
  top: 50%;
  left: -10px;
}

.competitor {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.score {
  font-weight: bold;
}
</style>
