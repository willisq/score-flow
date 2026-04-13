import { defineStore } from "pinia";
import { ref } from "vue";
import type { Tournament } from "@/features/tournament/types";

export const useTournamentStore = defineStore("tournament", () => {
  const activeTournament = ref<Tournament | null>(null);
  const tournaments = ref<Tournament[]>([]);

  function setActiveTournament(tournament: Tournament): void {
    activeTournament.value = tournament;
  }

  function clearActiveTournament(): void {
    activeTournament.value = null;
  }

  function setTournaments(list: Tournament[]): void {
    tournaments.value = list;
  }

  return {
    activeTournament,
    tournaments,
    setActiveTournament,
    clearActiveTournament,
    setTournaments,
  };
});
