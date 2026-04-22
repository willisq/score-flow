<script setup lang="ts">
import { ref, reactive, onMounted, computed, watch } from 'vue';
import { useToast } from 'primevue/usetoast';
import Button from 'primevue/button';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Tag from 'primevue/tag';
import Card from 'primevue/card';
import InputNumber from 'primevue/inputnumber';
import MultiSelect from 'primevue/multiselect';
import Select from 'primevue/select';
import { CompetitorService } from '@/features/registration/services/CompetitorService';
import { InscriptionService } from '../services/InscriptionService';
import type {
  Competitor,
  CompetitorCategoryFilters,
  CompetitorFilterOptions,
} from '@/features/registration/types';
import { useTournamentData } from '../composables/useTournamentData';

// --- State ---
const toast = useToast();
const { activeTournament } = useTournamentData();

const loading = ref(false);
const submitting = ref(false);
const competitors = ref<Competitor[]>([]);
const filterOptions = ref<CompetitorFilterOptions | null>(null);

const filters = reactive<CompetitorCategoryFilters>({
  minAge: undefined,
  maxAge: undefined,
  rankIds: [],
  sexIds: [],
  specialCondition: undefined,
});

const specialConditionOptions = [
  { label: 'Si', value: true },
  { label: 'No', value: false }
];

// Selection state
const selectedStartId = ref<string | null>(null);
const selectedEndId = ref<string | null>(null);
const enrollmentQueue = ref<Competitor[]>([]);

// --- Computed ---
const selectedRange = computed(() => {
  if (!selectedStartId.value) return [];

  const startIndex = competitors.value.findIndex(c => c.id === selectedStartId.value);
  if (startIndex === -1) return [];

  if (!selectedEndId.value) return [competitors.value[startIndex]];

  const endIndex = competitors.value.findIndex(c => c.id === selectedEndId.value);
  if (endIndex === -1) return [competitors.value[startIndex]];

  const start = Math.min(startIndex, endIndex);
  const end = Math.max(startIndex, endIndex);

  return competitors.value.slice(start, end + 1);
});

const isRangeSelected = computed(() => selectedRange.value.length > 0);

// --- Methods ---
async function loadFilterOptions() {
  try {
    filterOptions.value = await CompetitorService.getFilterOptions();
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Error', detail: 'No se pudieron cargar las opciones de filtro', life: 3000 });
  }
}

async function fetchCompetitors() {
  loading.value = true;
  try {
    // Use the unregistered endpoint
    const rawCompetitors = await CompetitorService.getUnregisteredForCategoryBuilder(
      filters, 
      activeTournament.value?.id
    );
    
    // Remove competitors already in the queue from the list
    const queuedIds = new Set(enrollmentQueue.value.map(c => c.id));
    competitors.value = rawCompetitors.filter(c => !queuedIds.has(c.id));
    
    selectedStartId.value = null;
    selectedEndId.value = null;
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Error', detail: 'No se pudieron cargar los competidores', life: 3000 });
  } finally {
    loading.value = false;
  }
}

function handleRowClick(event: any) {
  const clickedId = event.data.id;

  if (!selectedStartId.value || (selectedStartId.value && selectedEndId.value)) {
    selectedStartId.value = clickedId;
    selectedEndId.value = null;
  } else {
    selectedEndId.value = clickedId;
  }
}

function isRowSelected(id: string) {
  if (!selectedStartId.value) return false;

  const startIndex = competitors.value.findIndex(c => c.id === selectedStartId.value);
  if (startIndex === -1) return false;

  if (!selectedEndId.value) return id === selectedStartId.value;

  const endIndex = competitors.value.findIndex(c => c.id === selectedEndId.value);
  const currentIndex = competitors.value.findIndex(c => c.id === id);

  const start = Math.min(startIndex, endIndex);
  const end = Math.max(startIndex, endIndex);

  return currentIndex >= start && currentIndex <= end;
}

function addToQueue() {
  if (selectedRange.value.length === 0) return;

  const range = selectedRange.value;

  enrollmentQueue.value.push(...range);

  // Remove these competitors from the table
  const assignedIds = new Set(range.map(c => c.id));
  competitors.value = competitors.value.filter(c => !assignedIds.has(c.id));

  // Clear selection
  selectedStartId.value = null;
  selectedEndId.value = null;
  
  toast.add({ severity: 'success', summary: 'Agregado', detail: `${range.length} competidores en cola`, life: 2000 });
}

function removeFromQueue(id: string) {
  enrollmentQueue.value = enrollmentQueue.value.filter(item => item.id !== id);
  // Re-fetch to repopulate the table safely
  fetchCompetitors();
}

