<script setup lang="ts">
import { inject } from "vue";
import type { Category } from "../../types";
import type { Competitor } from "@/features/registration/types";

const dialogRef = inject<any>("dialogRef");
const category = dialogRef?.value?.data?.category as Category | undefined;
const competitors = (dialogRef?.value?.data?.competitors ?? []) as Competitor[];
</script>

<template>
  <div class="flex flex-col gap-4 p-2">
    <div v-if="category" class="flex gap-2 items-center flex-wrap">
      <Tag :value="category.modality.name" />
      <span class="text-sm text-surface-500">
        Edades: {{ Math.min(...category.ages) }} – {{ Math.max(...category.ages) }}
      </span>
    </div>

    <DataTable :value="competitors" :rows="10" paginator>
      <template #empty>
        <div class="text-center text-surface-500 py-4">No hay competidores en esta categoría.</div>
      </template>

      <Column header="Nombre">
        <template #body="{ data }">
          {{ data.firstName }} {{ data.lastName }}
        </template>
      </Column>
      <Column field="academy.name" header="Academia" />
      <Column field="rank.name" header="Rango" />
      <Column field="weight" header="Peso">
        <template #body="{ data }">
          {{ data.weight ? `${data.weight} Kg` : "—" }}
        </template>
      </Column>
    </DataTable>
  </div>
</template>
