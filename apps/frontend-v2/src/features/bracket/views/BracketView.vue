<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { useToast } from "primevue/usetoast";
import { useBracketData } from "../composables/useBracketData";
import { BracketService } from "../services/BracketService";
import { CategoryService } from "@/features/tournament/services/CategoryService";
import { ModalityService } from "@/features/tournament/services/ModalityService";
import { RankService } from "@/features/registration/services/RankService";
import type { Category, Modality } from "@/features/tournament/types";
import type { Rank } from "@/features/registration/types";
import type { Match } from "../types";
import TournamentBracket from "./components/TournamentBracket.vue";

const toast = useToast();
const { matches, loading, loadMatches } = useBracketData();

const categories = ref<Category[]>([]);
const selectedCategories = ref<string[]>([]);
const generating = ref(false);

const categoryModalitiesDisplay = computed(() => {
  const list: any[] = [];
  for (const cat of categories.value) {
    for (const cm of cat.modalities) {
      const minAge = Math.min(...cat.ages);
      const maxAge = Math.max(...cat.ages);
      const sexesStr = cm.sexes.map(s => s.name).join('/');

      const pr = cm.physicalRequirement;
      const hasWeight = pr && (pr.initialWeight !== null || pr.finalWeight !== null);
      const weightStr = hasWeight ? `${pr.initialWeight ?? '0'}kg - ${pr.finalWeight ?? '∞'}kg` : null;

      const ranksStr = cm.rankGroup ? cm.rankGroup.name : 'Todos los rangos';

      list.push({
        id: cm.id,
        displayName: `${cm.modality.name} - ${sexesStr} | ${minAge}-${maxAge} años${weightStr ? ' | ' + weightStr : ''} | ${ranksStr}`,
        category: cat,
        modality: cm,
        // Individual properties for rich UI layout
        sexesStr,
        ageStr: `${minAge}-${maxAge} años`,
        ranksStr,
        weightStr,
        isSpecial: cat.specialCondition
      });
    }
  }
  return list;
});

const ranks = ref<Rank[]>([]);
const modalities = ref<Modality[]>([]);

const listFilters = ref({
  rank_id: null as string | null,
  modality_id: null as string | null,
  age: null as number | null,
  weight: null as number | null,
  special_condition: false
});

const matchesByCategory = computed(() => {
  const grouped: Record<string, { display: any | null; matches: Match[]; realMatchesCount: number }> = {};
  for (const match of matches.value) {
    const cmId = match.categoryModalityId ?? "uncategorized";
    if (!grouped[cmId]) {
      grouped[cmId] = {
        display: categoryModalitiesDisplay.value.find((c) => c.id === cmId) ?? null,
        matches: [],
        realMatchesCount: 0
      };
    }
    grouped[cmId].matches.push(match);

    // Is it a BYE? (No second competitor and first is winner)
    const isBye = !match.secondCompetitor && match.winner?.id === match.firstCompetitor?.id;
    if (!isBye) {
      grouped[cmId].realMatchesCount++;
    }
  }
  return Object.values(grouped);
});

async function applyFilters() {
  const queryFilters: any = {};
  if (listFilters.value.rank_id) queryFilters.rank_id = listFilters.value.rank_id;
  if (listFilters.value.modality_id) queryFilters.modality_id = listFilters.value.modality_id;
  if (listFilters.value.age !== null) queryFilters.age = listFilters.value.age;
  if (listFilters.value.weight !== null) queryFilters.weight = listFilters.value.weight;

  queryFilters.special_condition = listFilters.value.special_condition;

  await loadMatches(queryFilters);
}

async function generateBrackets(): Promise<void> {
  generating.value = true;
  try {
    const result = await BracketService.generate({
      categoryModalityIds: selectedCategories.value.length > 0 ? selectedCategories.value : null,
    });
    const total = result.results.reduce((sum, r) => sum + r.matchesGenerated, 0);
    toast.add({
      severity: "success",
      summary: "Pirámides Generadas",
      detail: `${total} enfrentamientos creados en ${result.results.length} categoría(s).`,
      life: 5000,
    });
    await applyFilters();
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
  const [categoriesData, ranksData, modalitiesData] = await Promise.all([
    CategoryService.getAll(),
    RankService.getAll(),
    ModalityService.getAll()
  ]);
  categories.value = categoriesData;
  ranks.value = ranksData;
  modalities.value = modalitiesData;

  await loadMatches();
});
</script>