async function submitBulk() {
  if (enrollmentQueue.value.length === 0) return;
  if (!activeTournament.value?.id) {
    toast.add({ severity: 'error', summary: 'Error', detail: 'Debe seleccionar un torneo activo.', life: 3000 });
    return;
  }

  submitting.value = true;
  try {
    const payload = {
      competitorIds: enrollmentQueue.value.map(item => item.id),
      tournamentId: activeTournament.value.id
    };
    
    const response = await InscriptionService.massRegister(payload);
    const successCount = response.registrations?.length || 0;
    const errorsCount = response.errors?.length || 0;
    
    if (errorsCount > 0) {
      toast.add({ severity: 'warn', summary: 'Inscripción parcial', detail: `${successCount} inscritos, ${errorsCount} fallaron. Las que fallaron volverán a la tabla.`, life: 5000 });
      // Remove successful ones from queue, keep errors.
      const errorIds = new Set(response.errors.map((e: any) => e.competitorId));
      enrollmentQueue.value = enrollmentQueue.value.filter(item => errorIds.has(item.id));
      fetchCompetitors();
    } else {
      toast.add({ severity: 'success', summary: 'Éxito', detail: `${successCount} competidores inscritos correctamente`, life: 3000 });
      enrollmentQueue.value = [];
    }
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Error', detail: 'Problema al procesar la inscripción', life: 3000 });
  } finally {
    submitting.value = false;
  }
}

async function submitAllLoaded() {
  if (competitors.value.length === 0 && enrollmentQueue.value.length === 0) return;
  if (!activeTournament.value?.id) {
    toast.add({ severity: 'error', summary: 'Error', detail: 'Debe seleccionar un torneo activo.', life: 3000 });
    return;
  }

  submitting.value = true;
  try {
    const allIds = [
      ...competitors.value.map(c => c.id),
      ...enrollmentQueue.value.map(c => c.id)
    ];

    const payload = {
      competitorIds: allIds,
      tournamentId: activeTournament.value.id
    };
    
    const response = await InscriptionService.massRegister(payload);
    const successCount = response.registrations?.length || 0;
    const errorsCount = response.errors?.length || 0;
    
    if (errorsCount > 0) {
      toast.add({ severity: 'warn', summary: 'Inscripción parcial', detail: `${successCount} inscritos, ${errorsCount} fallaron.`, life: 5000 });
      enrollmentQueue.value = [];
      fetchCompetitors();
    } else {
      toast.add({ severity: 'success', summary: 'Éxito', detail: `${allIds.length} competidores inscritos correctamente`, life: 3000 });
      enrollmentQueue.value = [];
      competitors.value = [];
      fetchCompetitors();
    }
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Error', detail: 'Problema al procesar la inscripción masiva', life: 3000 });
  } finally {
    submitting.value = false;
  }
}

onMounted(() => {
  loadFilterOptions();
  fetchCompetitors();
});

// Watch filters for changes
watch(filters, () => {
  fetchCompetitors();
}, { deep: true });

// Watch for tournament changes to refresh the "unregistered" list
watch(activeTournament, () => {
  fetchCompetitors();
});

</script>

