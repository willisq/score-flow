import { ref, onMounted, computed } from "vue";
import type { Category, Modality, Tournament } from "../types";
import { CategoryService } from "../services/CategoryService";
import { ModalityService } from "../services/ModalityService";
import { TournamentService } from "../services/TournamentService";

export function useTournamentData() {
  const categories = ref<Category[]>([]);
  const modalities = ref<Modality[]>([]);
  const tournaments = ref<Tournament[]>([]);
  const activeTournament = ref<Tournament | null>(null);
  const loading = ref(false);

  async function loadAll(): Promise<void> {
    loading.value = true;
    try {
      const [categoryData, modalityData, tournamentData] = await Promise.all([
        CategoryService.getAll(),
        ModalityService.getAll(),
        TournamentService.getAll(),
      ]);
      categories.value = categoryData;
      modalities.value = modalityData;
      tournaments.value = tournamentData;
      
      // Set the first tournament as active if none is set
      if (tournamentData.length > 0 && !activeTournament.value) {
        activeTournament.value = tournamentData[0];
      }
    } finally {
      loading.value = false;
    }
  }

  onMounted(loadAll);

  return { 
    categories, 
    modalities, 
    tournaments, 
    activeTournament, 
    loading, 
    reload: loadAll 
  };
}
