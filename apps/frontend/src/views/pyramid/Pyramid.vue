<template>
  <div class="grid">
    <div class="col-12">
      <div class="card" style="overflow-x: auto">
        <div class="mb-6">
          <AppTitle title="Piramides" />
        </div>
        <Accordion value="0">
          <AccordionPanel
            v-for="piramid in piramids"
            :key="piramid.details.id"
            :value="piramid.details.id"
          >
            <AccordionHeader
              >{{ piramid.details.initial_age }} -
              {{ piramid.details.final_age }} Años
              {{ piramid.details.modality }}
              <template
                v-for="(description, index) in piramid.details.ranks"
                :index="index"
              >
                <Tag :value="description" /> </template
            ></AccordionHeader>
            <AccordionContent>
              <TournamentBracket v-model="piramid.rounds" />
            </AccordionContent>
          </AccordionPanel>
        </Accordion>
      </div>
    </div>
  </div>
</template>
<script setup>
import { onMounted, ref } from "vue";
import { PyramidService } from "@/service/PyramidService";
import TournamentBracket from "@/views/pyramid/components/TournamentBracket.vue";

const piramids = ref({});
onMounted(async () => {
  const piramidsData = await PyramidService.findPyramid();

  piramids.value = piramidsData;
});
</script>
