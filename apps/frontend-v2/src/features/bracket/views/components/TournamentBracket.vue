<script setup lang="ts">
import type { Match } from "../../types";

defineProps<{
  matches: Match[];
}>();

function getCompetitorName(match: Match, position: "first" | "second"): string {
  const competitor = position === "first" ? match.firstCompetitor : match.secondCompetitor;
  if (!competitor) return "BYE";
  return `${competitor.firstName} ${competitor.lastName}`;
}

function getCompetitorAcademy(match: Match, position: "first" | "second"): string {
  const competitor = position === "first" ? match.firstCompetitor : match.secondCompetitor;
  return competitor?.academy?.name ?? "";
}

function isWinner(match: Match, position: "first" | "second"): boolean {
  if (!match.winner) return false;
  const competitor = position === "first" ? match.firstCompetitor : match.secondCompetitor;
  return competitor?.id === match.winner.id;
}

function isBye(match: Match): boolean {
  return !match.secondCompetitor;
}
</script>

<template>
  <div class="bracket-container overflow-x-auto">
    <div class="flex flex-col gap-3">
      <div
        v-for="match in matches"
        :key="match.id"
        class="bracket-match border border-surface-200 dark:border-surface-700 rounded-lg overflow-hidden"
        style="min-width: 320px"
      >
        <div class="flex items-center justify-between text-xs text-surface-400 px-3 py-1 bg-surface-50 dark:bg-surface-800">
          <span>{{ match.round.description }}</span>
          <span>Posición {{ match.position }}</span>
        </div>

        <!-- First competitor -->
        <div
          class="flex items-center justify-between px-3 py-2 border-b border-surface-100 dark:border-surface-700"
          :class="{ 'bg-green-50 dark:bg-green-900/20': isWinner(match, 'first') }"
        >
          <div class="flex flex-col">
            <span class="font-semibold text-sm">{{ getCompetitorName(match, "first") }}</span>
            <span class="text-xs text-surface-400">{{ getCompetitorAcademy(match, "first") }}</span>
          </div>
          <i v-if="isWinner(match, 'first')" class="pi pi-trophy text-green-500"></i>
        </div>

        <!-- Second competitor -->
        <div
          class="flex items-center justify-between px-3 py-2"
          :class="{
            'bg-green-50 dark:bg-green-900/20': isWinner(match, 'second'),
            'bg-surface-100 dark:bg-surface-800 opacity-60': isBye(match),
          }"
        >
          <div class="flex flex-col">
            <span class="font-semibold text-sm">{{ getCompetitorName(match, "second") }}</span>
            <span class="text-xs text-surface-400">{{ getCompetitorAcademy(match, "second") }}</span>
          </div>
          <i v-if="isWinner(match, 'second')" class="pi pi-trophy text-green-500"></i>
          <Tag v-if="isBye(match)" value="BYE" severity="secondary" class="text-xs" />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.bracket-match {
  transition: box-shadow 0.2s;
}
.bracket-match:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
</style>
