<script setup lang="ts">
import { ref, inject, onMounted, computed } from 'vue';
import InputNumber from 'primevue/inputnumber';
import MultiSelect from 'primevue/multiselect';
import Dropdown from 'primevue/dropdown';
import Button from 'primevue/button';
import Message from 'primevue/message';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import { CategoryService } from '../../services/CategoryService';
import { RankGroupService } from '../../services/RankGroupService';
import type { CategoryModality, RankGroup } from '../../types';
import type { Sex } from '@/features/registration/types';

const dialogRef = inject<any>("dialogRef");

const modality = ref<CategoryModality | null>(null);
const categoryId = ref<string>("");

const sexesOptions = ref<Sex[]>([]);
const modalityOptions = ref<any[]>([]);
const rankGroups = ref<RankGroup[]>([]);
const ranks = ref<any[]>([]);

const competitors = ref<any[]>([]);
const selectedCompetitors = ref<any[]>([]);
const loadingCompetitors = ref(false);

const form = ref({
  modalityId: "",
  sexIds: [] as string[],
  rankGroupId: "",
  physicalRequirement: {
    initialWeight: null as number | null,
    finalWeight: null as number | null,
    initialHeight: 0,
    finalHeight: 200,
  }
});

const loading = ref(false);
const errorMsg = ref('');

onMounted(async () => {
  try {
    rankGroups.value = await RankGroupService.getAll();
  } catch (err) {
    errorMsg.value = "Error al cargar los grupos de rangos.";
  }

  if (dialogRef?.value?.data) {
    modality.value = dialogRef.value.data.modality;
    categoryId.value = dialogRef.value.data.categoryId;

    const rawSexes = dialogRef.value.data.sexes;
    sexesOptions.value = rawSexes?.value ?? rawSexes ?? [];

    const rawModalities = dialogRef.value.data.modalities;
    modalityOptions.value = rawModalities?.value ?? rawModalities ?? [];

    const rawRanks = dialogRef.value.data.ranks;
    ranks.value = rawRanks?.value ?? rawRanks ?? [];

    if (modality.value) {
      form.value.modalityId = modality.value.modality.id;
      form.value.sexIds = modality.value.sexes.map(s => s.id);
      form.value.rankGroupId = modality.value.rankGroup?.id || "";
      form.value.physicalRequirement = {
        initialWeight: modality.value.physicalRequirement?.initialWeight ?? null,
        finalWeight: modality.value.physicalRequirement?.finalWeight ?? null,
        initialHeight: 0,
        finalHeight: 200,
      };

      loadingCompetitors.value = true;
      try {
        const data = await CategoryService.getCompetitors(modality.value.id);
        competitors.value = data.map(c => ({
          ...c,
          newWeight: c.weight,
          newAge: c.age,
          newRankId: c.rank.id
        }));
      } catch (err) {
        console.error("Error cargando atletas", err);
      } finally {
        loadingCompetitors.value = false;
      }
    }
  }
});

async function handleSave() {
  if (!form.value.modalityId) {
    errorMsg.value = 'Debe seleccionar una modalidad base.';
    return;
  }
  if (!form.value.sexIds || form.value.sexIds.length === 0) {
    errorMsg.value = 'Debe seleccionar al menos un sexo.';
    return;
  }
  if (!form.value.rankGroupId) {
    errorMsg.value = 'Debe seleccionar un grupo de rangos.';
    return;
  }

  loading.value = true;
  errorMsg.value = '';

  const payload = {
    modalityId: form.value.modalityId,
    sexIds: form.value.sexIds,
    rankGroupIds: [form.value.rankGroupId],
    physicalRequirements: [{
      ...form.value.physicalRequirement,
      initialHeight: 0,
      finalHeight: 200,
    }],
    sourceCategoryModalityId: modality.value?.id,
    competitorsToMigrate: selectedCompetitors.value.map(c => ({
      registrationId: c.registrationId,
      competitorId: c.id,
      newWeight: c.newWeight,
      newAge: c.newAge,
      newRankId: c.newRankId
    }))
  };

  try {
    await CategoryService.appendModality(categoryId.value, payload);
    dialogRef.value.close(true);
  } catch (err: any) {
    errorMsg.value = err.response?.data?.detail || 'Error al clonar la subcategoría';
  } finally {
    loading.value = false;
  }
}

function cancel() {
  dialogRef.value.close();
}
</script>

