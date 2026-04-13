<script setup lang="ts">
import { ref, inject, computed } from "vue";
import { useToast } from "primevue/usetoast";
import { CompetitorService } from "../../services/CompetitorService";
import type { CompetitorCreate, Competitor } from "../../types";

const dialogRef = inject<any>("dialogRef");
const toast = useToast();

const academyOptions = computed(() => dialogRef?.value?.data?.academies?.value ?? dialogRef?.value?.data?.academies ?? []);
const rankOptions = computed(() => dialogRef?.value?.data?.ranks?.value ?? dialogRef?.value?.data?.ranks ?? []);
const sexOptions = computed(() => dialogRef?.value?.data?.sexes?.value ?? dialogRef?.value?.data?.sexes ?? []);
const existingCompetitor = dialogRef?.value?.data?.competitor as Competitor | undefined;

const form = ref<CompetitorCreate>({
  firstName: existingCompetitor?.firstName ?? "",
  lastName: existingCompetitor?.lastName ?? "",
  academyId: existingCompetitor?.academy?.id ?? "",
  rankId: existingCompetitor?.rank?.id ?? "",
  sexId: existingCompetitor?.sex?.id ?? "",
  weight: existingCompetitor?.weight ?? null,
  height: existingCompetitor?.height ?? null,
  age: existingCompetitor?.age ?? null,
  specialCondition: existingCompetitor?.specialCondition ?? false,
});

const submitting = ref(false);

async function onSubmit(): Promise<void> {
  submitting.value = true;
  try {
    await CompetitorService.create(form.value);
    toast.add({ severity: "success", summary: "Éxito", detail: "Competidor guardado.", life: 3000 });
    dialogRef?.value?.close();
  } catch {
    toast.add({ severity: "error", summary: "Error", detail: "No se pudo guardar.", life: 5000 });
  } finally {
    submitting.value = false;
  }
}
</script>

<template>
  <form class="flex flex-col gap-4 p-2" @submit.prevent="onSubmit">
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
      <div class="flex flex-col gap-2">
        <label for="comp-first" class="font-semibold">Nombre</label>
        <InputText id="comp-first" v-model="form.firstName" required class="w-full" />
      </div>
      <div class="flex flex-col gap-2">
        <label for="comp-last" class="font-semibold">Apellido</label>
        <InputText id="comp-last" v-model="form.lastName" required class="w-full" />
      </div>
    </div>

    <div class="flex flex-col gap-2">
      <label for="comp-academy" class="font-semibold">Academia</label>
      <Select
        id="comp-academy"
        v-model="form.academyId"
        :options="academyOptions"
        optionLabel="name"
        optionValue="id"
        placeholder="Seleccionar academia"
        class="w-full"
      />
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
      <div class="flex flex-col gap-2">
        <label for="comp-rank" class="font-semibold">Rango</label>
        <Select
          id="comp-rank"
          v-model="form.rankId"
          :options="rankOptions"
          optionLabel="name"
          optionValue="id"
          placeholder="Seleccionar rango"
          class="w-full"
        />
      </div>
      <div class="flex flex-col gap-2">
        <label for="comp-sex" class="font-semibold">Sexo</label>
        <Select
          id="comp-sex"
          v-model="form.sexId"
          :options="sexOptions"
          optionLabel="name"
          optionValue="id"
          placeholder="Seleccionar sexo"
          class="w-full"
        />
      </div>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
      <div class="flex flex-col gap-2">
        <label for="comp-weight" class="font-semibold">Peso (Kg)</label>
        <InputNumber id="comp-weight" v-model="form.weight" :minFractionDigits="1" class="w-full" />
      </div>
      <div class="flex flex-col gap-2">
        <label for="comp-height" class="font-semibold">Altura (cm)</label>
        <InputNumber id="comp-height" v-model="form.height" :minFractionDigits="1" class="w-full" />
      </div>
      <div class="flex flex-col gap-2">
        <label for="comp-age" class="font-semibold">Edad</label>
        <InputNumber id="comp-age" v-model="form.age" class="w-full" />
      </div>
    </div>

    <div class="flex items-center gap-2">
      <Checkbox id="comp-special" v-model="form.specialCondition" :binary="true" />
      <label for="comp-special">Condición Especial</label>
    </div>

    <Button type="submit" label="Guardar" icon="pi pi-check" :loading="submitting" />
  </form>
</template>
