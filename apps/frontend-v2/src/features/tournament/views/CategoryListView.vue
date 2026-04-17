<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { useDialog } from "primevue/usedialog";
import { CategoryService } from "../services/CategoryService";
import type { Category } from "../types";
import CategoryForm from "./components/CategoryForm.vue";
import CategoryCompetitorList from "./components/CategoryCompetitorList.vue";
import { useRegistrationData } from "@/features/registration/composables/useRegistrationData";
import { useTournamentData } from "../composables/useTournamentData";
import Button from "primevue/button";
import Tag from "primevue/tag";
import DataView from "primevue/dataview";

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
    items: Category[] 
  }> = {};

  categories.value.forEach((cat) => {
    const min = Math.min(...cat.ages);
    const max = Math.max(...cat.ages);
    const key = `${min}-${max}-${cat.specialCondition}`;
    
    if (!groups[key]) {
      groups[key] = {
        id: key,
        ages: cat.ages,
        specialCondition: cat.specialCondition,
        items: [],
      };
    }
    groups[key].items.push(cat);
  });

  return Object.values(groups).sort((a, b) => Math.min(...a.ages) - Math.min(...b.ages));
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

function getUniqueRanks(cat: Category) {
  const allRanks = cat.modalities.flatMap(m => 
    m.rankGroup?.ranks || m.ranks || []
  );
  const seen = new Set();
  return allRanks.filter(r => {
    if (seen.has(r.id)) return false;
    seen.add(r.id);
    return true;
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
        <div class="flex flex-col gap-4">
          <div
            v-for="group in slotProps.items"
            :key="group.id"
            class="surface-card border-1 border-surface-200 dark:border-surface-700 border-round overflow-hidden shadow-1"
          >
            <!-- Header del Grupo (Elemento Padre) -->
            <div class="bg-surface-50 dark:bg-surface-900 p-4 border-b-1 border-surface-200 dark:border-surface-700 flex justify-between items-center">
              <div class="flex items-center gap-3">
                <div class="bg-primary-500 text-white w-10 h-10 border-round flex items-center justify-center font-bold shadow-2">
                  {{ Math.min(...group.ages) }}+
                </div>
                <div>
                  <div class="text-xl font-bold">
                    Rango: {{ Math.min(...group.ages) }} – {{ Math.max(...group.ages) }} años
                  </div>
                  <Tag v-if="group.specialCondition" value="Condición Especial" severity="warn" class="text-xs" />
                </div>
              </div>
              <div class="text-surface-400 text-sm italic">
                {{ group.items.length }} subcategorías definidas
              </div>
            </div>

            <!-- Lista de Subcategorías (Hijos) -->
            <div class="p-0">
              <div v-for="(cat, idx) in group.items" :key="cat.id" 
                   class="flex flex-col p-4"
                   :class="{ 'border-t-1 border-surface-100 dark:border-surface-800': idx !== 0 }">
                
                <div class="flex flex-col md:flex-row justify-between gap-4">
                  <!-- Detalles de Sexo y Rangos -->
                  <div class="flex-1 flex flex-col gap-3">
                    <div class="flex items-center gap-2 flex-wrap">
                      <span class="text-sm font-semibold uppercase text-surface-400">Géneros:</span>
                      <div class="flex gap-1">
                        <i v-for="sex in cat.sexes" :key="sex.id" 
                           :class="['pi text-lg', sex.name.toLowerCase().includes('masc') ? 'pi-mars text-blue-500' : 'pi-venus text-pink-500']"
                           :title="sex.name"></i>
                      </div>
                    </div>
                    
                    <div class="flex items-center gap-2 flex-wrap">
                      <span class="text-sm font-semibold uppercase text-surface-400">Rangos:</span>
                      <div class="flex gap-1 flex-wrap">
                        <Tag v-for="rank in getUniqueRanks(cat)" :key="rank.id" :value="rank.name" severity="secondary" class="text-[10px]" />
                      </div>
                    </div>
                  </div>

                  <!-- Botón de Acción de la Categoría -->
                  <div class="flex items-start">
                    <Button icon="pi pi-pencil" severity="secondary" text rounded @click="openEditDialog(cat)" title="Editar Categoría" />
                  </div>
                </div>

                <!-- Modalidades específicas de esta combinación -->
                <div class="mt-4 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                  <div v-for="mod in cat.modalities" :key="mod.id" 
                       class="bg-surface-0 dark:bg-surface-800 border-1 border-surface-100 dark:border-surface-700 p-3 border-round hover:border-primary-300 transition-colors shadow-sm relative group">
                    <div class="flex justify-between items-start mb-2">
                       <div class="flex flex-col gap-1">
                         <Tag :value="mod.modality.name" severity="info" />
                         <span v-if="mod.rankGroup" class="text-[10px] font-bold opacity-60">
                           {{ mod.rankGroup.name }}
                         </span>
                       </div>
                    </div>
                    
                    <div class="text-xs space-y-1">
                      <div v-if="mod.physicalRequirement?.initialWeight != null" class="flex justify-between">
                         <span class="opacity-60">Peso:</span>
                         <span class="font-bold">{{ mod.physicalRequirement.initialWeight }}–{{ mod.physicalRequirement.finalWeight }} Kg</span>
                      </div>
                      <div v-if="mod.physicalRequirement?.initialHeight != null" class="flex justify-between">
                         <span class="opacity-60">Altura:</span>
                         <span class="font-bold">{{ mod.physicalRequirement.initialHeight }}–{{ mod.physicalRequirement.finalHeight }} cm</span>
                      </div>
                    </div>

                    <div class="mt-3 flex gap-2">
                      <Button icon="pi pi-users" label="Ver Atletas" 
                              class="text-[10px] py-1 px-2 h-8 w-full" 
                              @click="showCompetitors(mod)" />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
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
