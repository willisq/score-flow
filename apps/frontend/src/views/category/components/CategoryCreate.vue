<template>
  <Form @submit="createCategory" :resolver :initialValues>
    <div class="flex flex-col mt-6 gap-10">
      <div class="flex flex-col gap-1">
        <FloatLabel>
          <InputNumber fluid id="initialWeight" name="initialWeight" />
          <label for="initialWeight">Peso Inicial</label>
        </FloatLabel>
      </div>

      <div class="flex flex-col gap-1">
        <FloatLabel>
          <InputNumber fluid id="finalWeight" name="finalWeight" />
          <label for="finalWeight">Peso Final</label>
        </FloatLabel>
      </div>

      <div class="flex flex-col gap-1">
        <FloatLabel>
          <InputNumber fluid id="initialAge" name="initialAge" />
          <label for="initialAge">Edad Inicio</label>
        </FloatLabel>
      </div>

      <div class="flex flex-col gap-1">
        <FloatLabel>
          <InputNumber fluid id="finalAge" name="finalAge" />
          <label for="finalAge">Edad Fin</label>
        </FloatLabel>
      </div>

      <div class="flex flex-col gap-1">
        <FloatLabel>
          <InputNumber fluid id="initialHeight" name="initialHeight" />
          <label for="initialHeight">Altura Inicial</label>
        </FloatLabel>
      </div>

      <div class="flex flex-col gap-1">
        <FloatLabel>
          <InputNumber fluid id="finalHeight" name="finalHeight" />
          <label for="finalHeight">Altura Final</label>
        </FloatLabel>
      </div>

      <div class="flex flex-col gap-1">
        <FloatLabel>
          <MultiSelect
            :options="modalities"
            optionLabel="description"
            optionValue="id"
            fluid
            id="modalities"
            name="modalities"
          />
          <label for="modalities">Modalidades</label>
        </FloatLabel>
      </div>

      <div class="flex flex-col gap-1">
        <FloatLabel>
          <MultiSelect
            :options="ranks"
            optionLabel="description"
            optionValue="id"
            fluid
            id="ranks"
            name="ranks"
          />
          <label for="ranks">Rangos</label>
        </FloatLabel>
      </div>

      <div class="flex flex-col gap-1">
        <FloatLabel>
          <MultiSelect
            :options="sexes"
            optionLabel="description"
            optionValue="id"
            fluid
            id="sexes"
            name="sexes"
          />
          <label for="sexes">Sexos</label>
        </FloatLabel>
      </div>

      <div class="flex flex-row items-center gap-1">
        <ToggleSwitch name="specialCondition" inputId="specialCondition" />
        <label class="ml-2" for="specialCondition">Condicición Especial</label>
      </div>

      <div class="flex flex-row justify-end">
        <Button type="submit" label="Crear" />
      </div>
    </div>
  </Form>
</template>
<script setup>
import { Form } from "@primevue/forms";
import { yupResolver } from "@primevue/forms/resolvers/yup";
import { useToast } from "primevue/usetoast";
import { computed, inject } from "vue";
import * as yup from "yup";

import { CategoryService } from "@/service/CategoryService";

const toast = useToast();

const closeDialog = () => {
  dialogRef.value.close();
};

const dialogRef = inject("dialogRef");

const modalities = computed(() => dialogRef.value.data.modalities);
const ranks = computed(() => dialogRef.value.data.ranks);
const sexes = computed(() => dialogRef.value.data.sexes);

const resolver = yupResolver(
  yup.object({
    initialWeight: yup.number().required(),
    finalWeight: yup.number().required(),
    initialAge: yup.number().integer().required(),
    finalAge: yup.number().integer().required(),
    initialHeight: yup
      .number()
      .transform((value) => (isNaN(value) ? null : value))
      .nullable(),
    finalHeight: yup
      .number()
      .transform((value) => (isNaN(value) ? null : value))
      .nullable(),
    modalities: yup.array().of(yup.string().uuid()).required(),
    ranks: yup.array().of(yup.string().uuid()).required(),
    sexes: yup.array().of(yup.string().uuid()).required(),
    specialCondition: yup.boolean().required().default(false),
  })
);

const initialValues = {
  specialCondition: false,
};

const createCategory = async (data) => {
  const { valid, values } = data;

  if (!valid) return;

  const {
    initialWeight,
    finalWeight,
    initialAge,
    finalAge,
    initialHeight,
    finalHeight,
    modalities,
    ranks,
    sexes,
    specialCondition,
  } = values;

  const body = {
    categoryData: {
      initialAge,
      finalAge,
      initialWeight,
      finalWeight,
      initialHeight,
      finalHeight,
      specialCondition,
    },
    modalities,
    ranks,
    sexes,
  };

  await CategoryService.create([body]);

  toast.add({
    severity: "info",
    summary: "Categoria creada con exito",
    life: 4000,
  });
  closeDialog();
};
</script>
