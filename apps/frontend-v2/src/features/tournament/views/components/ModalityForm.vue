<script setup lang="ts">
import { ref, inject, onMounted } from 'vue';
import InputNumber from 'primevue/inputnumber';
import MultiSelect from 'primevue/multiselect';
import Button from 'primevue/button';
import Message from 'primevue/message';
import { CategoryService } from '../../services/CategoryService';
import type { CategoryModality, CategoryModalityUpdate } from '../../types';
import type { Sex } from '@/features/registration/types';

const dialogRef = inject<any>("dialogRef");

const modality = ref<CategoryModality | null>(null);
const sexesOptions = ref<Sex[]>([]);
const form = ref<CategoryModalityUpdate>({
  sexIds: [],
  physicalRequirement: {
    initialWeight: null,
    finalWeight: null,
    initialHeight: 0,
    finalHeight: 200,
  }
});

onMounted(() => {
  if (dialogRef?.value?.data) {
    modality.value = dialogRef.value.data.modality;
    const rawSexes = dialogRef.value.data.sexes;
    sexesOptions.value = rawSexes?.value ?? rawSexes ?? [];

    if (modality.value) {
      form.value.sexIds = modality.value.sexes.map(s => s.id);
      form.value.physicalRequirement = {
        initialWeight: modality.value.physicalRequirement?.initialWeight ?? null,
        finalWeight: modality.value.physicalRequirement?.finalWeight ?? null,
        initialHeight: 0,
        finalHeight: 200,
      };
    }
  }
});

const loading = ref(false);
const errorMsg = ref('');

async function handleSave() {
  if (!modality.value || !form.value.sexIds || form.value.sexIds.length === 0) {
    errorMsg.value = 'Debe seleccionar al menos un sexo.';
    return;
  }

  loading.value = true;
  errorMsg.value = '';
  try {
    await CategoryService.updateModality(modality.value.id, {
      ...form.value,
      physicalRequirement: {
        ...form.value.physicalRequirement!,
        initialHeight: 0,
        finalHeight: 200,
      }
    });
    dialogRef.value.close(true);
  } catch (err: any) {
    errorMsg.value = err.response?.data?.detail || 'Error al actualizar la subcategoría';
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

    <!-- Sección de Sexos -->
    <div class="flex flex-col gap-2">
      <label class="font-bold text-surface-700 dark:text-surface-0/80">Géneros Permitidos</label>
      <MultiSelect v-model="form.sexIds" :options="sexesOptions" optionLabel="name" optionValue="id"
        placeholder="Seleccionar Sexos" class="w-full" display="chip" />
    </div>

    <!-- Requerimientos de Peso -->
    <div class="flex flex-col gap-4">
      <div class="flex flex-col gap-2">
        <label class="font-bold text-surface-700 dark:text-surface-0/80">Peso Inicial (kg)</label>
        <InputNumber v-model="form.physicalRequirement!.initialWeight" :min="0" :maxFractionDigits="2"
          placeholder="Ej: 45.5" class="" />
      </div>
      <div class="flex flex-col gap-2">
        <label class="font-bold text-surface-700 dark:text-surface-0/80">Peso Final (kg)</label>
        <InputNumber v-model="form.physicalRequirement!.finalWeight" :min="0" :maxFractionDigits="2"
          placeholder="Ej: 50.0" class="w-full" />
      </div>
    </div>

    <!-- Requerimientos de Altura eliminados por lógica de negocio -->

    <div class="flex justify-end gap-2 mt-4">
      <Button label="Cancelar" icon="pi pi-times" text @click="cancel" />
      <Button label="Guardar Cambios" icon="pi pi-check" :loading="loading" @click="handleSave" />
    </div>
  </div>
</template>
