<template>
  <div class="grid">
    <div class="col-12">
      <div class="card" style="overflow-x: auto">
        <div class="mb-6">
          <span class="text-4xl">Piramides</span>
        </div>

        <div class="card !bg-gray-100">
          <!-- <Form> -->
          <!-- <InputNumber placeholder="Edad"></InputNumber>
          <MultiSelect placeholder="Sexo"></MultiSelect>
          <MultiSelect placeholder="Rango"></MultiSelect>
          <Select placeholder="Modalidad"></Select>
          <div class="flex items-center gap-2">
            <Checkbox v-model="pizza" inputId="ingredient1" name="pizza" value="Cheese" />
            <label for="ingredient1"> Cond. Especial </label>
          </div> -->

          <!-- </Form> -->
        </div>
        <Accordion value="0">
          <AccordionPanel v-for="piramid in piramids" :key="piramid.details.id" :value="piramid">
            <AccordionHeader>{{ piramid.details.initial_age }} - {{ piramid.details.final_age  }} Años {{ piramid.details.modality }} <template v-for="description, index in piramid.details.ranks" :index="index">
              <Tag :value="description"/>
            </template></AccordionHeader>
            <AccordionContent>
              <TournamentBracket  v-model="piramid.rounds" />
            </AccordionContent>
          </AccordionPanel>
        </Accordion>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted } from "vue";
import TournamentBracket from "@/views/pyramid/components/TournamentBracket.vue";

import { PyramidService } from "@/service/PyramidService";

const pairs = ref();
const piramids = ref({})
onMounted(async () => {
  const piramidsData = await PyramidService.findPyramid();

  piramids.value = piramidsData;
})
</script>
