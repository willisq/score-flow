<script setup lang="ts">
import { ref, inject } from "vue";
import { useToast } from "primevue/usetoast";
import { TournamentService } from "../../services/TournamentService";
import type { TournamentCreate } from "../../types";

const dialogRef = inject<any>("dialogRef");
const toast = useToast();

const form = ref<TournamentCreate>({ description: "" });
const submitting = ref(false);

async function onSubmit(): Promise<void> {
  submitting.value = true;
  try {
    await TournamentService.create(form.value);
    toast.add({ severity: "success", summary: "Éxito", detail: "Torneo creado.", life: 3000 });
    dialogRef?.value?.close();
  } catch {
    toast.add({ severity: "error", summary: "Error", detail: "No se pudo crear el torneo.", life: 5000 });
  } finally {
    submitting.value = false;
  }
}
</script>

<template>
  <form class="flex flex-col gap-4 p-2" @submit.prevent="onSubmit">
    <div class="flex flex-col gap-2">
      <label for="tournament-desc" class="font-semibold">Descripción</label>
      <InputText id="tournament-desc" v-model="form.description" placeholder="Ej: Campeonato Nacional 2026" required />
    </div>
    <Button type="submit" label="Crear" icon="pi pi-check" :loading="submitting" />
  </form>
</template>
