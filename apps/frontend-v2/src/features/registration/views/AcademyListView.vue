<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useDialog } from "primevue/usedialog";
import { AcademyService } from "../services/AcademyService";
import type { Academy } from "../types";
import AcademyForm from "./components/AcademyForm.vue";
import { FilterMatchMode } from "@primevue/core/api";

const dialog = useDialog();

const academies = ref<Academy[]>([]);
const loading = ref(true);

const filters = ref({
  global: { value: null, matchMode: FilterMatchMode.CONTAINS },
  name: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
});

async function loadAcademies(): Promise<void> {
  loading.value = true;
  try {
    academies.value = await AcademyService.getAll();
  } finally {
    loading.value = false;
  }
}

function openCreateDialog(): void {
  dialog.open(AcademyForm, {
    props: {
      header: "Crear Academia",
      style: { width: "25vw" },
      breakpoints: { "960px": "50vw", "640px": "90vw" },
      modal: true,
      dismissableMask: true,
    },
    onClose: () => loadAcademies(),
  });
}

function openEditDialog(academy: Academy): void {
  dialog.open(AcademyForm, {
    props: {
      header: "Editar Academia",
      style: { width: "25vw" },
      breakpoints: { "960px": "50vw", "640px": "90vw" },
      modal: true,
      dismissableMask: true,
    },
    data: { academy },
    onClose: () => loadAcademies(),
  });
}

onMounted(loadAcademies);
</script>

<template>
  <div class="card">
    <h2 class="text-2xl font-bold mb-4">Academias</h2>
    <DataTable
      v-model:filters="filters"
      :value="academies"
      :loading="loading"
      paginator
      :rows="10"
      filterDisplay="row"
      :globalFilterFields="['name']"
    >
      <template #header>
        <div class="flex justify-end">
          <Button icon="pi pi-plus" label="Nueva Academia" @click="openCreateDialog" />
        </div>
      </template>

      <Column field="name" header="Nombre" :sortable="true">
        <template #filter="{ filterModel, filterCallback }">
          <InputText
            v-model="filterModel.value"
            type="text"
            placeholder="Buscar por nombre"
            @input="filterCallback()"
          />
        </template>
      </Column>

      <Column header="Instructor">
        <template #body="{ data }">
          {{ data.instructor.firstName }} {{ data.instructor.lastName }}
        </template>
      </Column>

      <Column header="Acciones" style="width: 5rem">
        <template #body="{ data }">
          <Button icon="pi pi-pencil" text rounded @click="openEditDialog(data)" />
        </template>
      </Column>
    </DataTable>
  </div>
</template>
