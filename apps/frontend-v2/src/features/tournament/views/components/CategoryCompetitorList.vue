<script setup lang="ts">
import { inject, onMounted, ref } from "vue";
import type { CategoryModality } from "../../types";
import type { Competitor } from "@/features/registration/types";
import { CategoryService } from "../../services/CategoryService";
import { BracketService } from "../../../bracket/services/BracketService";
import { useConfirm } from "primevue/useconfirm";
import { useToast } from "primevue/usetoast";
import DataTable from "primevue/datatable";
import Column from "primevue/column";
import Avatar from "primevue/avatar";
import Tag from "primevue/tag";
import Button from "primevue/button";
import Divider from "primevue/divider";
import ConfirmDialog from "primevue/confirmdialog";

const toast = useToast();
const confirm = useConfirm();

const dialogRef = inject<any>("dialogRef");
const categoryModality = dialogRef?.value?.data?.categoryModality as any | undefined;
const competitors = ref<Competitor[]>([]);
const loading = ref(true);

const refreshCompetitors = async () => {
  if (!categoryModality?.id) return;
  loading.value = true;
  try {
    competitors.value = await CategoryService.getCompetitors(categoryModality.id);
  } catch (error) {
    console.error("Error fetching competitors:", error);
  } finally {
    loading.value = false;
  }
};

onMounted(refreshCompetitors);

const isDeleting = ref(false);
const pendingDeletePayload = ref<{ registrationId: string; categoryModalityId: string } | null>(null);

function handleDeleteCompetitor(competitor: Competitor) {
  if (!competitor.registrationId) {
    toast.add({ severity: "error", summary: "Error", detail: "No se encontró el ID de inscripción.", life: 3000 });
    return;
  }

  pendingDeletePayload.value = {
    registrationId: competitor.registrationId,
    categoryModalityId: categoryModality.id
  };

  confirm.require({
    group: 'competitorDeleteList',
    header: 'Confirmar eliminación',
    message: `¿Cómo deseas eliminar a ${competitor.firstName} ${competitor.lastName}?`,
    icon: 'pi pi-user-minus',
  });
}

async function handleConfirmDelete(removeFromCategory: boolean) {
  if (!pendingDeletePayload.value) return;
  const payload = pendingDeletePayload.value;
  confirm.close();

  isDeleting.value = true;
  try {
    await BracketService.removeCompetitor(payload.categoryModalityId, payload.registrationId, removeFromCategory);
    toast.add({
      severity: "success",
      summary: removeFromCategory ? "Eliminado de categoría" : "Quitado de pirámide",
      detail: "La lista de competidores ha sido actualizada.",
      life: 3000
    });
    await refreshCompetitors();
  } catch (error) {
    toast.add({ severity: "error", summary: "Error", detail: "No se pudo realizar la operación.", life: 3000 });
  } finally {
    isDeleting.value = false;
    pendingDeletePayload.value = null;
  }
}
</script>

<template>
  <div class="flex flex-col gap-4 p-2">
    <div v-if="categoryModality" class="flex gap-2 items-center flex-wrap">
      <Tag :value="categoryModality.modality.name" severity="secondary" />
      <span class="text-sm font-medium text-surface-600 dark:text-surface-400">
        {{ Math.min(...categoryModality.ages) }} – {{ Math.max(...categoryModality.ages) }} años
      </span>
      <Divider layout="vertical" class="hidden sm:block" />
      <div class="flex gap-1">
        <Tag v-for="rank in categoryModality.ranks" :key="rank.id" :value="rank.name" severity="info"
          pt:root:class="!text-[10px] !px-2" />
      </div>
    </div>

    <DataTable :value="competitors" :rows="10" paginator :loading="loading" class="p-datatable-sm">
      <template #empty>
        <div class="flex flex-col items-center justify-center py-10 gap-3">
          <i class="pi pi-users text-4xl text-surface-300 dark:text-surface-600" />
          <p class="text-surface-500 font-medium">No hay competidores registrados en esta categoría.</p>
        </div>
      </template>

      <Column header="Competidor" class="font-semibold">
        <template #body="{ data }">
          <div class="flex items-center gap-2">
            <Avatar :label="data.firstName[0] + data.lastName[0]" shape="circle" class="bg-primary text-white text-xs"
              style="width: 2rem; height: 2rem" />
            <div class="flex flex-col">
              <span>{{ data.firstName }} {{ data.lastName }}</span>
              <small class="text-surface-500">{{ data.sex.name }}</small>
            </div>
          </div>
        </template>
      </Column>
      <Column header="Academia">
        <template #body="{ data }">
          <div class="flex flex-col">
            <span class="text-sm">{{ data.academy.name }}</span>
            <small class="text-xs text-surface-500">Prof: {{ data.academy.instructor.firstName }}</small>
          </div>
        </template>
      </Column>
      <Column :exportable="false" style="min-width: 4rem" header="Acciones">
        <template #body="{ data }">
          <Button icon="pi pi-trash" severity="danger" text rounded @click="handleDeleteCompetitor(data)"
            title="Eliminar de la categoría" :disabled="isDeleting" />
        </template>
      </Column>
    </DataTable>

    <ConfirmDialog group="competitorDeleteList">
      <template #container="{ message }">
        <div
          class="flex flex-col items-center p-6 bg-surface-0 dark:bg-surface-900 rounded-lg shadow-lg border border-surface-200 dark:border-surface-700 max-w-md">
          <div class="rounded-full bg-primary-100 dark:bg-primary-900/30 p-4 mb-4">
            <i :class="message.icon" class="text-3xl text-primary-600"></i>
          </div>
          <span class="font-bold text-xl mb-2">{{ message.header }}</span>
          <p class="text-surface-600 dark:text-surface-400 text-center mb-6">{{ message.message }}</p>
          <div class="flex flex-wrap justify-center gap-2 w-full">
            <Button label="Cancelar" severity="secondary" outlined @click="confirm.close()" class="flex-1 min-w-[100px]" />
            <Button label="Solo Pirámide" severity="warn" icon="pi pi-minus-circle" @click="handleConfirmDelete(false)"
              class="flex-1 min-w-[150px]" />
            <Button label="De Categoría" severity="danger" icon="pi pi-trash" @click="handleConfirmDelete(true)"
              class="flex-1 min-w-[150px]" />
          </div>
        </div>
      </template>
    </ConfirmDialog>
  </div>
</template>
