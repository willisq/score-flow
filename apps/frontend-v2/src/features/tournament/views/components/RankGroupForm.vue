<script setup lang="ts">
import { ref, inject, onMounted } from "vue";
import { useToast } from "primevue/usetoast";
import { RankGroupService } from "../../services/RankGroupService";
import { RankService } from "@/features/registration/services/RankService";
import type { RankGroup, RankGroupCreate } from "../../types";
import type { Rank } from "@/features/registration/types";

const dialogRef = inject<any>("dialogRef");
const toast = useToast();

const existingGroup = dialogRef?.value?.data?.group as RankGroup | undefined;
const isEditing = !!existingGroup;

const form = ref<RankGroupCreate>({
  name: existingGroup?.name ?? "",
  rankIds: existingGroup?.ranks.map((r) => r.id) ?? [],
});

const ranks = ref<Rank[]>([]);
const loadingRanks = ref(true);
const submitting = ref(false);

onMounted(async () => {
  try {
    ranks.value = await RankService.getAll();
  } catch (e) {
    toast.add({ severity: "error", summary: "Error", detail: "No se pudieron cargar los rangos.", life: 3000 });
  } finally {
    loadingRanks.value = false;
  }
});

async function onSubmit(): Promise<void> {
  submitting.value = true;
  try {
    if (isEditing) {
      await RankGroupService.update(existingGroup!.id, form.value);
      toast.add({ severity: "success", summary: "Éxito", detail: "Grupo actualizado.", life: 3000 });
    } else {
      await RankGroupService.create(form.value);
      toast.add({ severity: "success", summary: "Éxito", detail: "Grupo creado.", life: 3000 });
    }
    dialogRef?.value?.close(true);
  } catch {
    toast.add({ severity: "error", summary: "Error", detail: "No se pudo guardar el grupo.", life: 5000 });
  } finally {
    submitting.value = false;
  }
}
</script>

<template>
  <form class="flex flex-col gap-4 p-2" @submit.prevent="onSubmit">
    <div class="flex flex-col gap-2">
      <label for="group-name" class="font-semibold">Nombre del Grupo</label>
      <InputText id="group-name" v-model="form.name" placeholder="Ej: Principiantes" required />
    </div>

    <div class="flex flex-col gap-2">
      <label for="group-ranks" class="font-semibold">Rangos ({{ form.rankIds.length }} seleccionados)</label>
      <MultiSelect id="group-ranks" v-model="form.rankIds" :options="ranks" optionLabel="name" optionValue="id"
        placeholder="Selecciona uno o más rangos" display="chip" :loading="loadingRanks" :maxSelectedLabels="3" filter
        required />
    </div>

    <div class="flex justify-end gap-2 mt-2">
      <Button type="button" label="Cancelar" icon="pi pi-times" severity="secondary"
        @click="dialogRef?.value?.close()" />
      <Button type="submit" :label="isEditing ? 'Actualizar' : 'Guardar'" icon="pi pi-check" :loading="submitting" />
    </div>
  </form>
</template>