<template>
  <div class="flex flex-col gap-6 p-1">
    <Message v-if="errorMsg" severity="error" closable @close="errorMsg = ''">{{ errorMsg }}</Message>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <!-- Modalidad Base -->
      <div class="flex flex-col gap-2">
        <label class="font-bold text-surface-700 dark:text-surface-0/80">Modalidad</label>
        <Dropdown v-model="form.modalityId" :options="modalityOptions" optionLabel="name" optionValue="id"
          placeholder="Seleccionar Modalidad" class="w-full" />
      </div>

      <!-- Sexos -->
      <div class="flex flex-col gap-2">
        <label class="font-bold text-surface-700 dark:text-surface-0/80">Géneros Permitidos</label>
        <MultiSelect v-model="form.sexIds" :options="sexesOptions" optionLabel="name" optionValue="id"
          placeholder="Seleccionar Sexos" class="w-full" display="chip" />
      </div>
    </div>

    <div class="grid grid-cols-1 gap-4">
      <!-- Grupo de Rangos -->
      <div class="flex flex-col gap-2">
        <label class="font-bold text-surface-700 dark:text-surface-0/80">Grupo de Rangos</label>
        <Dropdown v-model="form.rankGroupId" :options="rankGroups" optionLabel="name" optionValue="id"
          placeholder="Seleccionar Grupo de Rangos" class="w-full" />
      </div>
    </div>

    <!-- Requerimientos de Peso -->
    <div class="flex flex-col gap-4 border-t-1 border-surface-200 pt-4 mt-2">
      <h3 class="text-lg font-bold m-0 text-surface-700 dark:text-surface-0/80">Rango de Peso</h3>
      <div class="grid grid-cols-2 gap-4">
        <div class="flex flex-col gap-2">
          <label class="font-semibold text-sm text-surface-600 dark:text-surface-400">Peso Inicial (kg)</label>
          <InputNumber v-model="form.physicalRequirement.initialWeight" :min="0" :maxFractionDigits="2"
            placeholder="Ej: 45.5" class="w-full" />
        </div>
        <div class="flex flex-col gap-2">
          <label class="font-semibold text-sm text-surface-600 dark:text-surface-400">Peso Final (kg)</label>
          <InputNumber v-model="form.physicalRequirement.finalWeight" :min="0" :maxFractionDigits="2"
            placeholder="Ej: 50.0" class="w-full" />
        </div>
      </div>
    </div>

    <!-- Migración de Competidores -->
    <div v-if="competitors.length > 0" class="flex flex-col gap-4 border-t-1 border-surface-200 pt-4 mt-2">
      <h3 class="text-lg font-bold m-0 text-surface-700 dark:text-surface-0/80">Migrar Atletas</h3>
      <p class="text-sm text-surface-500">Seleccione los atletas que desea mover a esta nueva subcategoría y edite sus datos si es necesario.</p>
      
      <DataTable :value="competitors" v-model:selection="selectedCompetitors" dataKey="id" :loading="loadingCompetitors" class="p-datatable-sm" scrollable scrollHeight="200px">
        <Column selectionMode="multiple" headerStyle="width: 3rem"></Column>
        <Column field="firstName" header="Atleta" style="min-width: 150px">
          <template #body="{ data }">
            <span class="font-semibold">{{ data.firstName }} {{ data.lastName }}</span>
          </template>
        </Column>
        <Column header="Peso (kg)" style="min-width: 100px">
          <template #body="{ data }">
            <InputNumber v-model="data.newWeight" :minFractionDigits="1" class="w-full max-w-[5rem]" inputClass="p-inputtext-sm" />
          </template>
        </Column>
        <Column header="Edad" style="min-width: 80px">
          <template #body="{ data }">
            <InputNumber v-model="data.newAge" :min="0" class="w-full max-w-[4rem]" inputClass="p-inputtext-sm" />
          </template>
        </Column>
        <Column header="Rango" style="min-width: 150px">
          <template #body="{ data }">
            <Dropdown v-model="data.newRankId" :options="ranks" optionLabel="name" optionValue="id" class="w-full p-inputtext-sm" appendTo="body" />
          </template>
        </Column>
      </DataTable>
    </div>

    <div class="flex justify-end gap-2 mt-4 border-t-1 border-surface-200 pt-4">
      <Button label="Cancelar" icon="pi pi-times" text @click="cancel" />
      <Button label="Guardar" icon="pi pi-check" :loading="loading" @click="handleSave" />
    </div>
  </div>
</template>
