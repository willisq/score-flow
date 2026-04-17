<script setup lang="ts">
import { ref, inject, computed, onMounted } from "vue";
import { useToast } from "primevue/usetoast";
import { CategoryService } from "../../services/CategoryService";
import { RankGroupService } from "../../services/RankGroupService";
import type { CategoryCreate, CategoryUpdate, RankGroup } from "../../types";

const dialogRef = inject<any>("dialogRef");
const toast = useToast();

const isEdit = computed(() => !!dialogRef?.value?.data?.category);
const categoryToEdit = computed(() => dialogRef?.value?.data?.category);

const modalityOptions = computed(() => dialogRef?.value?.data?.modalities?.value ?? dialogRef?.value?.data?.modalities ?? []);
const sexOptions = computed(() => dialogRef?.value?.data?.sexes?.value ?? dialogRef?.value?.data?.sexes ?? []);
const rankGroups = ref<RankGroup[]>([]);

const form = ref({
  ages: [] as number[],
  specialCondition: false,
  sexIds: [] as string[],
  modalities: [] as {
    modalityId: string;
    rankGroupIds: string[];
    usePhysicalRequirement: boolean;
    physicalRequirements: {
      initialWeight: number | null;
      finalWeight: number | null;
      initialHeight: number | null;
      finalHeight: number | null;
    }[];
  }[],
});

const selectedModalityIds = ref<string[]>([]);

onMounted(async () => {
  try {
    rankGroups.value = await RankGroupService.getAll();
  } catch (error) {
    toast.add({ severity: "error", summary: "Error", detail: "No se pudieron cargar los grupos de rangos.", life: 3000 });
  }

  if (isEdit.value && categoryToEdit.value) {
    const cat = categoryToEdit.value;
    form.value.ages = [...cat.ages];
    form.value.specialCondition = cat.specialCondition;
    if (cat.sexes) form.value.sexIds = cat.sexes.map((s: any) => s.id);

    if (cat.modalities) {
      selectedModalityIds.value = [...new Set(cat.modalities.map((m: any) => m.modality.id) as string[])];
      
      // Agrupar por modalidad
      const groups: Record<string, any> = {};
      
      cat.modalities.forEach((m: any) => {
        const modalityId = m.modality.id;
        const rgid = m.rankGroup?.id;
        const pr = m.physicalRequirement;
        
        if (!groups[modalityId]) {
          groups[modalityId] = {
            modalityId: modalityId,
            rankGroupIds: new Set<string>(),
            usePhysicalRequirement: false,
            physicalRequirements: [] as any[],
          };
        }
        
        if (rgid) groups[modalityId].rankGroupIds.add(rgid);
        
        if (pr) {
          groups[modalityId].usePhysicalRequirement = true;
          // Evitar duplicados si vienen de la base de datos (aunque deberían ser únicos)
          const alreadyExists = groups[modalityId].physicalRequirements.some((existing: any) => 
            existing.initialWeight === pr.initialWeight &&
            existing.finalWeight === pr.finalWeight &&
            existing.initialHeight === pr.initialHeight &&
            existing.finalHeight === pr.finalHeight
          );
          if (!alreadyExists) {
            groups[modalityId].physicalRequirements.push({
              initialWeight: pr.initialWeight,
              finalWeight: pr.finalWeight,
              initialHeight: pr.initialHeight,
              finalHeight: pr.finalHeight,
            });
          }
        }
      });
      
      form.value.modalities = Object.values(groups).map((g: any) => ({
        modalityId: g.modalityId,
        rankGroupIds: Array.from(g.rankGroupIds),
        usePhysicalRequirement: g.usePhysicalRequirement,
        physicalRequirements: g.physicalRequirements.length > 0 ? g.physicalRequirements : [{ initialWeight: null, finalWeight: null, initialHeight: null, finalHeight: null }]
      }));
    }
  }
});

function onModalitiesChange(): void {
  // Add new modalities
  selectedModalityIds.value.forEach((id) => {
    if (!form.value.modalities.find((m) => m.modalityId === id)) {
      form.value.modalities.push({
        modalityId: id,
        rankGroupIds: [],
        usePhysicalRequirement: false,
        physicalRequirements: [{
          initialWeight: null,
          finalWeight: null,
          initialHeight: null,
          finalHeight: null,
        }],
      });
    }
  });
  // Remove unselected
  form.value.modalities = form.value.modalities.filter((m) =>
    selectedModalityIds.value.includes(m.modalityId)
  );
}

