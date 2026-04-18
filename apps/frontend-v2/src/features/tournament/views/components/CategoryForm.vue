<script setup lang="ts">
import { ref, inject, computed, onMounted } from "vue";
import { useToast } from "primevue/usetoast";
import { CategoryService } from "../../services/CategoryService";
import { RankGroupService } from "../../services/RankGroupService";
import type { CategoryCreate, CategoryUpdate, RankGroup } from "../../types";
import Accordion from 'primevue/accordion';
import AccordionPanel from 'primevue/accordionpanel';
import AccordionHeader from 'primevue/accordionheader';
import AccordionContent from 'primevue/accordioncontent';

const dialogRef = inject<any>("dialogRef");
const toast = useToast();

const isEdit = computed(() => !!dialogRef?.value?.data?.category);
const categoryToEdit = computed(() => dialogRef?.value?.data?.category);

const modalityOptions = computed(() => dialogRef?.value?.data?.modalities?.value ?? dialogRef?.value?.data?.modalities ?? []);
const sexOptions = computed(() => dialogRef?.value?.data?.sexes?.value ?? dialogRef?.value?.data?.sexes ?? []);
const rankGroups = ref<RankGroup[]>([]);

let nextUiId = 1;

const form = ref({
  ages: [] as number[],
  specialCondition: false,
  modalities: [] as {
    _uiId: number;
    modalityId: string;
    sexIds: string[];
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

    if (cat.modalities && cat.modalities.length > 0) {
      const flatList = cat.modalities.map((m: any) => ({
        modalityId: m.modality.id,
        sexIds: (m.sexes?.map((s: any) => s.id) || []).sort(),
        rankGroupId: m.rankGroup?.id,
        pr: m.physicalRequirement
      }));

      // Paso 1: Agrupar por modalidad + sexos + requerimiento fisico
      const step1Groups = new Map<string, any>();
      flatList.forEach((item: any) => {
        const prKey = item.pr ? `${item.pr.initialWeight}-${item.pr.finalWeight}-${item.pr.initialHeight}-${item.pr.finalHeight}` : 'none';
        const key = `${item.modalityId}|${item.sexIds.join(',')}|${prKey}`;
        
        if (!step1Groups.has(key)) {
          step1Groups.set(key, {
            modalityId: item.modalityId,
            sexIds: item.sexIds,
            pr: item.pr,
            rankGroupIds: new Set<string>()
          });
        }
        if (item.rankGroupId) {
          step1Groups.get(key).rankGroupIds.add(item.rankGroupId);
        }
      });

      // Paso 2: Agrupar por modalidad + sexos + arreglos exactos de grupos de rango combinados
      const finalGroups = new Map<string, any>();
      step1Groups.forEach((group: any) => {
        const rgKey = Array.from(group.rankGroupIds).sort().join(',');
        const key = `${group.modalityId}|${group.sexIds.join(',')}|${rgKey}`;
        
        if (!finalGroups.has(key)) {
          finalGroups.set(key, {
            _uiId: nextUiId++,
            modalityId: group.modalityId,
            sexIds: group.sexIds,
            rankGroupIds: Array.from(group.rankGroupIds),
            usePhysicalRequirement: false,
            physicalRequirements: [] as any[]
          });
        }
        
        if (group.pr) {
          finalGroups.get(key).usePhysicalRequirement = true;
          finalGroups.get(key).physicalRequirements.push({
            initialWeight: group.pr.initialWeight,
            finalWeight: group.pr.finalWeight,
            initialHeight: group.pr.initialHeight,
            finalHeight: group.pr.finalHeight,
          });
        }
      });

      form.value.modalities = Array.from(finalGroups.values()).map(g => {
        if (g.physicalRequirements.length === 0) {
          g.physicalRequirements.push({ initialWeight: null, finalWeight: null, initialHeight: 0, finalHeight: 200 });
        } else {
          // Force fixed height on rehydration if needed
          g.physicalRequirements.forEach((pr: any) => {
            pr.initialHeight = 0;
            pr.finalHeight = 200;
          });
        }
        return g;
      });
    }
  }
});

function addModalityBlock(): void {
  form.value.modalities.push({
    _uiId: nextUiId++,
    modalityId: "",
    sexIds: [],
    rankGroupIds: [],
    usePhysicalRequirement: false,
    physicalRequirements: [{
      initialWeight: null,
      finalWeight: null,
      initialHeight: 0,
      finalHeight: 200,
    }],
  });
}

