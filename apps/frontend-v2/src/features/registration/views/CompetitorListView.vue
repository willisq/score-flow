<script setup lang="ts">
import { ref, reactive, computed, onMounted, watch } from "vue";
import { useDialog } from "primevue/usedialog";
import { CompetitorService } from "../services/CompetitorService";
import { useRegistrationData } from "../composables/useRegistrationData";
import type { Competitor, CompetitorFilters } from "../types";
import CompetitorForm from "./components/CompetitorForm.vue";
import CompetitorUploadDialog from "./components/CompetitorUploadDialog.vue";

const dialog = useDialog();
const { academies, ranks, sexes } = useRegistrationData();

const allCompetitors = ref<Competitor[]>([]);
const loading = ref(true);

// --- Filters ---
const filters = reactive<CompetitorFilters>({
  name: undefined,
  academyId: undefined,
  rankId: undefined,
  sexId: undefined,
  specialCondition: undefined,
});

const ageMin = ref<number | undefined>(undefined);
const ageMax = ref<number | undefined>(undefined);

const specialConditionOptions = [
  { label: "Sí", value: true },
  { label: "No", value: false },
];

// Client-side age filter (backend CompetitorFilters doesn't support age)
const competitors = computed(() => {
  return allCompetitors.value.filter((c) => {
    if (ageMin.value != null && (c.age == null || c.age < ageMin.value)) return false;
    if (ageMax.value != null && (c.age == null || c.age > ageMax.value)) return false;
    return true;
  });
});

// --- Data Loading ---
async function loadCompetitors(): Promise<void> {
  loading.value = true;
  try {
    const cleanFilters: Record<string, unknown> = {};
    if (filters.name) cleanFilters.name = filters.name;
    if (filters.academyId) cleanFilters.academyId = filters.academyId;
    if (filters.rankId) cleanFilters.rankId = filters.rankId;
    if (filters.sexId) cleanFilters.sexId = filters.sexId;
    if (filters.specialCondition !== undefined) cleanFilters.specialCondition = filters.specialCondition;

    allCompetitors.value = await CompetitorService.getAll(cleanFilters as CompetitorFilters);
  } finally {
    loading.value = false;
  }
}

function clearFilters(): void {
  filters.name = undefined;
  filters.academyId = undefined;
  filters.rankId = undefined;
  filters.sexId = undefined;
  filters.specialCondition = undefined;
  ageMin.value = undefined;
  ageMax.value = undefined;
}

// Re-fetch when backend-supported filters change
watch(
  () => ({ ...filters }),
  () => loadCompetitors(),
  { deep: true }
);

// --- Dialogs ---
function openCreateDialog(): void {
  dialog.open(CompetitorForm, {
    props: {
      header: "Crear Competidor",
      style: { width: "30vw" },
      breakpoints: { "960px": "60vw", "640px": "90vw" },
      modal: true,
      dismissableMask: true,
    },
    data: { academies, ranks, sexes },
    onClose: () => loadCompetitors(),
  });
}

function openEditDialog(competitor: Competitor): void {
  dialog.open(CompetitorForm, {
    props: {
      header: "Editar Competidor",
      style: { width: "30vw" },
      breakpoints: { "960px": "60vw", "640px": "90vw" },
      modal: true,
      dismissableMask: true,
    },
    data: { academies, ranks, sexes, competitor },
    onClose: () => loadCompetitors(),
  });
}

function openUploadDialog(): void {
  dialog.open(CompetitorUploadDialog, {
    props: {
      header: "Registro Masivo (Excel)",
      style: { width: "30vw" },
      breakpoints: { "960px": "60vw", "640px": "90vw" },
      modal: true,
      dismissableMask: true,
    },
    onClose: () => loadCompetitors(),
  });
}

onMounted(loadCompetitors);
</script>

