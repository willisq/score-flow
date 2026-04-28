<script setup lang="ts">
import { ref, onMounted, computed, nextTick } from "vue";
import { useToast } from "primevue/usetoast";
import { useConfirm } from "primevue/useconfirm";
import { useBracketData } from "../composables/useBracketData";
import { useBracketExport } from "../composables/useBracketExport";
import { BracketService } from "../services/BracketService";
import { CategoryService } from "@/features/tournament/services/CategoryService";
import { ModalityService } from "@/features/tournament/services/ModalityService";
import { RankService } from "@/features/registration/services/RankService";
import { SexService } from "@/features/registration/services/SexService";
import type { Category, Modality } from "@/features/tournament/types";
import type { Rank, Sex } from "@/features/registration/types";
import type { Match } from "../types";
import TournamentBracket from "./components/TournamentBracket.vue";

const toast = useToast();
const confirm = useConfirm();
const { matches, loading, loadMatches } = useBracketData();
const { exportToPdf, exportAllToPdf } = useBracketExport();
const isDeleting = ref(false);
const pendingDeletePayload = ref<{ registrationId: string; categoryModalityId: string } | null>(null);

async function handleDeleteCompetitor(payload: { registrationId: string; categoryModalityId: string }) {
  if (isDeleting.value) return;
  pendingDeletePayload.value = payload;
  confirm.require({
    group: 'competitorDelete',
    header: 'Confirmar eliminación',
    message: '¿Cómo deseas eliminar a este competidor? Puedes quitarlo solo de esta pirámide (se mantiene en la categoría) o eliminar su inscripción permanentemente.',
    icon: 'pi pi-user-minus',
  });
}

async function handleConfirmCompetitorDelete(removeFromCategory: boolean) {
  if (!pendingDeletePayload.value) return;
  const payload = pendingDeletePayload.value;
  confirm.close();
  
  isDeleting.value = true;
  loading.value = true;
  try {
    await BracketService.removeCompetitor(payload.categoryModalityId, payload.registrationId, removeFromCategory);
    toast.add({ 
      severity: "success", 
      summary: removeFromCategory ? "Eliminado de categoría" : "Quitado de pirámide", 
      detail: "La pirámide ha sido regenerada.", 
      life: 3000 
    });
    await applyFilters();
  } catch (error) {
    toast.add({ severity: "error", summary: "Error", detail: "No se pudo realizar la operación.", life: 3000 });
  } finally {
    loading.value = false;
    isDeleting.value = false;
    pendingDeletePayload.value = null;
  }
}

async function handleDeletePyramid(cmId: string) {
  if (isDeleting.value) return;
  isDeleting.value = true;
  confirm.require({
    message: "¿Estás seguro de que deseas eliminar esta pirámide completa? Todos los enfrentamientos de esta categoría serán borrados.",
    header: "Confirmar eliminación",
    icon: "pi pi-exclamation-triangle",
    acceptProps: { label: "Eliminar", severity: "danger" },
    rejectProps: { label: "Cancelar", severity: "secondary", outlined: true },
    accept: async () => {
      loading.value = true;
      try {
        await BracketService.delete(cmId);
        toast.add({ severity: "success", summary: "Pirámide eliminada", life: 3000 });
        await applyFilters();
      } catch (error) {
        toast.add({ severity: "error", summary: "Error", detail: "No se pudo eliminar la pirámide.", life: 3000 });
      } finally {
        loading.value = false;
        isDeleting.value = false;
      }
    },
    onHide: () => {
      isDeleting.value = false;
    }
  });
}

