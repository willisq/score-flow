<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { useDialog } from "primevue/usedialog";
import { CategoryService } from "../services/CategoryService";
import type { Category } from "../types";
import CategoryForm from "./components/CategoryForm.vue";
import ModalityForm from "./components/ModalityForm.vue";
import CategoryCompetitorList from "./components/CategoryCompetitorList.vue";
import { useRegistrationData } from "@/features/registration/composables/useRegistrationData";
import { useTournamentData } from "../composables/useTournamentData";
import Button from "primevue/button";
import Tag from "primevue/tag";
import DataView from "primevue/dataview";
import Accordion from 'primevue/accordion';
import AccordionPanel from 'primevue/accordionpanel';
import AccordionHeader from 'primevue/accordionheader';
import AccordionContent from 'primevue/accordioncontent';

const dialog = useDialog();
const { ranks, sexes } = useRegistrationData();
const { modalities: allModalities } = useTournamentData();

const categories = ref<Category[]>([]);
const loading = ref(true);

// Grouping logic: Root = Age Range + Special Condition
const groupedCategories = computed(() => {
  const groups: Record<string, {
    id: string;
    ages: number[];
    specialCondition: boolean;
    categories: Category[];
    rankGroups: { id: string, name: string, modalities: any[], categoryIds: string[] }[]
  }> = {};

  categories.value.forEach((cat) => {
    const min = Math.min(...cat.ages);
    const max = Math.max(...cat.ages);
    const key = `${min}-${max}-${cat.specialCondition}`;

    if (!groups[key]) {
      groups[key] = {
        id: key,
        ages: [min, max],
        specialCondition: cat.specialCondition,
        categories: [],
        rankGroups: []
      };
    }
    groups[key].categories.push(cat);
  });

  // Calculate nested rank groups
  Object.values(groups).forEach(group => {
    const rgMap = new Map();
    group.categories.forEach(cat => {
      cat.modalities.forEach(mod => {
        const rgId = mod.rankGroup?.id || 'no-rank';
        const rgName = mod.rankGroup?.name || 'Varios / Sin Grupo';
        if (!rgMap.has(rgId)) {
          rgMap.set(rgId, { id: rgId, name: rgName, modalities: [], categoryIds: new Set() });
        }
        // Add modality but inject parent category for editing context if needed
        rgMap.get(rgId).modalities.push({ ...mod, _categoryId: cat.id });
        rgMap.get(rgId).categoryIds.add(cat.id);
      });
    });
    group.rankGroups = Array.from(rgMap.values()).map(rg => ({
      ...rg,
      categoryIds: Array.from(rg.categoryIds)
    }));
  });

  return Object.values(groups).sort((a, b) => a.ages[0] - b.ages[0]);
});

async function loadCategories(): Promise<void> {
  loading.value = true;
  try {
    categories.value = await CategoryService.getAll();
  } finally {
    loading.value = false;
  }
}

function openCreateDialog(): void {
  dialog.open(CategoryForm, {
    props: {
      header: "Crear Categoría",
      style: { width: "60vw" },
      breakpoints: { "960px": "85vw", "640px": "95vw" },
      modal: true,
      dismissableMask: true,
    },
    data: { ranks, sexes, modalities: allModalities },
    onClose: () => loadCategories(),
  });
}

function openEditDialog(category: Category): void {
  dialog.open(CategoryForm, {
    props: {
      header: "Editar Categoría",
      style: { width: "60vw" },
      breakpoints: { "960px": "85vw", "640px": "95vw" },
      modal: true,
      dismissableMask: true,
    },
    data: { category, ranks, sexes, modalities: allModalities },
    onClose: () => loadCategories(),
  });
}

function openModalityEditDialog(modality: any): void {
  dialog.open(ModalityForm, {
    props: {
      header: `Editar ${modality.modality.name}`,
      style: { width: "30vw" },
      breakpoints: { "960px": "50vw", "640px": "90vw" },
      modal: true,
      dismissableMask: true,
    },
    data: { modality, sexes },
    onClose: (options) => {
      if (options?.data) {
        loadCategories();
      }
    },
  });
}

function showCompetitors(categoryModality: any): void {
  dialog.open(CategoryCompetitorList, {
    props: {
      header: "Competidores en la Categoría",
      style: { width: "50vw" },
      breakpoints: { "960px": "80vw", "640px": "90vw" },
      modal: true,
      dismissableMask: true,
    },
    data: { categoryModality },
  });
}

onMounted(loadCategories);
</script>

