<script setup lang="ts">
import { ref, inject, onMounted, computed } from 'vue';
import InputNumber from 'primevue/inputnumber';
import MultiSelect from 'primevue/multiselect';
import Dropdown from 'primevue/dropdown';
import Button from 'primevue/button';
import Message from 'primevue/message';
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
    }]
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

    <div class="flex justify-end gap-2 mt-4">
      <Button label="Cancelar" icon="pi pi-times" text @click="cancel" />
      <Button label="Guardar" icon="pi pi-check" :loading="loading" @click="handleSave" />
    </div>
  </div>
</template>
