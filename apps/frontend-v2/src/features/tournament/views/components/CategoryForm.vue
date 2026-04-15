<script setup lang="ts">
import { ref, inject, computed } from "vue";
import { useToast } from "primevue/usetoast";
import { CategoryService } from "../../services/CategoryService";
import type { CategoryCreate } from "../../types";

const dialogRef = inject<any>("dialogRef");
const toast = useToast();

const modalityOptions = computed(() => dialogRef?.value?.data?.modalities?.value ?? dialogRef?.value?.data?.modalities ?? []);
const rankOptions = computed(() => dialogRef?.value?.data?.ranks?.value ?? dialogRef?.value?.data?.ranks ?? []);
const sexOptions = computed(() => dialogRef?.value?.data?.sexes?.value ?? dialogRef?.value?.data?.sexes ?? []);

const form = ref<CategoryCreate>({
  ages: [],
  specialCondition: false,
  modalityIds: [],
  rankIds: [],
  sexIds: [],
  initialWeight: null,
  finalWeight: null,
  initialHeight: null,
  finalHeight: null,
});

const submitting = ref(false);
const ageInput = ref<string>("");

function addAge(): void {
  const age = Number.parseInt(ageInput.value, 10);
  if (!Number.isNaN(age) && !form.value.ages.includes(age)) {
    form.value.ages.push(age);
    form.value.ages.sort((a, b) => a - b);
  }
  ageInput.value = "";
}

function removeAge(age: number): void {
  form.value.ages = form.value.ages.filter((a) => a !== age);
}

async function onSubmit(): Promise<void> {
  submitting.value = true;
  try {
    await CategoryService.create(form.value);
    toast.add({ severity: "success", summary: "Éxito", detail: "Categoría creada.", life: 3000 });
    dialogRef?.value?.close();
  } catch {
    toast.add({ severity: "error", summary: "Error", detail: "No se pudo crear la categoría.", life: 5000 });
  } finally {
    submitting.value = false;
  }
}
</script>

<template>
  <form class="flex flex-col gap-4 p-2" @submit.prevent="onSubmit">
    <div class="flex flex-col gap-2">
      <label class="font-semibold">Modalidad</label>
      <MultiSelect
        v-model="form.modalityIds"
        :options="modalityOptions"
        optionLabel="name"
        optionValue="id"
        placeholder="Seleccionar modalidades"
      />
    </div>

    <div class="flex flex-col gap-2">
      <label class="font-semibold">Edades</label>
      <div class="flex gap-2">
        <InputText v-model="ageInput" placeholder="Agregar edad" @keyup.enter="addAge" />
        <Button icon="pi pi-plus" @click="addAge" type="button" />
      </div>
      <div class="flex gap-1 flex-wrap">
        <Chip v-for="age in form.ages" :key="age" :label="String(age)" removable @remove="removeAge(age)" />
      </div>
    </div>

    <div class="grid grid-cols-2 gap-4">
      <div class="flex flex-col gap-2">
        <label class="font-semibold">Rangos</label>
        <MultiSelect
          v-model="form.rankIds"
          :options="rankOptions"
          optionLabel="name"
          optionValue="id"
          placeholder="Seleccionar rangos"
        />
      </div>
      <div class="flex flex-col gap-2">
        <label class="font-semibold">Sexos</label>
        <MultiSelect
          v-model="form.sexIds"
          :options="sexOptions"
          optionLabel="name"
          optionValue="id"
          placeholder="Seleccionar sexos"
        />
      </div>
    </div>

    <div class="grid grid-cols-2 gap-4">
      <div class="flex flex-col gap-2">
        <label class="font-semibold">Peso Inicial (Kg)</label>
        <InputNumber v-model="form.initialWeight" :minFractionDigits="1" />
      </div>
      <div class="flex flex-col gap-2">
        <label class="font-semibold">Peso Final (Kg)</label>
        <InputNumber v-model="form.finalWeight" :minFractionDigits="1" />
      </div>
    </div>

    <div class="grid grid-cols-2 gap-4">
      <div class="flex flex-col gap-2">
        <label class="font-semibold">Altura Inicial (cm)</label>
        <InputNumber v-model="form.initialHeight" :minFractionDigits="1" />
      </div>
      <div class="flex flex-col gap-2">
        <label class="font-semibold">Altura Final (cm)</label>
        <InputNumber v-model="form.finalHeight" :minFractionDigits="1" />
      </div>
    </div>

    <div class="flex items-center gap-2">
      <Checkbox v-model="form.specialCondition" :binary="true" />
      <label>Condición Especial</label>
    </div>

    <Button type="submit" label="Crear Categoría" icon="pi pi-check" :loading="submitting" />
  </form>
</template>