async function handleDeleteCategory(cmId: string) {
  if (isDeleting.value) return;
  isDeleting.value = true;
  confirm.require({
    message: "¿Estás seguro de que deseas eliminar esta categoría completa? Se borrarán todas las configuraciones de esta categoría en el torneo. Esta acción no se puede deshacer.",
    header: "Confirmar eliminación de Categoría",
    icon: "pi pi-exclamation-triangle",
    acceptProps: { label: "Eliminar Todo", severity: "danger" },
    rejectProps: { label: "Cancelar", severity: "secondary", outlined: true },
    accept: async () => {
      loading.value = true;
      try {
        await CategoryService.deleteModality(cmId);
        toast.add({ severity: "success", summary: "Categoría eliminada", life: 3000 });
        await applyFilters();
        // Refresh categories list
        const allCats = await CategoryService.getAll(true);
        categories.value = allCats;
      } catch (error) {
        toast.add({ severity: "error", summary: "Error", detail: "No se pudo eliminar la categoría.", life: 3000 });
      } finally {
        loading.value = false;
        isDeleting.value = false;
      }
    },
    onHide: () => {
      isDeleting.value = false;
    }
  });
}

const categories = ref<Category[]>([]);
const selectedCategories = ref<string[]>([]);
const generating = ref(false);
const exportingId = ref<string | null>(null);
const exportingGlobal = ref(false);
const activePanels = ref<string[]>([]);

function getBracketInfo(group: any) {
  const matchesByRound: Record<string, any[]> = {};
  for (const m of group.matches) {
    if (!matchesByRound[m.round.id]) matchesByRound[m.round.id] = [];
    matchesByRound[m.round.id].push(m);
  }
  const sortedRounds = Object.values(matchesByRound).sort((a, b) => b.length - a.length);
  const firstRoundSize = sortedRounds.length > 0 ? sortedRounds[0].length : 0;
  
  // If more than 8 matches in the first round, use portrait (vertical)
  const orientation = firstRoundSize > 8 ? "portrait" : "landscape";

  return {
    id: group.display?.id,
    elementId: `bracket-${group.display?.id}`,
    modalityName: group.display?.modality.modality.name,
    ageStr: group.display?.ageStr,
    sexesStr: group.display?.sexesStr,
    ranksStr: group.display?.ranksStr,
    weightStr: group.display?.weightStr,
    orientation
  };
}

async function handleExport(group: any) {
  exportingId.value = group.display.id;
  try {
    const info = getBracketInfo(group);
    await exportToPdf(info.elementId, info);
  } finally {
    exportingId.value = null;
  }
}

async function handleExportAll() {
  const previousPanels = [...activePanels.value];
  exportingGlobal.value = true;
  try {
    // Open all panels to ensure they are rendered for html2canvas
    activePanels.value = matchesByCategory.value
      .filter(g => g.display)
      .map(g => g.display.id);
    
    await nextTick();
    // Small delay to ensure layout is stable
    await new Promise(resolve => setTimeout(resolve, 500));

    const allInfo = matchesByCategory.value
      .filter(g => g.display)
      .map(g => getBracketInfo(g));
    
    await exportAllToPdf(allInfo);
    
    toast.add({
      severity: "success",
      summary: "Reporte Generado",
      detail: "Se ha generado el PDF con todas las pirámides.",
      life: 3000
    });
  } catch (error) {
    console.error(error);
    toast.add({
      severity: "error",
      summary: "Error",
      detail: "No se pudo generar el reporte global.",
      life: 3000
    });
  } finally {
    activePanels.value = previousPanels;
    exportingGlobal.value = false;
  }
}

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
const sexes = ref<Sex[]>([]);

const listFilters = ref({
  rank_id: null as string | null,
  modality_id: null as string | null,
  sex_id: null as string | null,
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
  if (listFilters.value.sex_id) queryFilters.sex_id = listFilters.value.sex_id;
  if (listFilters.value.age !== null) queryFilters.age = listFilters.value.age;
  if (listFilters.value.weight !== null) queryFilters.weight = listFilters.value.weight;

  queryFilters.special_condition = listFilters.value.special_condition;

  await loadMatches(queryFilters);
  if (matchesByCategory.value.length > 0) {
    activePanels.value = [matchesByCategory.value[0].display?.id].filter(Boolean) as string[];
  }
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
  const [categoriesData, ranksData, modalitiesData, sexesData] = await Promise.all([
    CategoryService.getAll(true),
    RankService.getAll(),
    ModalityService.getAll(),
    SexService.getAll()
  ]);
  categories.value = categoriesData;
  ranks.value = ranksData;
  modalities.value = modalitiesData;
  sexes.value = sexesData;

  await loadMatches();
  if (matchesByCategory.value.length > 0) {
    activePanels.value = [matchesByCategory.value[0].display?.id].filter(Boolean) as string[];
  }
});
</script>

