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
          <div class="match__content flex flex-col gap-2" :style="matchStyle">
            <CompetitorCard
              :name="match?.first_competitor?.name"
              :academy="match?.first_competitor?.academy_name"
            />
            <CompetitorCard
              :name="match?.second_competitor?.name"
              :academy="match?.second_competitor?.academy_name"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
import CompetitorCard from "./CompetitorCard.vue";

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
      height: "80px",
    }),
  },
});

const roundsSize = computed(() => {
  const nummberOfPairs = Object.values(pairs.value).reduce((acc, round) => {
    return acc + round.length;
  }, 0);

  return 2 ** Math.ceil(Math.log2(nummberOfPairs));
});

/**
 * Genera la estructura completa de la pirámide, incluyendo rondas vacías.
 */
const bracketRounds = computed(() => {
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
  const round1Matches = pairs.value?.round1 || pairs.value?.Final || [];
  const byeCompetitors = Reflect.get(pairs.value, "byes") || [];

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
  min-height: 400px;
  /* Altura mínima para visualizar pirámides pequeñas */
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
  min-height: 40px;
  /* Ajustado a la altura del padding del match */
  border-left: 2px solid #888;
  position: absolute;
  left: -10px;
  top: 50%;
  margin-top: -20px;
  /* Mitad de min-height */
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
</style>
