<script setup lang="ts">
import { ref, inject } from "vue";
import { useToast } from "primevue/usetoast";
import { AcademyService } from "../../services/AcademyService";
import type { AcademyCreate, Academy } from "../../types";

const dialogRef = inject<any>("dialogRef");
const toast = useToast();

const existingAcademy = dialogRef?.value?.data?.academy as Academy | undefined;

const form = ref<AcademyCreate>({
  name: existingAcademy?.name ?? "",
  instructor: {
    firstName: existingAcademy?.instructor?.firstName ?? "",
    lastName: existingAcademy?.instructor?.lastName ?? "",
  },
});

const submitting = ref(false);

async function onSubmit(): Promise<void> {
  submitting.value = true;
  try {
    await AcademyService.create(form.value);
    toast.add({ severity: "success", summary: "Éxito", detail: "Academia guardada.", life: 3000 });
    dialogRef?.value?.close();
  } catch {
    toast.add({ severity: "error", summary: "Error", detail: "No se pudo guardar la academia.", life: 5000 });
  } finally {
    submitting.value = false;
  }
}
</script>

<template>
  <form class="flex flex-col gap-4 p-2" @submit.prevent="onSubmit">
    <div class="flex flex-col gap-2">
      <label for="academy-name" class="font-semibold">Nombre de la Academia</label>
      <InputText id="academy-name" v-model="form.name" placeholder="Ej: Chois Do" required />
    </div>

    <div class="flex flex-col gap-2">
      <label for="instructor-first" class="font-semibold">Nombre del Instructor</label>
      <InputText id="instructor-first" v-model="form.instructor.firstName" placeholder="Nombre" required />
    </div>

    <div class="flex flex-col gap-2">
      <label for="instructor-last" class="font-semibold">Apellido del Instructor</label>
      <InputText id="instructor-last" v-model="form.instructor.lastName" placeholder="Apellido" required />
    </div>

    <Button type="submit" label="Guardar" icon="pi pi-check" :loading="submitting" />
  </form>
</template>