<template>
  <div class="card">
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-2xl font-bold">Pirámides</h2>
      <div class="flex gap-2 items-center">
        <MultiSelect v-model="selectedCategories" :options="categoryModalitiesDisplay" optionLabel="displayName"
          optionValue="id" placeholder="Categorías a generar..." class="w-64" />
        <Button icon="pi pi-bolt" label="Generar Pirámides" :loading="generating" @click="generateBrackets" />
      </div>
    </div>

    <!-- Filter Panel for Display -->
    <div class="p-fluid grid grid-flow-row grid-cols-3 mb-6 gap-2">
      <div class="flex flex-col col-1">
        <label for="rank">Rango</label>
        <Dropdown id="rank" v-model="listFilters.rank_id" :options="ranks" optionLabel="name" optionValue="id"
          placeholder="Cualquier Rango" showClear />
      </div>
      <div class="flex flex-col col-2">
        <label for="modality">Modalidad</label>
        <Dropdown id="modality" v-model="listFilters.modality_id" :options="modalities" optionLabel="name"
          optionValue="id" placeholder="Cualquier Modalidad" showClear />
      </div>
      <div class="flex flex-col col-3">
        <label for="age">Edad</label>
        <InputNumber id="age" v-model="listFilters.age" placeholder="Edad" />
      </div>
      <div class="flex flex-col col-1">
        <label for="weight">Peso (Kg)</label>
        <InputNumber id="weight" v-model="listFilters.weight" placeholder="Peso" mode="decimal" :minFractionDigits="0"
          :maxFractionDigits="2" />
      </div>
      <div class="flex items-center mb-3 col-3">
        <Checkbox inputId="special" v-model="listFilters.special_condition" :binary="true" />
        <label for="special" class="ml-2 mt-1">Condición Especial</label>
      </div>

      <div class="col-12 flex justify-end">
        <Button label="Buscar Enfrentamientos" icon="pi pi-search" @click="applyFilters" class="w-auto"
          :loading="loading" />
      </div>
    </div>

    <ProgressBar v-if="loading" mode="indeterminate" class="mb-4" style="height: 4px" />

    <div v-if="matchesByCategory.length === 0 && !loading" class="text-center text-surface-500 py-8">
      <i class="pi pi-sitemap text-4xl mb-4 block"></i>
      <p>No hay enfrentamientos generados o encontrados bajo los filtros actuales.</p>
    </div>

    <Accordion v-else :value="matchesByCategory[0]?.display?.id">
      <AccordionPanel v-for="group in matchesByCategory" :key="group.display?.id ?? 'uncategorized'"
        :value="group.display?.id ?? 'uncategorized'">
        <AccordionHeader>
          <div v-if="group.display" class="flex flex-wrap items-center gap-2 w-full pr-4">
            <span class="font-bold text-lg mr-2">{{ group.display.modality.modality.name }} | {{ group.display.sexesStr
            }} | {{ group.display.ageStr }} | {{ group.display.ranksStr }}</span>
            <Tag v-if="group.display.weightStr" severity="warn" :value="group.display.weightStr" rounded />
            <Tag v-if="group.display.isSpecial" severity="secondary" value="Cond. Especial" rounded />

            <Tag severity="contrast" :value="`${group.realMatchesCount} combates`" class="ml-auto" />
          </div>
          <div v-else class="flex w-full justify-between pr-4 items-center">
            <span class="font-bold">Sin categoría</span>
            <Tag severity="contrast" :value="`${group.realMatchesCount} combates`" />
          </div>
        </AccordionHeader>
        <AccordionContent>
          <TournamentBracket :matches="group.matches" />
        </AccordionContent>
      </AccordionPanel>
    </Accordion>
  </div>
</template>
