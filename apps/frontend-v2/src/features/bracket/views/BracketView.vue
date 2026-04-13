<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { useToast } from "primevue/usetoast";
import { useBracketData } from "../composables/useBracketData";
import { BracketService } from "../services/BracketService";
import { CategoryService } from "@/features/tournament/services/CategoryService";
import type { Category } from "@/features/tournament/types";
import type { Match } from "../types";
import TournamentBracket from "./components/TournamentBracket.vue";

const toast = useToast();
const { matches, loading, loadMatches } = useBracketData();

const categories = ref<Category[]>([]);
const selectedCategories = ref<string[]>([]);
const generating = ref(false);

const matchesByCategory = computed(() => {
  const grouped: Record<string, { category: Category | null; matches: Match[] }> = {};
  for (const match of matches.value) {
    const catId = match.categoryId ?? "uncategorized";
    if (!grouped[catId]) {
      grouped[catId] = {
        category: categories.value.find((c) => c.id === catId) ?? null,
        matches: [],
      };
    }
    grouped[catId].matches.push(match);
  }
  return Object.values(grouped);
});

async function generateBrackets(): Promise<void> {
  generating.value = true;
  try {
    const result = await BracketService.generate({
      categories: selectedCategories.value.length > 0 ? selectedCategories.value : null,
    });
    const total = result.results.reduce((sum, r) => sum + r.matchesGenerated, 0);
    toast.add({
      severity: "success",
      summary: "Pirámides Generadas",
      detail: `${total} enfrentamientos creados en ${result.results.length} categoría(s).`,
      life: 5000,
    });
    await loadMatches();
  } catch {
    toast.add({
      severity: "error",
      summary: "Error",
      detail: "No se pudieron generar las pirámides.",
      life: 5000,
    });
  } finally {
    generating.value = false;
  }
}

onMounted(async () => {
  categories.value = await CategoryService.getAll();
  await loadMatches();
});
</script>

<template>
  <div class="card">
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-2xl font-bold">Pirámides</h2>
      <div class="flex gap-2 items-center">
        <MultiSelect
          v-model="selectedCategories"
          :options="categories"
          optionLabel="modality.name"
          optionValue="id"
          placeholder="Filtrar categorías..."
          class="w-64"
        />
        <Button
          icon="pi pi-bolt"
          label="Generar Pirámides"
          :loading="generating"
          @click="generateBrackets"
        />
      </div>
    </div>

    <ProgressBar v-if="loading" mode="indeterminate" class="mb-4" style="height: 4px" />

    <div v-if="matchesByCategory.length === 0 && !loading" class="text-center text-surface-500 py-8">
      <i class="pi pi-sitemap text-4xl mb-4 block"></i>
      <p>No hay enfrentamientos generados. Seleccione categorías y genere las pirámides.</p>
    </div>

    <Accordion v-else :value="matchesByCategory[0]?.category?.id">
      <AccordionPanel
        v-for="group in matchesByCategory"
        :key="group.category?.id ?? 'uncategorized'"
        :value="group.category?.id ?? 'uncategorized'"
      >
        <AccordionHeader>
          <span v-if="group.category">
            {{ group.category.modality.name }} —
            {{ Math.min(...group.category.ages) }}–{{ Math.max(...group.category.ages) }} años
          </span>
          <span v-else>Sin categoría</span>
          <Tag :value="`${group.matches.length} enfrentamientos`" class="ml-2" />
        </AccordionHeader>
        <AccordionContent>
          <TournamentBracket :matches="group.matches" />
        </AccordionContent>
      </AccordionPanel>
    </Accordion>
  </div>
</template>