<template>
  <div class="enrollment-view flex flex-col h-full gap-4 p-4">
    <!-- Header with Action -->
    <Card>
      <template #header>
        <div class="p-4">
          <h1 class="text-3xl font-bold bg-gradient-to-r from-primary-500 to-primary-700 bg-clip-text text-transparent">
            Inscripción Masiva
          </h1>
          <p class="text-surface-500 text-sm mt-1">
            Selecciona múltiples competidores para asignarlos a sus respectivas categorías.
          </p>
        </div>
      </template>
      <template #content>
        <div class="flex flex-wrap gap-3">
          <Button label="Inscribir Seleccionados" icon="pi pi-check-circle" severity="success"
            :disabled="enrollmentQueue.length === 0" :loading="submitting" @click="submitBulk" class="shadow-lg px-6">
            <template #icon>
              <div class="relative mr-2">
                <i class="pi pi-check-circle"></i>
                <span v-if="enrollmentQueue.length > 0"
                  class="absolute -top-3 -right-3 bg-red-500 text-white rounded-full text-[10px] w-5 h-5 flex items-center justify-center border-2 border-white dark:border-surface-900">
                  {{ enrollmentQueue.length }}
                </span>
              </div>
            </template>
          </Button>

          <Button label="Inscribir Todo el Listado" icon="pi pi-users" severity="primary"
            :disabled="competitors.length === 0 && enrollmentQueue.length === 0" :loading="submitting" @click="submitAllLoaded" class="shadow-lg px-6" />
        </div>
      </template>
    </Card>

    <!-- Main Workspace -->
    <div class="flex flex-1 gap-4 overflow-hidden">
      <!-- Left: Filters & Table -->
      <div class="flex-1 flex flex-col gap-4 overflow-hidden">
        <!-- Filter Bar -->
        <Card class="filter-bar border-none shadow-sm">
          <template #content>
            <div class="flex flex-wrap gap-4 items-end">
              <div class="flex flex-col gap-2 min-w-[150px]">
                <label class="text-xs font-bold uppercase text-surface-500">Rango Edad</label>
                <div class="flex items-center gap-2">
                  <InputNumber v-model="filters.minAge" placeholder="Mín" :min="0" class="w-20" fluid />
                  <span class="text-surface-400">-</span>
                  <InputNumber v-model="filters.maxAge" placeholder="Máx" :min="0" class="w-20" fluid />
                </div>
              </div>

              <div class="flex flex-col gap-2 min-w-[200px] flex-1">
                <label class="text-xs font-bold uppercase text-surface-500">Rangos</label>
                <MultiSelect v-model="filters.rankIds" :options="filterOptions?.ranks || []" optionLabel="name"
                  optionValue="id" placeholder="Filtrar Rangos" class="w-full" display="chip" />
              </div>

              <div class="flex flex-col gap-2 min-w-[150px]">
                <label class="text-xs font-bold uppercase text-surface-500">Sexo</label>
                <MultiSelect v-model="filters.sexIds" :options="filterOptions?.sexes || []" optionLabel="name"
                  optionValue="id" placeholder="Seleccionar" class="w-full" />
              </div>

              <div class="flex flex-col gap-2 min-w-[120px]">
                <label class="text-xs font-bold uppercase text-surface-500">Condición Esp.</label>
                <Select v-model="filters.specialCondition" :options="specialConditionOptions" optionLabel="label"
                  optionValue="value" placeholder="Cualquiera" class="w-full" />
              </div>

              <div class="flex items-center gap-2">
                <Button icon="pi pi-refresh" severity="secondary" text rounded aria-label="Recargar"
                  @click="fetchCompetitors" />
              </div>
            </div>
          </template>
        </Card>

        <!-- Competitor Table -->
        <Card>
          <template #content>
            <DataTable :value="competitors" :loading="loading" class="p-datatable-sm h-full" scrollable
              scrollHeight="flex" @row-click="handleRowClick" dataKey="id">
              <Column field="firstName" header="Competidor">
                <template #body="slotProps">
                  <div class="flex flex-col"
                    :class="{ 'text-primary-600 dark:text-primary-400 font-bold': isRowSelected(slotProps.data.id) }">
                    <span>{{ slotProps.data.firstName }} {{ slotProps.data.lastName }}</span>
                    <span class="text-[10px] opacity-60">{{ slotProps.data.academy.name }}</span>
                  </div>
                </template>
              </Column>
              <Column field="age" header="Edad" style="width: 70px" />
              <Column field="weight" header="Peso" style="width: 90px">
                <template #body="slotProps">
                  {{ slotProps.data.weight ? slotProps.data.weight.toFixed(1) + 'kg' : '-' }}
                </template>
              </Column>
              <Column field="rank.name" header="Rango">
                <template #body="slotProps">
                  <Tag :value="slotProps.data.rank.name" severity="secondary" class="text-[10px]" />
                </template>
              </Column>
              <Column field="specialCondition" header="C.E." style="width: 60px">
                <template #body="slotProps">
                  <Tag :value="slotProps.data.specialCondition ? 'SÍ' : 'NO'"
                    :severity="slotProps.data.specialCondition ? 'warn' : 'secondary'" class="text-[10px]" />
                </template>
              </Column>
              <Column field="sex.name" header="Sexo" style="width: 60px">
                <template #body="slotProps">
                  <i :class="[
                    'pi text-base',
                    slotProps.data.sex.name === 'Masculino' || slotProps.data.sex.name === 'Hombre'
                      ? 'pi-mars text-blue-500'
                      : 'pi-venus text-pink-500',
                  ]"></i>
                </template>
              </Column>

              <template #empty>
                <div class="flex flex-col items-center justify-center p-12 text-surface-400">
                  <i class="pi pi-filter-slash text-5xl mb-4"></i>
                  <p>No hay competidores que coincidan.</p>
                </div>
              </template>
            </DataTable>
          </template>
        </Card>
      </div>

      <!-- Right: Action Sidebars -->
      <div class="w-80 lg:w-96 flex flex-col gap-4 overflow-hidden">
        <!-- Range Selection Info -->
        <Card class="flex-none border-primary-100 dark:border-primary-900 shadow-md">
          <template #title>
            <div class="text-lg flex items-center gap-2">
              <i class="pi pi-user-plus text-primary-500"></i>
              <span>Preparar Inscripción</span>
            </div>
          </template>
          <template #content>
            <div v-if="isRangeSelected" class="space-y-4">
              <div
                class="bg-surface-50 dark:bg-surface-800 p-3 rounded-md border border-surface-200 dark:border-surface-700">
                <div class="flex justify-between text-xs mb-2 text-surface-500 font-bold uppercase">
                  <span>Seleccionados</span>
                  <span class="text-primary-500">{{ selectedRange.length }}</span>
                </div>
                <div class="max-h-24 overflow-y-auto text-[11px] space-y-1">
                  <div v-for="c in selectedRange" :key="c.id" class="flex justify-between">
                    <span class="truncate pr-2">{{ c.firstName }} {{ c.lastName }}</span>
                    <span class="text-surface-400 whitespace-nowrap">{{ c.age }}a / {{ c.weight }}k</span>
                  </div>
                </div>
              </div>

              <div class="space-y-3">
                <Button label="Añadir a la Cola" icon="pi pi-plus" class="w-full"
                  :disabled="!isRangeSelected" @click="addToQueue" />
              </div>
            </div>
            <div v-else class="text-center py-8 px-4 opacity-50 space-y-4">
              <div
                class="w-16 h-16 bg-surface-100 dark:bg-surface-800 rounded-full flex items-center justify-center mx-auto mb-2">
                <i class="pi pi-mouse-pointer text-2xl"></i>
              </div>
              <p class="text-sm">Selecciona uno o más competidores en la tabla para enlistarlos.</p>
            </div>
          </template>
        </Card>

        <!-- Queue -->
        <Card class="flex-1 overflow-hidden flex flex-col border-none shadow-lg">
          <template #title>
            <div class="text-lg flex items-center justify-between">
              <div class="flex items-center gap-2">
                <i class="pi pi-users text-primary-500"></i>
                <span>En Cola</span>
              </div>
              <Tag :value="enrollmentQueue.length" severity="info" rounded />
            </div>
          </template>
          <template #content>
            <div class="flex flex-col h-full overflow-hidden">
              <div v-if="enrollmentQueue.length > 0" class="flex-1 overflow-y-auto space-y-3 pr-2 custom-scrollbar">
                <div v-for="competitor in enrollmentQueue" :key="competitor.id"
                  class="group p-3 rounded-lg border border-surface-200 dark:border-surface-700 hover:border-primary-500 transition-all bg-surface-0 dark:bg-surface-900 shadow-sm relative">
                  <div class="pr-5">
                    <div class="text-sm font-bold text-primary-600 dark:text-primary-400">
                      {{ competitor.firstName }} {{ competitor.lastName }}
                    </div>
                    <div class="text-xs opacity-70 mt-1">
                      {{ competitor.age }} años | {{ competitor.weight?.toFixed(1) || '-' }} kg
                    </div>
                    <div class="mt-2 flex flex-wrap gap-1 items-center">
                      <Tag :value="competitor.rank.name" severity="secondary" class="text-[9px] px-1 h-5" />
                      <Tag v-if="competitor.specialCondition" icon="pi pi-star" value="CE" severity="warn"
                        class="text-[8px] px-1 h-5" />
                      <i :class="[
                        'pi text-[10px] ml-1',
                        competitor.sex.name === 'Masculino' || competitor.sex.name === 'Hombre'
                          ? 'pi-mars text-blue-500'
                          : 'pi-venus text-pink-500',
                      ]"></i>
                    </div>
                  </div>
                  <Button icon="pi pi-times" severity="danger" text rounded
                    class="absolute top-1 right-1 h-8 w-8 !p-0 opacity-0 group-hover:opacity-100 transition-opacity"
                    @click="removeFromQueue(competitor.id)" />
                </div>
              </div>
              <div v-else class="flex-1 flex flex-col items-center justify-center opacity-30 text-center p-4">
                <i class="pi pi-inbox text-4xl mb-2"></i>
                <p class="text-sm">No hay competidores listos para inscribir.</p>
              </div>
            </div>
          </template>
        </Card>
      </div>
    </div>
  </div>
</template>

<style scoped>
.enrollment-view {
  animation: slideUp 0.4s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

:deep(.p-datatable-row) {
  cursor: pointer;
}

:deep(.p-datatable-tbody > tr.bg-primary-50) {
  background-color: var(--p-primary-50) !important;
}

.dark :deep(.p-datatable-tbody > tr.bg-primary-900\/20) {
  background-color: rgba(var(--p-primary-500-rgb), 0.15) !important;
}
</style>
