<template>
  <div class="grid card">
    <div class="col-12">
      <AppTitle title="Academias" />
    </div>
    <div class="col-12">
      <DataTable
        v-model:filters="filters"
        :value="academies"
        paginator
        :rows="8"
        filterDisplay="row"
        :globalFilterFields="['name', 'instructor']"
      >
        <template #header>
          <div class="flex justify-end">
            <Button
              @click="showAcademyModalToCreate"
              icon="pi pi-plus"
              type="button"
              label="Nueva Academia"
            />
          </div>
        </template>
        <Column field="name" header="Nombre">
          <template #body="{ data }">
            {{ data.name }}
          </template>
          <template #filter="{ filterModel, filterCallback }">
            <InputText
              v-model="filterModel.value"
              type="text"
              @input="filterCallback()"
              placeholder="Buscar por Nombre"
            /> </template
        ></Column>
        <Column field="instructor" header="Instructor">
          <template #body="{ data }">
            {{ data.instructor }}
          </template>
          <template #filter="{ filterModel, filterCallback }">
            <InputText
              v-model="filterModel.value"
              type="text"
              @input="filterCallback()"
              placeholder="Buscar por Instructor"
            /> </template
        ></Column>
        <Column>
          <template #body="slotProps">
            <Button
              @click="showAcademyModalToEdit(slotProps.data)"
              icon="pi pi-pencil"
              type="button"
              text
              rounded
            ></Button> </template
        ></Column>
      </DataTable>
    </div>
  </div>
</template>
<script setup>
import { FilterMatchMode } from "@primevue/core/api";
import { useDialog } from "primevue/usedialog";
import { defineAsyncComponent, ref } from "vue";

const dialog = useDialog();

const dynamicComponent = defineAsyncComponent(() =>
  import("@/views/academy/components/CreateAcademy.vue")
);

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

const showAcademyModalToEdit = (data) => {
  dialog.open(dynamicComponent, {
    props: {
      header: "Editar Academia",
      ...sharedModalProps,
    },
    data,
  });
};

const showAcademyModalToCreate = () => {
  dialog.open(dynamicComponent, {
    props: {
      header: "Crear Academia",
      ...sharedModalProps,
    },
  });
};

const academies = ref([
  {
    name: "Chois Do",
    instructor: "Eli Urdaneta",
  },
  {
    name: "Chois Kwan Do",
    instructor: "Ivan Suarez",
  },
  {
    name: "Moo Sool Kwan",
    instructor: "Leonel Araujo",
  },
]);

const filters = ref({
  global: { value: null, matchMode: FilterMatchMode.CONTAINS },
  name: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
  instructor: { value: null, matchMode: FilterMatchMode.CONTAINS },
});
</script>
