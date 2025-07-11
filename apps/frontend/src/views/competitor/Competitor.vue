<template>
  <div class="grid card">
    <div class="col-12">
      <AppTitle title="Competidores" />
    </div>
    <div class="col-12">
      <DataTable
        :value="competitors"
        paginator
        :rows="8"
        :globalFilterFields="['name', 'instructor']"
      >
        <template #header>
          <div class="flex justify-end">
            <Button
              @click="showAcademyModalToCreate"
              icon="pi pi-plus"
              type="button"
              label="Crear Competidor"
            />
          </div>
        </template>

        <Column field="person.name" header="Nombre" />
        <Column field="academy.name" header="Academia" />
        <Column field="rank.description" header="Rango" />
        <Column field="sex.description" header="Sexo">
          <template #body="{ data }">
            <i
              :class="`pi pi-${
                data.sex.description === 'Hombre' ? 'mars' : 'venus'
              } text-${
                data.sex.description === 'Hombre' ? 'blue' : 'pink'
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

        <Column field="special_condition" header="Con. Especial">
          <template #body="{ data }">
            {{ data.special_condition ? "Sí" : "No" }}
          </template>
        </Column>

        <Column header="Editar">
          <template #body="slotProps">
            <Button
              @click="showAcademyModalToEdit(slotProps.data)"
              icon="pi pi-pencil"
              type="button"
              text
              rounded
            ></Button>
          </template>
        </Column>
      </DataTable>
    </div>
  </div>
</template>
<script setup>
import { useDialog } from "primevue/usedialog";
import { defineAsyncComponent, ref, onMounted } from "vue";
import { AcademyService } from "@/service/AcademyService";
import { CompetitorService } from "@/service/CompetitorService";
import { ModalityService } from "@/service/ModalityService";
import { RankService } from "@/service/RankService";
import { SexService } from "@/service/SexService";

const dialog = useDialog();

const dynamicComponent = defineAsyncComponent(() =>
  import("@/views/competitor/components/CreateCompetitor.vue")
);

const showAcademyModalToEdit = (data) => {
  dialog.open(dynamicComponent, {
    props: {
      header: "Editar Competidor",
      ...sharedModalProps,
    },
    data: { ranks, sexes, academies, modalities, ...data },
  });
};

const showAcademyModalToCreate = () => {
  dialog.open(dynamicComponent, {
    props: {
      header: "Crear Competidor",
      ...sharedModalProps,
    },
    data: { ranks, sexes, academies, modalities },
  });
};

const sharedModalProps = {
  style: {
    width: "25vw",
  },
  breakpoints: {
    "960px": "50vw",
    "640px": "90vw",
  },
  modal: true,
  dismissableMask: true,
};
const ranks = ref([]);
const sexes = ref([]);
const academies = ref([]);
const competitors = ref([]);
const modalities = ref([]);

onMounted(async () => {
  const data = [
    RankService.findAll(),
    CompetitorService.findAll(),
    SexService.findAll(),
    AcademyService.getAllAcademies(),
    ModalityService.findAll(),
  ];
  const [ranksData, competitorsData, sexesData, academiesData, modalitiesData] =
    await Promise.all(data);

  competitors.value = competitorsData;
  ranks.value = ranksData;
  sexes.value = sexesData;
  academies.value = academiesData;
  modalities.value = modalitiesData;
});
</script>
