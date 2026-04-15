<script setup lang="ts">
import { inject, onMounted, ref } from "vue";
import type { Category } from "../../types";
import type { Competitor } from "@/features/registration/types";
import { CategoryService } from "../../services/CategoryService";

const dialogRef = inject<any>("dialogRef");
const category = dialogRef?.value?.data?.category as Category | undefined;
const competitors = ref<Competitor[]>([]);
const loading = ref(true);

onMounted(async () => {
  if (!category?.id) {
    loading.value = false;
    return;
  }

  try {
    competitors.value = await CategoryService.getCompetitors(category.id);
  } catch (error) {
    console.error("Error fetching competitors:", error);
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <div class="flex flex-col gap-4 p-2">
    <div v-if="category" class="flex gap-2 items-center flex-wrap">
      <Tag :value="category.modality.name" severity="secondary" />
      <span class="text-sm font-medium text-surface-600 dark:text-surface-400">
        {{ Math.min(...category.ages) }} – {{ Math.max(...category.ages) }} años
      </span>
      <Divider layout="vertical" class="hidden sm:block" />
      <div class="flex gap-1">
        <Tag v-for="rank in category.ranks" :key="rank.id" :value="rank.name" severity="info"
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
    </DataTable>
  </div>
</template>