<template>
  <div class="card">
    <h2 class="text-2xl font-bold mb-4">Competidores</h2>
    <DataTable :value="competitors" :loading="loading" paginator :rows="10">
      <template #header>
        <div class="flex flex-col gap-4">
          <!-- Filter Bar -->
          <div class="flex flex-wrap gap-3 items-end">
            <div class="flex flex-col gap-1 min-w-[200px] flex-1">
              <label class="text-xs font-bold uppercase text-surface-500">Nombre</label>
              <InputText v-model="filters.name" placeholder="Buscar por nombre..." class="w-full" />
            </div>

            <div class="flex flex-col gap-1 min-w-[160px]">
              <label class="text-xs font-bold uppercase text-surface-500">Rango</label>
              <Select
                v-model="filters.rankId"
                :options="ranks"
                optionLabel="name"
                optionValue="id"
                placeholder="Todos"
                showClear
                class="w-full"
              />
            </div>

            <div class="flex flex-col gap-1 min-w-[140px]">
              <label class="text-xs font-bold uppercase text-surface-500">Sexo</label>
              <Select
                v-model="filters.sexId"
                :options="sexes"
                optionLabel="name"
                optionValue="id"
                placeholder="Todos"
                showClear
                class="w-full"
              />
            </div>

            <div class="flex flex-col gap-1 min-w-[180px]">
              <label class="text-xs font-bold uppercase text-surface-500">Rango Edad</label>
              <div class="flex items-center gap-2">
                <InputNumber v-model="ageMin" placeholder="Mín" :min="0" class="w-20" fluid />
                <span class="text-surface-400">–</span>
                <InputNumber v-model="ageMax" placeholder="Máx" :min="0" class="w-20" fluid />
              </div>
            </div>

            <div class="flex flex-col gap-1 min-w-[130px]">
              <label class="text-xs font-bold uppercase text-surface-500">Cond. Especial</label>
              <Select
                v-model="filters.specialCondition"
                :options="specialConditionOptions"
                optionLabel="label"
                optionValue="value"
                placeholder="Todos"
                showClear
                class="w-full"
              />
            </div>

            <div class="flex items-end gap-1">
              <Button
                icon="pi pi-filter-slash"
                severity="secondary"
                text
                rounded
                aria-label="Limpiar filtros"
                @click="clearFilters"
                v-tooltip.top="'Limpiar filtros'"
              />
              <Button
                icon="pi pi-refresh"
                severity="secondary"
                text
                rounded
                aria-label="Recargar"
                @click="loadCompetitors"
                v-tooltip.top="'Recargar'"
              />
            </div>
          </div>

          <!-- Actions -->
          <div class="flex justify-end gap-2">
            <Button icon="pi pi-upload" label="Carga Masiva" severity="secondary" @click="openUploadDialog" />
            <Button icon="pi pi-plus" label="Crear Competidor" @click="openCreateDialog" />
          </div>
        </div>
      </template>

      <Column header="Nombre">
        <template #body="{ data }">
          {{ data.firstName }} {{ data.lastName }}
        </template>
      </Column>

      <Column field="academy.name" header="Academia" :sortable="true" />

      <Column field="rank.name" header="Rango" :sortable="true" />

      <Column header="Sexo">
        <template #body="{ data }">
          <i
            :class="[
              'pi',
              data.sex.name === 'Masculino' || data.sex.name === 'Hombre'
                ? 'pi-mars text-blue-500'
                : 'pi-venus text-pink-500',
            ]"
          ></i>
        </template>
      </Column>

      <Column field="weight" header="Peso">
        <template #body="{ data }">
          {{ data.weight ? `${data.weight} Kg` : "—" }}
        </template>
      </Column>

      <Column field="height" header="Altura">
        <template #body="{ data }">
          {{ data.height ? `${data.height} cm` : "—" }}
        </template>
      </Column>

      <Column field="age" header="Edad">
        <template #body="{ data }">
          {{ data.age ? `${data.age} años` : "—" }}
        </template>
      </Column>

      <Column header="Cond. Especial">
        <template #body="{ data }">
          <Tag v-if="data.specialCondition" value="Sí" severity="info" />
          <span v-else>No</span>
        </template>
      </Column>

      <Column header="Acciones" style="width: 5rem">
        <template #body="{ data }">
          <Button icon="pi pi-pencil" text rounded @click="openEditDialog(data)" />
        </template>
      </Column>
    </DataTable>
  </div>
</template>
