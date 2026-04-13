import { ref, onMounted } from "vue";
import type { Category, Modality } from "../types";
import { CategoryService } from "../services/CategoryService";
import { ModalityService } from "../services/ModalityService";

export function useTournamentData() {
  const categories = ref<Category[]>([]);
  const modalities = ref<Modality[]>([]);
  const loading = ref(false);

  async function loadAll(): Promise<void> {
    loading.value = true;
    try {
      const [categoryData, modalityData] = await Promise.all([
        CategoryService.getAll(),
        ModalityService.getAll(),
      ]);
      categories.value = categoryData;
      modalities.value = modalityData;
    } finally {
      loading.value = false;
    }
  }

  onMounted(loadAll);

  return { categories, modalities, loading, reload: loadAll };
}