<template>
  <div class="card p-4">
    <div class="flex justify-between items-center mb-6">
      <div>
        <h2 class="text-3xl font-bold bg-primary-500 bg-clip-text text-transparent inline-block">
          Gestión de Categorías
        </h2>
        <p class="text-surface-500 text-sm">Organización jerárquica por edades y requerimientos.</p>
      </div>
      <Button icon="pi pi-plus" label="Nueva Categoría" @click="openCreateDialog" class="shadow-2" />
    </div>

    <DataView :value="groupedCategories" :loading="loading" paginator :rows="10">
      <template #list="slotProps">
        <div class="flex flex-col gap-4 mt-2">
          <Accordion :value="slotProps.items[0]?.id">
            <AccordionPanel v-for="group in slotProps.items" :key="group.id" :value="group.id">

              <!-- Header del Grupo (Nivel 1: Edades) -->
              <AccordionHeader>
                <div class="flex justify-between items-center w-full pr-4">
                  <div class="flex items-center gap-3">
                    <div class="text-xl font-bold text-surface-900 dark:text-surface-0">
                      Edades: {{ group.ages[0] }} – {{ group.ages[1] }} años
                    </div>
                    <Tag v-if="group.specialCondition" value="Condición Especial" severity="warn" class="text-xs" />
                  </div>
                  <div class="text-surface-500 text-sm whitespace-nowrap">
                    {{ group.rankGroups.length }} rangos definidos
                  </div>
                </div>
              </AccordionHeader>

              <!-- Content de la Edad (Segundo Nivel de Agrupamiento) -->
              <AccordionContent>
                <div class="p-2 bg-surface-50 dark:bg-surface-900/50 rounded-b-lg">
                  <Accordion :value="group.rankGroups[0]?.id">
                    <AccordionPanel v-for="rg in group.rankGroups" :key="rg.id" :value="rg.id">

                      <AccordionHeader>
                        <div class="flex justify-between items-center w-full pr-4">
                          <div class="flex items-center gap-2">
                            <i class="pi pi-shield text-orange-500"></i>
                            <span class="font-bold text-surface-700 dark:text-surface-200 uppercase tracking-tighter">{{
                              rg.name }}</span>
                          </div>
                          <!-- Botón para editar la categoría raíz asociada a este rango en esta edad -->
                          <Button v-if="rg.categoryIds.length === 1" icon="pi pi-pencil" severity="secondary" text
                            rounded size="small"
                            @click.stop="openEditDialog(group.categories.find((c: Category) => c.id === rg.categoryIds[0])!)"
                            v-tooltip.top="'Editar Categoría Completa'" />
                        </div>
                      </AccordionHeader>

                      <AccordionContent>
                        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3 p-1">
                          <div v-for="mod in rg.modalities" :key="mod.id"
                            class="bg-surface-0 dark:bg-surface-800 p-4 border-round hover:border-primary-400 hover:shadow-lg transition-all shadow-sm relative group border border-surface-100 dark:border-surface-700">

                            <div class="flex justify-between items-start mb-3">
                              <div class="flex flex-col gap-1">
                                <Tag :value="mod.modality.name" severity="info" class="font-bold" />
                                <div class="flex gap-2 mt-1 items-center">
                                  <div class="flex gap-1">
                                    <i v-for="sex in mod.sexes" :key="sex.id"
                                      :class="['pi text-xs', sex.name.toLowerCase().includes('masc') ? 'pi-mars text-blue-500' : 'pi-venus text-pink-500']"
                                      v-tooltip.top="sex.name"></i>
                                  </div>
                                  <Button icon="pi pi-cog" severity="secondary" text rounded size="small"
                                    class="opacity-0 group-hover:opacity-100 transition-opacity !p-0 h-5 w-5"
                                    @click.stop="openModalityEditDialog(mod)"
                                    v-tooltip.top="'Configurar Subcategoría'" />
                                </div>
                              </div>
                            </div>

                            <div class="text-xs space-y-2 mb-4">
                              <div v-if="mod.physicalRequirement?.initialWeight != null"
                                class="flex justify-between items-center text-surface-600 dark:text-surface-400">
                                <span>Peso:</span>
                                <span class="font-bold text-surface-900 dark:text-surface-100">{{
                                  mod.physicalRequirement.initialWeight }}–{{ mod.physicalRequirement.finalWeight }}
                                  Kg</span>
                              </div>
                            </div>

                            <Button icon="pi pi-users" label="Ver Atletas"
                              class="text-[10px] py-1.5 px-3 h-9 w-full shadow-sm" severity="primary"
                              @click="showCompetitors(mod)" />
                          </div>
                        </div>
                      </AccordionContent>
                    </AccordionPanel>
                  </Accordion>
                </div>
              </AccordionContent>
            </AccordionPanel>
          </Accordion>
        </div>
      </template>

      <template #empty>
        <div class="flex flex-col items-center justify-center p-20 text-surface-400">
          <i class="pi pi-search text-6xl mb-4"></i>
          <p class="text-xl">No se han definido categorías aún.</p>
          <Button label="Crear la Primera" icon="pi pi-plus" @click="openCreateDialog" class="mt-4" />
        </div>
      </template>
    </DataView>
  </div>
</template>

<style scoped>
.surface-card {
  transition: transform 0.2s;
}

.surface-card:hover {
  transform: translateY(-2px);
}
</style>
