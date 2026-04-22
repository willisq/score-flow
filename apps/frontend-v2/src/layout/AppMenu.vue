<script setup lang="ts">
import { onMounted, ref } from "vue";
import AppMenuItem from "./AppMenuItem.vue";
import { useTournamentStore } from "@/core/stores/useTournamentStore";
import { TournamentService } from "@/features/tournament/services/TournamentService";
import type { Tournament } from "@/features/tournament/types";

const tournamentStore = useTournamentStore();
const loadingTournaments = ref(false);

const menuItems = ref([
  {
    label: "General",
    items: [{ label: "Dashboard", icon: "pi pi-fw pi-home", to: "/" }],
  },
  {
    label: "Gestión",
    items: [
      { label: "Competidores", icon: "pi pi-fw pi-id-card", to: "/competitors" },
      { label: "Academias", icon: "pi pi-fw pi-building", to: "/academies" },
      { label: "Torneos", icon: "pi pi-fw pi-trophy", to: "/tournaments" },
    ],
  },
  {
    label: "Competencia",
    items: [
      { label: "Grupos de Rangos", icon: "pi pi-fw pi-tags", to: "/rank-groups" },
      { label: "Categorías", icon: "pi pi-fw pi-users", to: "/categories" },
      { label: "Generador de Categorías", icon: "pi pi-fw pi-sliders-h", to: "/category-builder" },
      { label: "Inscripciones Masivas", icon: "pi pi-fw pi-user-plus", to: "/enrollment" },
      { label: "Pirámides", icon: "pi pi-fw pi-sitemap", to: "/brackets" },
    ],
  },
]);

function onTournamentChange(tournament: Tournament): void {
  tournamentStore.setActiveTournament(tournament);
}

onMounted(async () => {
  loadingTournaments.value = true;
  try {
    const tournaments = await TournamentService.getAll();
    tournamentStore.setTournaments(tournaments);

    if (tournaments.length > 0 && !tournamentStore.activeTournament) {
      tournamentStore.setActiveTournament(tournaments[0]);
    }
  } finally {
    loadingTournaments.value = false;
  }
});
</script>

<template>
  <div class="layout-menu-container">
    <!-- Tournament Selector -->
    <div class="p-3 border-b border-surface-200 dark:border-surface-700">
      <label class="block text-sm font-semibold mb-2 text-surface-600 dark:text-surface-300">
        <i class="pi pi-trophy mr-1"></i> Competencia Activa
      </label>
      <Select v-model="tournamentStore.activeTournament" :options="tournamentStore.tournaments"
        optionLabel="description" placeholder="Seleccionar torneo..." class="w-full" :loading="loadingTournaments"
        @change="onTournamentChange($event.value)" />
    </div>

    <!-- Navigation Menu -->
    <ul class="layout-menu">
      <template v-for="(item, i) in menuItems" :key="i">
        <AppMenuItem :item="item" :index="i" />
      </template>
    </ul>
  </div>
</template>

<style lang="scss" scoped></style>
