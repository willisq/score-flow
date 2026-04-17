<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useDialog } from "primevue/usedialog";
import { useConfirm } from "primevue/useconfirm";
import { useToast } from "primevue/usetoast";
import { RankGroupService } from "../services/RankGroupService";
import type { RankGroup } from "../types";
import RankGroupForm from "./components/RankGroupForm.vue";
import { FilterMatchMode } from "@primevue/core/api";

const dialog = useDialog();
const confirm = useConfirm();
const toast = useToast();

const groups = ref<RankGroup[]>([]);
const loading = ref(true);

const filters = ref({
  global: { value: null, matchMode: FilterMatchMode.CONTAINS },
  name: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
});

async function loadGroups(): Promise<void> {
  loading.value = true;
  try {
    groups.value = await RankGroupService.getAll();
  } catch (error) {
    toast.add({ severity: "error", summary: "Error", detail: "No se pudieron cargar los grupos de rangos", life: 3000 });
  } finally {
    loading.value = false;
  }
}

function openCreateDialog(): void {
  dialog.open(RankGroupForm, {
    props: {
      header: "Crear Grupo de Rangos",
      style: { width: "30vw" },
      breakpoints: { "960px": "50vw", "640px": "90vw" },
      modal: true,
      dismissableMask: true,
    },
    onClose: (opt) => {
      if (opt?.data) {
        loadGroups();
      }
    },
  });
}

function openEditDialog(group: RankGroup): void {
  dialog.open(RankGroupForm, {
    props: {
      header: "Editar Grupo de Rangos",
      style: { width: "30vw" },
      breakpoints: { "960px": "50vw", "640px": "90vw" },
      modal: true,
      dismissableMask: true,
    },
    data: { group },
    onClose: (opt) => {
      if (opt?.data) {
        loadGroups();
      }
    },
  });
}

function confirmDelete(event: Event, group: RankGroup): void {
  confirm.require({
    target: event.currentTarget as HTMLElement,
    message: `¿Estás seguro de que deseas eliminar el grupo "${group.name}"?`,
    header: "Confirmar eliminación",
    icon: "pi pi-exclamation-triangle",
    acceptClass: "p-button-danger",
    acceptLabel: "Sí",
    rejectLabel: "No",
    accept: async () => {
      try {
        await RankGroupService.delete(group.id);
        toast.add({ severity: "success", summary: "Confirmado", detail: "Grupo eliminado.", life: 3000 });
        loadGroups();
      } catch (error) {
        toast.add({ severity: "error", summary: "Error", detail: "No se pudo eliminar el grupo.", life: 3000 });
      }
    },
  });
}

onMounted(loadGroups);
</script>

<template>
  <div class="card">
    <h2 class="text-2xl font-bold mb-4">Mantenimiento de Grupos de Rangos</h2>
    <DataTable
      v-model:filters="filters"
      :value="groups"
      :loading="loading"
      paginator
      :rows="10"
      filterDisplay="row"
      :globalFilterFields="['name']"
    >
      <template #header>
        <div class="flex justify-end">
          <Button icon="pi pi-plus" label="Nuevo Grupo" @click="openCreateDialog" />
        </div>
      </template>

      <Column field="name" header="Nombre del Grupo" :sortable="true" style="width: 30%">
        <template #filter="{ filterModel, filterCallback }">
          <InputText
            v-model="filterModel.value"
            type="text"
            placeholder="Buscar por nombre"
            @input="filterCallback()"
          />
        </template>
      </Column>

      <Column header="Rangos Incluidos" style="width: 50%">
        <template #body="{ data }">
          <div class="flex flex-wrap gap-1">
            <Tag v-for="rank in data.ranks" :key="rank.id" :value="rank.name" severity="secondary" rounded />
          </div>
        </template>
      </Column>

      <Column header="Acciones" style="width: 20%; min-width: 8rem">
        <template #body="{ data }">
          <div class="flex gap-2">
            <Button icon="pi pi-pencil" class="p-button-rounded p-button-text" @click="openEditDialog(data)" />
            <Button icon="pi pi-trash" severity="danger" class="p-button-rounded p-button-text" @click="confirmDelete($event, data)" />
          </div>
        </template>
      </Column>
    </DataTable>
  </div>
</template>