<template>
  <div class="card max-w-full overflow-auto">
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-2xl font-bold">Pirámides</h2>
      <div class="flex gap-2 items-center">
        <MultiSelect v-model="selectedCategories" :options="categoryModalitiesDisplay" optionLabel="displayName"
          optionValue="id" placeholder="Categorías a generar..." class="w-64" :filter="true"
          :virtualScrollerOptions="{ itemSize: 44 }" />
        <Button icon="pi pi-bolt" label="Generar" :loading="generating" @click="generateBrackets" />
        <Button icon="pi pi-file-pdf" label="Reporte Global" severity="secondary" :loading="exportingGlobal"
          :disabled="matchesByCategory.length === 0" @click="handleExportAll" />
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
        <label for="sex">Sexo</label>
        <Dropdown id="sex" v-model="listFilters.sex_id" :options="sexes" optionLabel="name" optionValue="id"
          placeholder="Cualquier Sexo" showClear />
      </div>
      <div class="flex flex-col col-1">
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

    <Accordion v-else v-model:value="activePanels" multiple>
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
          <div class="flex justify-between items-center mt-6 mb-2">
            <Button label="Exportar PDF" icon="pi pi-file-pdf" severity="secondary" outlined size="small"
              :loading="exportingId === group.display?.id" @click="handleExport(group)" />

            <div class="flex gap-2 no-print">
              <Button v-if="group.display" label="Eliminar Pirámide" icon="pi pi-times" severity="danger" outlined size="small"
                @click.stop="handleDeletePyramid(group.display.id)" />
              <Button v-if="group.display" label="Eliminar Categoría" icon="pi pi-trash" severity="danger" size="small"
                @click.stop="handleDeleteCategory(group.display.id)" />
            </div>
          </div>
          <div class="w-full overflow-x-auto min-w-0">
            <TournamentBracket :id="`bracket-${group.display?.id}`" :matches="group.matches" :show-edit="true"
              @delete-competitor="handleDeleteCompetitor" />
          </div>
        </AccordionContent>
      </AccordionPanel>
    </Accordion>

    <ConfirmDialog />
    <ConfirmDialog group="competitorDelete">
      <template #container="{ message }">
        <div class="flex flex-col items-center p-6 bg-surface-0 dark:bg-surface-900 rounded-lg shadow-lg border border-surface-200 dark:border-surface-700 max-w-md">
          <div class="rounded-full bg-primary-100 dark:bg-primary-900/30 p-4 mb-4">
            <i :class="message.icon" class="text-3xl text-primary-600"></i>
          </div>
          <span class="font-bold text-xl mb-2">{{ message.header }}</span>
          <p class="text-surface-600 dark:text-surface-400 text-center mb-6">{{ message.message }}</p>
          <div class="flex flex-wrap justify-center gap-2 w-full">
            <Button label="Cancelar" severity="secondary" outlined @click="confirm.close()" class="flex-1 min-w-[100px]" />
            <Button label="Solo Pirámide" severity="warn" icon="pi pi-minus-circle" @click="handleConfirmCompetitorDelete(false)" class="flex-1 min-w-[150px]" />
            <Button label="De Categoría" severity="danger" icon="pi pi-trash" @click="handleConfirmCompetitorDelete(true)" class="flex-1 min-w-[150px]" />
          </div>
        </div>
      </template>
    </ConfirmDialog>
  </div>
</template>