function removeModalityBlock(index: number): void {
  form.value.modalities.splice(index, 1);
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
  if (form.value.modalities.length === 0) {
    toast.add({ severity: "warn", summary: "Validación", detail: "Añade al menos una subcategoría/modalidad.", life: 3000 });
    return;
  }
  for (let i = 0; i < form.value.modalities.length; i++) {
    const m = form.value.modalities[i];
    if (!m.modalityId) {
      toast.add({ severity: "warn", summary: "Validación", detail: `Selecciona una modalidad para la subcategoría ${i + 1}.`, life: 3000 });
      return;
    }
    if (!m.rankGroupIds || m.rankGroupIds.length === 0) {
      toast.add({ severity: "warn", summary: "Validación", detail: `Selecciona al menos un grupo de rangos para la subcategoría ${i + 1}.`, life: 3000 });
      return;
    }
    if (!m.sexIds || m.sexIds.length === 0) {
      toast.add({ severity: "warn", summary: "Validación", detail: `Selecciona al menos un sexo para la subcategoría ${i + 1}.`, life: 3000 });
      return;
    }
    if (m.usePhysicalRequirement) {
      const hasValidPr = m.physicalRequirements.some(pr => 
        pr.initialWeight !== null || pr.finalWeight !== null
      );
      if (!hasValidPr) {
        toast.add({ severity: "warn", summary: "Validación", detail: `Llene al menos un límite de peso para los requerimientos físicos en la subcategoría ${i + 1}, o desactive la opción.`, life: 5000 });
        return;
      }
    }
  }

  submitting.value = true;
  const payload: CategoryCreate = {
    ages: form.value.ages,
    specialCondition: form.value.specialCondition,
    modalities: form.value.modalities.map((m) => ({
      modalityId: m.modalityId,
      sexIds: m.sexIds,
      rankGroupIds: m.rankGroupIds,
      physicalRequirements: m.usePhysicalRequirement ? m.physicalRequirements.filter(pr => 
        pr.initialWeight !== null || pr.finalWeight !== null
      ).map(pr => ({
        ...pr,
        initialHeight: 0,
        finalHeight: 200
      })) : [],
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
    initialHeight: 0,
    finalHeight: 200,
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

      <div class="flex items-center gap-2">
        <Checkbox v-model="form.specialCondition" :binary="true" inputId="sc-check" />
        <label for="sc-check" class="text-sm font-medium">Condición Especial (Ej. Discapacidad)</label>
      </div>
    </div>

    <!-- Modalidades y Requerimientos -->
    <div class="surface-card p-4 border-round shadow-1 flex flex-col gap-4">
      <div class="flex justify-between items-center mb-0">
        <h3 class="text-xl font-bold m-0">Modalidades y Requerimientos</h3>
        <Button label="Añadir Subcategoría" icon="pi pi-plus" size="small" @click="addModalityBlock" />
      </div>

      <div v-if="form.modalities.length > 0" class="mt-2">
        <Accordion :value="form.modalities[0]._uiId">
          <AccordionPanel v-for="(mod, modIndex) in form.modalities" :key="mod._uiId" :value="mod._uiId">
            
            <AccordionHeader>
              <div class="flex justify-between items-center w-full pr-4">
                <span class="font-bold">{{ mod.modalityId ? getModalityName(mod.modalityId) : 'Nueva Subcategoría' }}</span>
                <Button icon="pi pi-trash" severity="danger" text rounded 
                        class="h-8 w-8 !p-0"
                        @click.stop="removeModalityBlock(modIndex)" title="Eliminar subcategoría" />
              </div>
            </AccordionHeader>
            
            <AccordionContent>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4 mt-2">
                <div class="flex flex-col gap-2">
                  <label class="text-xs font-semibold">Seleccionar Modalidad</label>
                  <Dropdown
                    v-model="mod.modalityId"
                    :options="modalityOptions"
                    optionLabel="name"
                    optionValue="id"
                    placeholder="Elegir una modalidad"
                    fluid
                    class="p-inputtext-sm"
                  />
                </div>
                <div class="flex items-center gap-2 justify-end self-end h-[38px]">
                  <span class="text-xs font-semibold">Usar Requerimientos físicos</span>
                  <ToggleButton v-model="mod.usePhysicalRequirement" onLabel="Si" offLabel="No" class="w-16 h-8 text-xs" />
                </div>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                <div class="flex flex-col gap-2">
                  <label class="text-xs font-semibold">Sexos permitidos</label>
                  <MultiSelect
                    v-model="mod.sexIds"
                    :options="sexOptions"
                    optionLabel="name"
                    optionValue="id"
                    placeholder="Select genders"
                    display="chip"
                    fluid
                    class="p-inputtext-sm"
                  />
                </div>
                <div class="flex flex-col gap-2">
                  <label class="text-xs font-semibold">Grupos de Rangos</label>
                  <MultiSelect
                    v-model="mod.rankGroupIds"
                    :options="rankGroups"
                    optionLabel="name"
                    optionValue="id"
                    placeholder="Select ranks"
                    display="chip"
                    fluid
                    class="p-inputtext-sm"
                  />
                </div>
              </div>

              <div v-if="mod.usePhysicalRequirement" class="flex flex-col gap-3 animate-fade-in border-t-1 border-surface-200 mt-2 pt-3">
                <div class="flex justify-between items-center px-1">
                  <label class="text-xs font-bold uppercase text-surface-500">Rangos Físicos</label>
                  <Button icon="pi pi-plus" label="Añadir Rango" @click="addPhysicalRequirement(form.modalities.indexOf(mod))" 
                          class="p-button-text p-button-sm text-xs h-8" />
                </div>

                <div v-for="(pr, reqIdx) in mod.physicalRequirements" :key="reqIdx" 
                     class="grid grid-cols-[1fr,auto] gap-3 items-end p-2 border-round bg-surface-100 dark:bg-surface-800 relative">
                  <div class="flex flex-col gap-1">
                    <label class="text-[10px] font-semibold text-surface-500">Peso (Kg)</label>
                    <div class="flex items-center gap-1">
                      <InputNumber v-model="pr.initialWeight" :minFractionDigits="1" placeholder="Min" fluid inputClass="p-inputtext-sm" />
                      <InputNumber v-model="pr.finalWeight" :minFractionDigits="1" placeholder="Max" fluid inputClass="p-inputtext-sm" />
                    </div>
                  </div>
                  <Button icon="pi pi-times" severity="danger" text rounded 
                          @click="removePhysicalRequirement(form.modalities.indexOf(mod), reqIdx)" 
                          class="h-8 w-8" v-if="mod.physicalRequirements.length > 1" />
                </div>
              </div>
            </AccordionContent>
          </AccordionPanel>
        </Accordion>
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
