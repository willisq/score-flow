<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useDialog } from "primevue/usedialog";
import { CompetitorService } from "../services/CompetitorService";
import { useRegistrationData } from "../composables/useRegistrationData";
import type { Competitor } from "../types";
import CompetitorForm from "./components/CompetitorForm.vue";
import CompetitorUploadDialog from "./components/CompetitorUploadDialog.vue";

const dialog = useDialog();
const { academies, ranks, sexes } = useRegistrationData();

const competitors = ref<Competitor[]>([]);
const loading = ref(true);

async function loadCompetitors(): Promise<void> {
  loading.value = true;
  try {
    competitors.value = await CompetitorService.getAll();
  } finally {
    loading.value = false;
  }
}

function openCreateDialog(): void {
  dialog.open(CompetitorForm, {
    props: {
      header: "Crear Competidor",
      style: { width: "30vw" },
      breakpoints: { "960px": "60vw", "640px": "90vw" },
      modal: true,
      dismissableMask: true,
    },
    data: { academies, ranks, sexes },
    onClose: () => loadCompetitors(),
  });
}

function openEditDialog(competitor: Competitor): void {
  dialog.open(CompetitorForm, {
    props: {
      header: "Editar Competidor",
      style: { width: "30vw" },
      breakpoints: { "960px": "60vw", "640px": "90vw" },
      modal: true,
      dismissableMask: true,
    },
    data: { academies, ranks, sexes, competitor },
    onClose: () => loadCompetitors(),
  });
}

function openUploadDialog(): void {
  dialog.open(CompetitorUploadDialog, {
    props: {
      header: "Registro Masivo (Excel)",
      style: { width: "30vw" },
      breakpoints: { "960px": "60vw", "640px": "90vw" },
      modal: true,
      dismissableMask: true,
    },
    onClose: () => loadCompetitors(),
  });
}

onMounted(loadCompetitors);
</script>

<template>
  <div class="card">
    <h2 class="text-2xl font-bold mb-4">Competidores</h2>
    <DataTable :value="competitors" :loading="loading" paginator :rows="10">
      <template #header>
        <div class="flex justify-end gap-2">
          <Button icon="pi pi-upload" label="Carga Masiva" severity="secondary" @click="openUploadDialog" />
          <Button icon="pi pi-plus" label="Crear Competidor" @click="openCreateDialog" />
        </div>
      </template>

      <Column header="Nombre">
        <template #body="{ data }">
          {{ data.firstName }} {{ data.lastName }}
        </template>
      </Column>

      <Column field="academy.name" header="Academia" :sortable="true" />

      <Column field="rank.name" header="Rango" :sortable="true" />

      <Column header="Sexo">
        <template #body="{ data }">
          <i
            :class="[
              'pi',
              data.sex.name === 'Masculino' || data.sex.name === 'Hombre'
                ? 'pi-mars text-blue-500'
                : 'pi-venus text-pink-500',
            ]"
          ></i>
        </template>
      </Column>

      <Column field="weight" header="Peso">
        <template #body="{ data }">
          {{ data.weight ? `${data.weight} Kg` : "—" }}
        </template>
      </Column>

      <Column field="height" header="Altura">
        <template #body="{ data }">
          {{ data.height ? `${data.height} cm` : "—" }}
        </template>
      </Column>

      <Column field="age" header="Edad">
        <template #body="{ data }">
          {{ data.age ? `${data.age} años` : "—" }}
        </template>
      </Column>

      <Column header="Cond. Especial">
        <template #body="{ data }">
          <Tag v-if="data.specialCondition" value="Sí" severity="info" />
          <span v-else>No</span>
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
