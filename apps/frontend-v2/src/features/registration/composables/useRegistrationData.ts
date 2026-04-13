import { ref, onMounted } from "vue";
import type { Academy, Rank, Sex } from "../types";
import { AcademyService } from "../services/AcademyService";
import { RankService } from "../services/RankService";
import { SexService } from "../services/SexService";

export function useRegistrationData() {
  const academies = ref<Academy[]>([]);
  const ranks = ref<Rank[]>([]);
  const sexes = ref<Sex[]>([]);
  const loading = ref(false);

  async function loadAll(): Promise<void> {
    loading.value = true;
    try {
      const [academyData, rankData, sexData] = await Promise.all([
        AcademyService.getAll(),
        RankService.getAll(),
        SexService.getAll(),
      ]);
      academies.value = academyData;
      ranks.value = rankData;
      sexes.value = sexData;
    } finally {
      loading.value = false;
    }
  }

  onMounted(loadAll);

  return { academies, ranks, sexes, loading, reload: loadAll };
}
