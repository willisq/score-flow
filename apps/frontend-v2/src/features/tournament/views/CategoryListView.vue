<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { useDialog } from "primevue/usedialog";
import { CategoryService } from "../services/CategoryService";
import type { Category, CategoryModality } from "../types";
import CategoryForm from "./components/CategoryForm.vue";
import CategoryCompetitorList from "./components/CategoryCompetitorList.vue";
import { useRegistrationData } from "@/features/registration/composables/useRegistrationData";
import { useTournamentData } from "../composables/useTournamentData";

const dialog = useDialog();
const { ranks, sexes } = useRegistrationData();
const { modalities } = useTournamentData();

const categories = ref<Category[]>([]);
const loading = ref(true);

const flatCategories = computed(() => {
  return categories.value.flatMap((cat) =>
    cat.modalities.map((mod) => ({
      ...mod,
      // Pass category data along with modality
      ages: cat.ages,
      specialCondition: cat.specialCondition,
      ranks: cat.ranks,
      sexes: cat.sexes,
    }))
  );
});

async function loadCategories(): Promise<void> {
  loading.value = true;
  try {
    categories.value = await CategoryService.getAll();
  } finally {
    loading.value = false;
  }
}

function openCreateDialog(): void {
  dialog.open(CategoryForm, {
    props: {
      header: "Crear Categoría",
      style: { width: "50vw" },
      breakpoints: { "960px": "80vw", "640px": "90vw" },
      modal: true,
      dismissableMask: true,
    },
    data: { ranks, sexes, modalities },
    onClose: () => loadCategories(),
  });
}

function showCompetitors(categoryModality: any): void {
  dialog.open(CategoryCompetitorList, {
    props: {
      header: "Competidores en la Categoría",
      style: { width: "50vw" },
      breakpoints: { "960px": "80vw", "640px": "90vw" },
      modal: true,
      dismissableMask: true,
    },
    data: { categoryModality },
  });
}

onMounted(loadCategories);
</script>

<template>
  <div class="card">
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-2xl font-bold">Categorías</h2>
      <Button icon="pi pi-plus" label="Nueva Categoría" @click="openCreateDialog" />
    </div>

    <DataView :value="flatCategories" :loading="loading" paginator :rows="5">
      <template #list="slotProps">
        <div class="flex flex-col">
          <div
            v-for="(item, index) in slotProps.items"
            :key="item.id"
            class="flex flex-col sm:flex-row sm:items-center justify-between p-6 gap-4"
            :class="{ 'border-t border-surface-200 dark:border-surface-700': index !== 0 }"
          >
            <div class="flex flex-col items-start gap-1">
              <Tag :value="item.modality.name" class="mb-2" />
              <span class="text-lg font-semibold">
                Edades: {{ Math.min(...item.ages) }} – {{ Math.max(...item.ages) }} años
              </span>
              <span v-if="item.physicalRequirement?.initialWeight != null" class="text-lg font-semibold">
                Pesos: {{ item.physicalRequirement.initialWeight }} – {{ item.physicalRequirement.finalWeight }} Kg
              </span>
              <span v-if="item.physicalRequirement?.initialHeight != null" class="text-lg font-semibold">
                Alturas: {{ item.physicalRequirement.initialHeight }} – {{ item.physicalRequirement.finalHeight }} cm
              </span>
            </div>

            <div class="flex flex-col gap-1">
              <Tag v-for="rank in item.ranks" :key="rank.id" :value="rank.name" />
            </div>

            <div class="flex flex-col md:items-end gap-4">
              <Tag v-if="item.specialCondition" value="Condición Especial" severity="info" />
              <div class="flex gap-1">
                <i
                  v-for="sex in item.sexes"
                  :key="sex.id"
                  :class="[
                    'pi text-lg',
                    sex.name === 'Masculino' || sex.name === 'Hombre'
                      ? 'pi-mars text-blue-500'
                      : 'pi-venus text-pink-500',
                  ]"
                ></i>
              </div>
              <Button icon="pi pi-list" label="Ver Competidores" @click="showCompetitors(item)" />
            </div>
          </div>
        </div>
      </template>
    </DataView>
  </div>
</template>
