<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useDialog } from "primevue/usedialog";
import { TournamentService } from "../services/TournamentService";
import type { Tournament } from "../types";
import TournamentForm from "./components/TournamentForm.vue";

const dialog = useDialog();
const tournaments = ref<Tournament[]>([]);
const loading = ref(true);

async function loadTournaments(): Promise<void> {
  loading.value = true;
  try {
    tournaments.value = await TournamentService.getAll();
  } finally {
    loading.value = false;
  }
}

function openCreateDialog(): void {
  dialog.open(TournamentForm, {
    props: {
      header: "Crear Torneo",
      style: { width: "25vw" },
      breakpoints: { "960px": "50vw", "640px": "90vw" },
      modal: true,
      dismissableMask: true,
    },
    onClose: () => loadTournaments(),
  });
}

onMounted(loadTournaments);
</script>

<template>
  <div class="card">
    <h2 class="text-2xl font-bold mb-4">Torneos</h2>
    <DataTable :value="tournaments" :loading="loading" paginator :rows="10">
      <template #header>
        <div class="flex justify-end">
          <Button icon="pi pi-plus" label="Nuevo Torneo" @click="openCreateDialog" />
        </div>
      </template>

      <Column field="description" header="Descripción" :sortable="true" />
    </DataTable>
  </div>
</template>
