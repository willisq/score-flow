<script setup lang="ts">
import { ref, onMounted } from "vue";
import { CompetitorService } from "@/features/registration/services/CompetitorService";
import { AcademyService } from "@/features/registration/services/AcademyService";
import { CategoryService } from "@/features/tournament/services/CategoryService";

const stats = ref({
  competitors: 0,
  academies: 0,
  categories: 0,
});
const loading = ref(true);

onMounted(async () => {
  try {
    const [competitors, academies, categories] = await Promise.all([
      CompetitorService.getAll(),
      AcademyService.getAll(),
      CategoryService.getAll(),
    ]);
    stats.value = {
      competitors: competitors.length,
      academies: academies.length,
      categories: categories.length,
    };
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <div class="grid">
    <div class="col-12">
      <h1 class="text-3xl font-bold mb-2">Dashboard</h1>
      <p class="text-surface-500 dark:text-surface-400 mb-6">
        Resumen general de la plataforma ScoreFlow.
      </p>
    </div>

    <div class="col-12 lg:col-4">
      <div class="card mb-0">
        <div class="flex justify-between mb-4">
          <div>
            <span class="block text-surface-500 dark:text-surface-400 font-medium mb-3">Competidores</span>
            <div class="text-surface-900 dark:text-surface-0 font-bold text-4xl">
              {{ loading ? "..." : stats.competitors }}
            </div>
          </div>
          <div
            class="flex items-center justify-center bg-blue-100 dark:bg-blue-400/10 rounded-full"
            style="width: 2.5rem; height: 2.5rem"
          >
            <i class="pi pi-id-card text-blue-500 text-xl"></i>
          </div>
        </div>
        <span class="text-sm text-surface-500 dark:text-surface-400">Registrados en el sistema</span>
      </div>
    </div>

    <div class="col-12 lg:col-4">
      <div class="card mb-0">
        <div class="flex justify-between mb-4">
          <div>
            <span class="block text-surface-500 dark:text-surface-400 font-medium mb-3">Academias</span>
            <div class="text-surface-900 dark:text-surface-0 font-bold text-4xl">
              {{ loading ? "..." : stats.academies }}
            </div>
          </div>
          <div
            class="flex items-center justify-center bg-orange-100 dark:bg-orange-400/10 rounded-full"
            style="width: 2.5rem; height: 2.5rem"
          >
            <i class="pi pi-building text-orange-500 text-xl"></i>
          </div>
        </div>
        <span class="text-sm text-surface-500 dark:text-surface-400">Escuelas registradas</span>
      </div>
    </div>

    <div class="col-12 lg:col-4">
      <div class="card mb-0">
        <div class="flex justify-between mb-4">
          <div>
            <span class="block text-surface-500 dark:text-surface-400 font-medium mb-3">Categorías</span>
            <div class="text-surface-900 dark:text-surface-0 font-bold text-4xl">
              {{ loading ? "..." : stats.categories }}
            </div>
          </div>
          <div
            class="flex items-center justify-center bg-cyan-100 dark:bg-cyan-400/10 rounded-full"
            style="width: 2.5rem; height: 2.5rem"
          >
            <i class="pi pi-users text-cyan-500 text-xl"></i>
          </div>
        </div>
        <span class="text-sm text-surface-500 dark:text-surface-400">Categorías configuradas</span>
      </div>
    </div>
  </div>
</template>
