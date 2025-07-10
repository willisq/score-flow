<template>
  <Form @submit="createAcademy" :resolver>
    <div class="flex flex-col mt-6 gap-10">
      <div class="flex flex-col gap-1">
        <FloatLabel>
          <InputText fluid id="academyName" name="name" />
          <label for="academyName">Nombre Academia</label>
        </FloatLabel>
      </div>

      <div class="flex flex-col gap-1">
        <FloatLabel>
          <InputText fluid id="username" name="firstname" />
          <label for="username">Nombre Inst.</label>
        </FloatLabel>
      </div>

      <div class="flex flex-col gap-1">
        <FloatLabel>
          <InputText fluid id="instructorLastname" name="lastname" />
          <label for="instructorLastname">Apellido Inst.</label>
        </FloatLabel>
      </div>

      <Button type="submit" label="Crear" />
    </div>
  </Form>
</template>

<script setup>
import { inject } from "vue";

import { Form } from "@primevue/forms";
import { yupResolver } from '@primevue/forms/resolvers/yup';
import * as yup from "yup";

import { AcademyService } from "@/service/AcademyService";
const dialogRef = inject("dialogRef");

const resolver = yupResolver(yup.object({
  name: yup.string().required(),
  firstname: yup.string().required(),
  lastname: yup.string().required(),
}));

const closeDialog = () => {
  dialogRef.value.close();
};

const createAcademy = async (data) => {
  const { valid, values } = data;

  if (!valid) return;

  const { name, firstname, lastname } = values;

  const academy = {
    name,
    instructor: {
      firstname,
      lastname,
    },
  }

  await AcademyService.createAcademy(academy);

  closeDialog();
};
</script>