const submitting = ref(false);
const ageInput = ref<string>("");

function addAge(): void {
  const age = Number.parseInt(ageInput.value, 10);
  if (!Number.isNaN(age) && !form.value.ages.includes(age)) {
    form.value.ages.push(age);
    form.value.ages.sort((a, b) => a - b);
  }
  ageInput.value = "";
}

function removeAge(age: number): void {
  form.value.ages = form.value.ages.filter((a) => a !== age);
}

async function onSubmit(): Promise<void> {
  // Validation: Each modality must have at least one rank group
  if (form.value.modalities.some(m => !m.rankGroupIds || m.rankGroupIds.length === 0)) {
    toast.add({ severity: "warn", summary: "Validación", detail: "Por favor, selecciona al menos un grupo de rangos para cada modalidad.", life: 3000 });
    return;
  }

  submitting.value = true;
  const payload: CategoryCreate = {
    ages: form.value.ages,
    specialCondition: form.value.specialCondition,
    sexIds: form.value.sexIds,
    modalities: form.value.modalities.map((m) => ({
      modalityId: m.modalityId,
      rankGroupIds: m.rankGroupIds,
      physicalRequirements: m.usePhysicalRequirement ? m.physicalRequirements.filter(pr => 
        pr.initialWeight !== null || pr.finalWeight !== null || 
        pr.initialHeight !== null || pr.finalHeight !== null
      ) : [],
    })),
  };

  try {
    if (isEdit.value) {
      await CategoryService.update(categoryToEdit.value.id, payload as CategoryUpdate);
      toast.add({ severity: "success", summary: "Éxito", detail: "Categoría actualizada.", life: 3000 });
    } else {
      await CategoryService.create(payload);
      toast.add({ severity: "success", summary: "Éxito", detail: "Categoría creada.", life: 3000 });
    }
    dialogRef?.value?.close();
  } catch {
    toast.add({
      severity: "error",
      summary: "Error",
      detail: `No se pudo ${isEdit.value ? "actualizar" : "crear"} la categoría.`,
      life: 5000,
    });
  } finally {
    submitting.value = false;
  }
}

function getModalityName(id: string): string {
  return modalityOptions.value.find((m: any) => m.id === id)?.name || "Desconocida";
}

function addPhysicalRequirement(modIndex: number): void {
  form.value.modalities[modIndex].physicalRequirements.push({
    initialWeight: null,
    finalWeight: null,
    initialHeight: null,
    finalHeight: null,
  });
}

function removePhysicalRequirement(modIndex: number, reqIndex: number): void {
  form.value.modalities[modIndex].physicalRequirements.splice(reqIndex, 1);
  if (form.value.modalities[modIndex].physicalRequirements.length === 0) {
    addPhysicalRequirement(modIndex);
  }
}
</script>

