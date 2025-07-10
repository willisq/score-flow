<template>
  <div class="grid">
    <div class="col-12">
      <DataTable :value="competitors" paginator :rows="10">
        <template #header>
          <div class="flex justify-between items-end">
            <div class="flex flex-col items-start gap-1">
              <Tag :value="category.modality?.name" class="mb-2"></Tag>
              <div v-if="category.special_condition">
                <Tag
                  value="Condición Especial"
                  class="!bg-indigo-600 !text-white"
                />
              </div>

              <span class="text-lg font-semibold"
                >Edades: {{ category.initial_age }} -
                {{ category.final_age }} Años</span
              >
              <span class="text-lg font-semibold"
                >Pesos: {{ category.initial_weight }} -
                {{ category.final_weight }} Kg</span
              >
              <span v-if="category.initial_height" class="text-lg font-semibold"
                >Alturas: {{ category.initial_height }} -
                {{ category.final_height }} cm</span
              >
            </div>

            <div class="flex flex-col gap-1">
              <template
                v-for="(rank, rankIndex) in category.ranks"
                :key="rankIndex"
              >
                <Tag :value="rank.description"></Tag>
              </template>
            </div>

            <div class="flex flex-col gap-6">
              <Button
                icon="pi pi-sitemap"
                @click="confirmCreateCategory($event)"
                label="Armar Piramide"
              />
            </div>
            <ConfirmPopup></ConfirmPopup>
          </div>
        </template>
        <Column field="person.firstname" header="Nombre" />
        <Column field="person.lastname" header="Apellido" />
        <Column field="rank.description" header="Rango" />
        <Column field="sex.description" header="Sexo">
          <template #body="{ data }">
            <i
              :class="`pi pi-${
                data.sex.description === 'hombre' ? 'mars' : 'venus'
              } text-${
                data.sex.description === 'hombre' ? 'blue' : 'pink'
              }-500`"
            ></i>
          </template>
        </Column>
        <Column field="weight" header="Peso">
          <template #body="{ data }"> {{ data.weight }} Kg </template>
        </Column>
        <Column field="height" header="Altura">
          <template #body="{ data }">
            <span v-if="data.height">{{ data.height }} cm</span>
            <span v-else>----</span>
          </template>
        </Column>
        <Column field="age" header="Edad"
          ><template #body="{ data }"> {{ data.age }} Años </template>
        </Column>
      </DataTable>
    </div>
  </div>
</template>
<script setup>
import { ref, inject, onMounted } from "vue";
import { useConfirm } from "primevue/useconfirm";
import { useToast } from "primevue/usetoast";

import { PyramidService } from "@/service/PyramidService";

const confirm = useConfirm();
const toast = useToast();

const category = ref({});
const competitors = ref([]);

const dialogRef = inject("dialogRef");

const confirmCreateCategory = (event) => {
  confirm.require({
    target: event.currentTarget,
    message: "Se Generará la pirmide. ¿Desea continuar?",
    icon: "pi pi-exclamation-triangle",
    accept: async () => {
      await PyramidService.assemblePyramid({
        category: category.value.id,
      });

      toast.add({
        severity: "info",
        summary: "Piramide Creada",
        life: 4000,
      });
    },
  });
};

onMounted(() => {
  category.value = dialogRef.value.data.categoryData;
  competitors.value = dialogRef.value.data.competitors;
});
</script>
