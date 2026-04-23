import { ref } from "vue";
import type { Match } from "../types";
import { BracketService } from "../services/BracketService";

export function useBracketData() {
  const matches = ref<Match[]>([]);
  const loading = ref(false);

  async function loadMatches(filters: any = {}): Promise<void> {
    loading.value = true;
    try {
      matches.value = await BracketService.getAll(filters);
    } finally {
      loading.value = false;
    }
  }

  return { matches, loading, loadMatches };
}