<template>
  <form class="flex flex-col gap-6 p-2" @submit.prevent="onSubmit">
    <!-- Grupo Principal -->
    <div class="surface-card p-4 border-round shadow-1 flex flex-col gap-4">
      <h3 class="text-xl font-bold mb-2">Configuración Base</h3>
      
      <div class="flex flex-col gap-2">
        <label class="font-semibold text-sm">Edades</label>
        <div class="flex gap-2">
          <InputText v-model="ageInput" placeholder="Agregar edad" @keyup.enter="addAge" class="flex-1" />
          <Button icon="pi pi-plus" @click="addAge" type="button" />
        </div>
        <div class="flex gap-1 flex-wrap mt-2">
          <Chip v-for="age in form.ages" :key="age" :label="String(age)" removable @remove="removeAge(age)" />
        </div>
      </div>

      <div class="grid grid-cols-1 gap-4">
        <div class="flex flex-col gap-2">
          <label class="font-semibold text-sm">Sexos Globales</label>
          <MultiSelect
            v-model="form.sexIds"
            :options="sexOptions"
            optionLabel="name"
            optionValue="id"
            placeholder="Seleccionar sexos"
            display="chip"
            fluid
          />
        </div>
      </div>

      <div class="flex items-center gap-2">
        <Checkbox v-model="form.specialCondition" :binary="true" inputId="sc-check" />
        <label for="sc-check" class="text-sm font-medium">Condición Especial</label>
      </div>
    </div>

    <!-- Modalidades y Requerimientos -->
    <div class="surface-card p-4 border-round shadow-1 flex flex-col gap-4">
      <h3 class="text-xl font-bold mb-2">Modalidades y Requerimientos</h3>
      
      <div class="flex flex-col gap-2">
        <label class="font-semibold text-sm">Seleccionar Modalidades</label>
        <MultiSelect
          v-model="selectedModalityIds"
          :options="modalityOptions"
          optionLabel="name"
          optionValue="id"
          placeholder="Añadir modalidades a esta categoría"
          @change="onModalitiesChange"
          fluid
        />
      </div>

      <div v-if="form.modalities.length > 0" class="flex flex-col gap-4 mt-2">
        <div v-for="mod in form.modalities" :key="mod.modalityId" 
             class="border-1 border-surface-200 p-3 border-round bg-surface-50 dark:bg-surface-900">
          <div class="flex justify-between items-center mb-3">
            <span class="font-bold text-primary">{{ getModalityName(mod.modalityId) }}</span>
            <div class="flex items-center gap-2">
              <span class="text-xs">Requerimientos físicos</span>
              <ToggleButton v-model="mod.usePhysicalRequirement" onLabel="Si" offLabel="No" class="w-16 h-8 text-xs" />
            </div>
          </div>

          <div class="flex flex-col gap-3 mb-4">
            <label class="text-xs font-semibold">Grupos de Rangos para esta modalidad</label>
            <MultiSelect
              v-model="mod.rankGroupIds"
              :options="rankGroups"
              optionLabel="name"
              optionValue="id"
              placeholder="Seleccionar grupos de rangos"
              display="chip"
              fluid
              class="w-full"
            />
          </div>

          <div v-if="mod.usePhysicalRequirement" class="flex flex-col gap-3 animate-fade-in border-t-1 border-surface-200 mt-2 pt-3">
            <div class="flex justify-between items-center px-1">
              <label class="text-xs font-bold uppercase text-surface-500">Rangos Físicos</label>
              <Button icon="pi pi-plus" label="Añadir Rango" @click="addPhysicalRequirement(form.modalities.indexOf(mod))" 
                      class="p-button-text p-button-sm text-xs h-8" />
            </div>

            <div v-for="(pr, reqIdx) in mod.physicalRequirements" :key="reqIdx" 
                 class="grid grid-cols-[1fr,1fr,auto] gap-3 items-end p-2 border-round bg-surface-100 dark:bg-surface-800 relative">
              <div class="flex flex-col gap-1">
                <label class="text-[10px] font-semibold text-surface-500">Peso (Kg)</label>
                <div class="flex items-center gap-1">
                  <InputNumber v-model="pr.initialWeight" :minFractionDigits="1" placeholder="Min" fluid inputClass="p-inputtext-sm" />
                  <InputNumber v-model="pr.finalWeight" :minFractionDigits="1" placeholder="Max" fluid inputClass="p-inputtext-sm" />
                </div>
              </div>
              <div class="flex flex-col gap-1">
                <label class="text-[10px] font-semibold text-surface-500">Altura (cm)</label>
                <div class="flex items-center gap-1">
                  <InputNumber v-model="pr.initialHeight" :minFractionDigits="1" placeholder="Min" fluid inputClass="p-inputtext-sm" />
                  <InputNumber v-model="pr.finalHeight" :minFractionDigits="1" placeholder="Max" fluid inputClass="p-inputtext-sm" />
                </div>
              </div>
              <Button icon="pi pi-times" severity="danger" text rounded 
                      @click="removePhysicalRequirement(form.modalities.indexOf(mod), reqIdx)" 
                      class="h-8 w-8" v-if="mod.physicalRequirements.length > 1" />
            </div>
          </div>
        </div>
      </div>
      <div v-else class="text-center py-4 text-surface-400 italic text-sm">
        No hay modalidades seleccionadas.
      </div>
    </div>

    <Button 
      type="submit" 
      :label="isEdit ? 'Actualizar Categoría' : 'Crear Categoría'" 
      :icon="isEdit ? 'pi pi-save' : 'pi pi-plus'" 
      :loading="submitting" 
      class="mt-2"
    />
  </form>
</template>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-5px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
