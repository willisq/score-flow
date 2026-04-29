<script setup lang="ts">
import { ref, computed, watch } from "vue";
import { useToast } from "primevue/usetoast";
import { BracketService } from "../../services/BracketService";

const props = defineProps<{
  visible: boolean;
  registrationId: string;
  sourceCmId: string;
  competitor: any;
  categories: any[];
  ranks: any[];
}>();

const emit = defineEmits(["update:visible", "moved"]);

const toast = useToast();
const loading = ref(false);
const selectedTargetId = ref<string | null>(null);

// Form for physical updates
const form = ref({
  weight: 0,
  age: 0,
  rankId: "",
});

watch(() => props.visible, (newVal) => {
  if (newVal && props.competitor) {
    form.value.weight = props.competitor.weight || 0;
    form.value.age = props.competitor.age || 0;
    form.value.rankId = props.competitor.rank.id;
    selectedTargetId.value = null;
  }
});

const targetCategory = computed(() => {
  return props.categories.find(c => c.id === selectedTargetId.value);
});

const eligibility = computed(() => {
  if (!targetCategory.value) return null;
  const cm = targetCategory.value;
  
  // Age check
  const ages = cm.category.ages;
  const ageMatch = ages.includes(form.value.age);
  
  // Weight check
  const pr = cm.modality.physicalRequirement;
  let weightMatch = true;
  if (pr) {
    if (pr.initialWeight !== null && form.value.weight < pr.initialWeight) weightMatch = false;
    if (pr.finalWeight !== null && form.value.weight > pr.finalWeight) weightMatch = false;
  }
  
  // Rank check
  const rankMatch = cm.modality.ranks ? cm.modality.ranks.some((r: any) => r.id === form.value.rankId) : true;

  // Sex check
  const sexMatch = cm.modality.sexes.some((s: any) => s.id === props.competitor.sex.id);

  return {
    age: ageMatch,
    weight: weightMatch,
    rank: rankMatch,
    sex: sexMatch,
    all: ageMatch && weightMatch && rankMatch && sexMatch
  };
});

async function handleMove() {
  if (!selectedTargetId.value || !eligibility.value?.all) return;
  
  loading.value = true;
  try {
    await BracketService.moveCompetitor(props.sourceCmId, props.registrationId, {
      targetCategoryModalityId: selectedTargetId.value,
      competitorId: props.competitor.id,
      newWeight: form.value.weight,
      newAge: form.value.age,
      newRankId: form.value.rankId
    });
    
    toast.add({
      severity: "success",
      summary: "Movimiento exitoso",
      detail: "El competidor ha sido movido y las pirámides regeneradas.",
      life: 3000
    });
    
    emit("moved");
    emit("update:visible", false);
  } catch (error: any) {
    toast.add({
      severity: "error",
      summary: "Error",
      detail: error.response?.data?.detail || "No se pudo realizar el movimiento.",
      life: 5000
    });
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <Dialog :visible="visible" @update:visible="$emit('update:visible', $event)" modal header="Mover Competidor de Pirámide" :style="{ width: '50vw' }" :breakpoints="{ '960px': '75vw', '641px': '95vw' }">
    <div class="flex flex-col gap-4">
      <div v-if="competitor" class="p-4 bg-primary-50 dark:bg-primary-900/20 rounded-lg border border-primary-100 dark:border-primary-800 mb-2">
        <div class="flex items-center gap-3">
          <i class="pi pi-user text-2xl text-primary-500"></i>
          <div>
            <div class="font-bold text-lg">{{ competitor.firstName }} {{ competitor.lastName }}</div>
            <div class="text-sm text-surface-500">{{ competitor.academy.name }}</div>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Step 1: Select Category -->
        <div class="flex flex-col gap-3">
          <h3 class="font-bold flex items-center gap-2">
            <span class="bg-primary-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-xs">1</span>
            Seleccionar Categoría Destino
          </h3>
          <div class="flex flex-col gap-1">
            <label for="target">Categoría</label>
            <Dropdown id="target" v-model="selectedTargetId" :options="categories" optionLabel="displayName" optionValue="id" 
              placeholder="Buscar categoría..." filter class="w-full" :loading="loading" />
          </div>

          <div v-if="targetCategory" class="mt-2 p-3 bg-surface-50 dark:bg-surface-800 rounded border border-surface-200 dark:border-surface-700 text-sm">
            <div class="font-semibold mb-1">Requisitos de la categoría:</div>
            <ul class="list-disc ml-4 space-y-1">
              <li><span class="font-medium">Edades:</span> {{ targetCategory.ageStr }}</li>
              <li><span class="font-medium">Sexo:</span> {{ targetCategory.sexesStr }}</li>
              <li><span class="font-medium">Rango:</span> {{ targetCategory.ranksStr }}</li>
              <li v-if="targetCategory.weightStr"><span class="font-medium">Peso:</span> {{ targetCategory.weightStr }}</li>
            </ul>
          </div>
        </div>

        <!-- Step 2: Physical Updates -->
        <div class="flex flex-col gap-3">
          <h3 class="font-bold flex items-center gap-2">
            <span class="bg-primary-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-xs">2</span>
            Ajustar Datos del Competidor
          </h3>
          
          <div class="flex flex-col gap-1">
            <label for="age">Edad</label>
            <InputNumber id="age" v-model="form.age" :min="0" class="w-full" :invalid="eligibility && !eligibility.age" />
            <small v-if="eligibility && !eligibility.age" class="text-red-500">La edad no coincide con la categoría.</small>
          </div>

          <div class="flex flex-col gap-1">
            <label for="weight">Peso (Kg)</label>
            <InputNumber id="weight" v-model="form.weight" mode="decimal" :minFractionDigits="1" :maxFractionDigits="2" class="w-full" :invalid="eligibility && !eligibility.weight" />
            <small v-if="eligibility && !eligibility.weight" class="text-red-500">El peso está fuera del rango permitido.</small>
          </div>

          <div class="flex flex-col gap-1">
            <label for="rank">Rango</label>
            <Dropdown id="rank" v-model="form.rankId" :options="ranks" optionLabel="name" optionValue="id" filter class="w-full" :invalid="eligibility && !eligibility.rank" />
            <small v-if="eligibility && !eligibility.rank" class="text-red-500">El rango no es válido para esta categoría.</small>
          </div>

          <div v-if="eligibility && !eligibility.sex" class="p-2 bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 rounded text-xs flex items-center gap-2">
            <i class="pi pi-exclamation-circle"></i>
            <span>El sexo del competidor no es admitido en esta categoría.</span>
          </div>
        </div>
      </div>
    </div>

    <template #footer>
      <div class="flex justify-end gap-2 mt-4">
        <Button label="Cancelar" icon="pi pi-times" severity="secondary" outlined @click="$emit('update:visible', false)" :disabled="loading" />
        <Button label="Confirmar Movimiento" icon="pi pi-check" @click="handleMove" :loading="loading" :disabled="!selectedTargetId || !eligibility?.all" />
      </div>
    </template>
  </Dialog>
</template>
