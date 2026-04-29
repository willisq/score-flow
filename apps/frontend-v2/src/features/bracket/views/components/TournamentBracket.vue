<script setup lang="ts">
import { computed } from "vue";
import type { Match } from "../../types";
import CompetitorCard from "./CompetitorCard.vue";

const props = defineProps<{
  matches: Match[];
  id?: string;
  showEdit?: boolean;
}>();

const emit = defineEmits<{
  (e: "delete-competitor", payload: { registrationId: string; categoryModalityId: string }): void;
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
  // Make sure it's a power of 2
  let baseSize = Math.pow(2, Math.ceil(Math.log2(firstRoundSize)));

  // If less than 3 competitors, force at least 2 rounds (base size 2)
  let isForced = false;
  const competitorIds = new Set<string>();
  for (const m of props.matches) {
    if (m.firstCompetitor?.id) competitorIds.add(m.firstCompetitor.id);
    if (m.secondCompetitor?.id) competitorIds.add(m.secondCompetitor.id);
  }
  const competitorsCount = competitorIds.size;

  if (competitorsCount > 0 && competitorsCount < 3 && baseSize < 2) {
    baseSize = 2;
    isForced = true;
  }

  // Generate empty structure
  const allRounds: (Match | null)[][] = [];
  let currentSize = baseSize;
  while (currentSize >= 1) {
    allRounds.push(Array.from({ length: currentSize }, () => null));
    currentSize /= 2;
  }

  // Map existing matches into the structure
  // Only shift if we forced an extra round for aesthetic reasons
  let targetIdx = isForced ? 1 : 0;
  for (const group of sortedRoundGroups) {
    if (allRounds[targetIdx]) {
      for (const match of group) {
        if (match.position < allRounds[targetIdx].length) {
          allRounds[targetIdx][match.position] = match;
        }
      }
    }
    targetIdx++;
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
  // A match is a BYE if there is no second competitor AND the first competitor is already the winner
  return !match.secondCompetitor && match.winner?.id === match.firstCompetitor?.id;
}
</script>

<template>
  <div :id="id" class="tournament-brackets p-4 bg-surface-50 dark:bg-surface-900 rounded-lg relative">
    <img src="/img/logo.jpeg" class="absolute top-4 right-4 w-32 h-32 object-contain opacity-30 pointer-events-none" alt="Logo" />
    <div class="bracket inline-flex">
      <div v-for="(round, roundIndex) in bracketRounds" :key="roundIndex" class="round flex flex-col justify-around"
        :class="['round-' + (roundIndex + 1)]" style="min-width: 300px;">
        <div v-for="(match, matchIndex) in round" :key="matchIndex"
          class="match flex flex-col justify-center relative mx-4 py-3 flex-grow">
          <div v-if="match && !(bracketRounds.length > 1 && roundIndex === 0 && isBye(match))"
            class="match__content relative flex flex-col bg-surface-0 dark:bg-surface-800 border border-surface-200 dark:border-surface-700 rounded-md shadow-sm overflow-hidden">
            <div
              class="text-[9px] uppercase font-bold text-surface-400 bg-surface-50/50 dark:bg-surface-900/50 px-2 py-1 border-b border-surface-100 dark:border-surface-700 text-center">
              {{ match.round.description }}
            </div>
            <CompetitorCard
              :name="match.firstCompetitor ? `${match.firstCompetitor.firstName} ${match.firstCompetitor.lastName}` : '---'"
              :academy="match.firstCompetitor?.academy?.name" :is-winner="isWinner(match, 'first')"
              :show-delete="showEdit"
              @delete="match.firstCompetitor?.registrationId && $emit('delete-competitor', { registrationId: match.firstCompetitor.registrationId, categoryModalityId: match.categoryModalityId! })" />
            <CompetitorCard
              :name="match.secondCompetitor ? `${match.secondCompetitor.firstName} ${match.secondCompetitor.lastName}` : (isBye(match) ? 'BYE' : '---')"
              :academy="match.secondCompetitor?.academy?.name" :is-winner="isWinner(match, 'second')"
              :is-bye="isBye(match)"
              :show-delete="showEdit"
              @delete="match.secondCompetitor?.registrationId && $emit('delete-competitor', { registrationId: match.secondCompetitor.registrationId, categoryModalityId: match.categoryModalityId! })" />
          </div>
          <div v-else
            class="match__content relative flex flex-col bg-surface-100 dark:bg-surface-800 opacity-50 border border-dashed border-surface-300 dark:border-surface-700 rounded-md h-20">
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
