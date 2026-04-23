<script setup lang="ts">
import { computed } from "vue";
import type { Match } from "../../types";
import CompetitorCard from "./CompetitorCard.vue";

const props = defineProps<{
  matches: Match[];
}>();

// Compute the full bracket structure
const bracketRounds = computed(() => {
  if (!props.matches || props.matches.length === 0) return [];

  // Group matches by round id
  const matchesByRoundId: Record<string, Match[]> = {};
  for (const match of props.matches) {
    if (!matchesByRoundId[match.round.id]) {
      matchesByRoundId[match.round.id] = [];
    }
    matchesByRoundId[match.round.id].push(match);
  }

  // Sort groups by the number of matches descending to find the sequential rounds
  const sortedRoundGroups = Object.values(matchesByRoundId).sort((a, b) => b.length - a.length);

  // The first round determines the size of the pyramid
  const firstRoundSize = sortedRoundGroups[0].length;
  // Make sure it's a power of 2, if not find the next power of 2 (should be given the backend rules, but just in case)
  const baseSize = Math.pow(2, Math.ceil(Math.log2(firstRoundSize)));

  // Generate empty structure
  const allRounds: (Match | null)[][] = [];
  let currentSize = baseSize;
  while (currentSize >= 1) {
    allRounds.push(Array.from({ length: currentSize }, () => null));
    currentSize /= 2;
  }

  // Map existing matches into the structure
  for (const group of sortedRoundGroups) {
    // Determine which round index this group belongs to by its size
    // Example: If baseSize is 4, rounds are sizes 4, 2, 1.
    // If group.length is 4 => index 0. If 2 => index 1.
    // We use Math.log2 to find the exact index.
    const roundIndex = Math.log2(baseSize / group.length);
    // Integer round index ensures it maps exactly (assuming perfect halves).
    // If incomplete, we place them where they fit best.
    const targetIdx = Math.round(roundIndex);
    
    if (allRounds[targetIdx]) {
      for (const match of group) {
        if (match.position < allRounds[targetIdx].length) {
          allRounds[targetIdx][match.position] = match;
        }
      }
    }
  }

  return allRounds;
});

function isWinner(match: Match | null, position: "first" | "second"): boolean {
  if (!match || !match.winner) return false;
  const competitor = position === "first" ? match.firstCompetitor : match.secondCompetitor;
  return competitor?.id === match.winner.id;
}

function isBye(match: Match | null): boolean {
  if (!match) return false;
  return !match.secondCompetitor;
}
</script>

<template>
  <div class="tournament-brackets overflow-x-auto p-4 bg-surface-50 dark:bg-surface-900 rounded-lg">
    <div class="bracket inline-flex">
      <div
        v-for="(round, roundIndex) in bracketRounds"
        :key="roundIndex"
        class="round flex flex-col justify-around"
        :class="['round-' + (roundIndex + 1)]"
        style="min-width: 240px;"
      >
        <div
          v-for="(match, matchIndex) in round"
          :key="matchIndex"
          class="match flex flex-col justify-center relative mx-4 py-3 flex-grow"
        >
          <div v-if="match" class="match__content relative flex flex-col bg-surface-0 dark:bg-surface-800 border border-surface-200 dark:border-surface-700 rounded-md shadow-sm">
            <div class="text-[10px] uppercase font-bold text-surface-400 absolute -top-4 left-0 w-full text-center">
              {{ match.round.description }}
            </div>
            <CompetitorCard
              :name="match.firstCompetitor?.firstName + ' ' + match.firstCompetitor?.lastName"
              :academy="match.firstCompetitor?.academy?.name"
              :is-winner="isWinner(match, 'first')"
            />
            <CompetitorCard
              :name="match.secondCompetitor ? match.secondCompetitor?.firstName + ' ' + match.secondCompetitor?.lastName : undefined"
              :academy="match.secondCompetitor?.academy?.name"
              :is-winner="isWinner(match, 'second')"
              :is-bye="isBye(match)"
            />
          </div>
          <div v-else class="match__content relative flex flex-col bg-surface-100 dark:bg-surface-800 opacity-50 border border-dashed border-surface-300 dark:border-surface-700 rounded-md h-20">
             <!-- Placeholder para futuros enfrentamientos -->
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
*,
*::after,
*::before {
  box-sizing: border-box;
}

.bracket {
  display: flex;
  min-height: 400px;
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
  position: relative;
}

/* Línea de entrada que conecta desde la ronda anterior */
.match::before {
  content: "";
  display: block;
  min-height: 20px;
  border-left: 2px solid var(--surface-400);
  position: absolute;
  left: -16px;
  top: 50%;
  margin-top: -10px;
}

/* Ramificaciones de salida hacia la siguiente ronda (elemento superior) */
.match:nth-child(odd)::after {
  content: "";
  display: block;
  border: 2px solid transparent;
  border-top-color: var(--surface-400);
  border-right-color: var(--surface-400);
  height: 50%;
  position: absolute;
  right: -16px;
  width: 16px;
  top: 50%;
}

/* Ramificaciones de salida hacia la siguiente ronda (elemento inferior) */
.match:nth-child(even)::after {
  content: "";
  display: block;
  border: 2px solid transparent;
  border-bottom-color: var(--surface-400);
  border-right-color: var(--surface-400);
  height: 50%;
  position: absolute;
  right: -16px;
  width: 16px;
  bottom: 50%;
}

/* Conector que toca la caja del match */
.match__content::before {
  content: "";
  display: block;
  width: 16px;
  border-bottom: 2px solid var(--surface-400);
  position: absolute;
  top: 50%;
  left: -16px;
}
</style>
