<template>
  <Form @submit="createCompetitor" :resolver :initialValues>
    <div class="flex flex-col mt-6 gap-10">
      <div class="flex flex-col gap-1">
        <FloatLabel>
          <InputText fluid id="competitorName" name="firstname" />
          <label for="firstname">Nombre</label>
        </FloatLabel>
      </div>

      <div class="flex flex-col gap-1">
        <FloatLabel>
          <InputText fluid id="competitorLastname" name="lastname" />
          <label for="lastname">Apellido</label>
        </FloatLabel>
      </div>

      <div class="flex flex-col gap-1">
        <FloatLabel>
          <Select
            :options="academies"
            optionLabel="name"
            optionValue="id"
            fluid
            id="academy"
            name="academy"
          />
          <label for="academy">Academia</label>
        </FloatLabel>
      </div>

      <div class="flex flex-col gap-1">
        <FloatLabel>
          <Select
            :options="ranks"
            optionLabel="description"
            optionValue="id"
            fluid
            id="rank"
            name="rank"
          />
          <label for="rank">Rango</label>
        </FloatLabel>
      </div>

      <div class="flex flex-col gap-1">
        <FloatLabel>
          <Select
            :options="sexes"
            optionLabel="description"
            optionValue="id"
            fluid
            id="sex"
            name="sex"
          />
          <label for="sex">Sexo</label>
        </FloatLabel>
      </div>

      <div class="flex flex-col gap-1">
        <FloatLabel>
          <MultiSelect
            :options="modalities"
            optionLabel="description"
            optionValue="id"
            fluid
            id="sex"
            name="modalities"
          />
          <label for="sex">Modalidades</label>
        </FloatLabel>
      </div>

      <div class="flex flex-col gap-1">
        <FloatLabel>
          <InputNumber fluid id="weight" name="weight" />
          <label for="weight">Peso</label>
        </FloatLabel>
      </div>

      <div class="flex flex-col gap-1">
        <FloatLabel>
          <InputNumber fluid id="height" name="height" />
          <label for="height">Altura</label>
        </FloatLabel>
      </div>

      <div class="flex flex-col gap-1">
        <FloatLabel>
          <InputNumber fluid id="age" name="age" />
          <label for="age">Edad</label>
        </FloatLabel>
      </div>

      <div class="flex flex-row items-center gap-1">
        <ToggleSwitch name="specialCondition" inputId="specialCondition" />
        <label class="ml-2" for="specialCondition">Condicición Especial</label>
      </div>

      <Button type="submit" label="Crear" />
    </div>
  </Form>
</template>

<script setup>
import { computed, inject } from "vue";

import { Form } from "@primevue/forms";
import { yupResolver } from "@primevue/forms/resolvers/yup";
import * as yup from "yup";
import { useToast } from "primevue/usetoast";

import { CompetitorService } from "@/service/CompetitorService";

const dialogRef = inject("dialogRef");

const toast = useToast();

const academies = computed(() => dialogRef.value.data.academies);
const ranks = computed(() => dialogRef.value.data.ranks);
const sexes = computed(() => dialogRef.value.data.sexes);
const modalities = computed(() => dialogRef.value.data.modalities);

const resolver = yupResolver(
  yup.object({
    firstname: yup.string().required(),
    lastname: yup.string().required(),
    rank: yup.string().uuid().required(),
    sex: yup.string().uuid().required(),
    weight: yup.number().required(),
    academy: yup.string().uuid().required(),
    height: yup
      .number()
      .transform((value) => (isNaN(value) ? null : value))
      .nullable(),
    age: yup.number().integer().required(),
    specialCondition: yup.boolean().required(),
    modalities: yup.array().of(yup.string().uuid()).required(),
  })
);

const initialValues = {
  specialCondition: false,
};

const closeDialog = () => {
  dialogRef.value.close();
};

const createCompetitor = async (data) => {
  const { valid, values } = data;

  if (!valid) return;

  const {
    firstname,
    lastname,
    rank,
    sex,
    weight,
    academy,
    height,
    age,
    modalities,
    specialCondition,
  } = values;

  const body = [
    {
      personData: { firstname, lastname },
      rank,
      academy,
      sex,
      weight,
      height,
      age,
      special_condition: specialCondition,
      championship: "25558000-df7a-49c2-a319-a11a94db4717",
      modalities,
    },
  ];

  await CompetitorService.create(body);

  toast.add({
    severity: "info",
    summary: "Competidor creado con exito",
    life: 4000,
  });
  closeDialog();
};
</script>
