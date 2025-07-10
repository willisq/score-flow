<template>
  <div class="grid card">
    <div>
      <AppTitle title="Categorías" />
    </div>

    <DataView :value="categories" paginator :rows="5">
      <template #list="slotProps">
        <div class="flex flex-col">
          <div v-for="(item, index) in slotProps.items" :key="index">
            <div
              class="flex flex-col sm:flex-row sm:items-center justify-between p-6 gap-4"
              :class="{
                'border-t border-surface-200 dark:border-surface-700':
                  index !== 0,
              }"
            >
              <div class="flex flex-col items-start gap-1">
                <Tag :value="item.modality.name" class="mb-2"></Tag>

                <span class="text-lg font-semibold"
                  >Edades: {{ item.initial_age }} -
                  {{ item.final_age }} Años</span
                >
                <span class="text-lg font-semibold"
                  >Pesos: {{ item.initial_weight }} -
                  {{ item.final_weight }} Kg</span
                >
                <span v-if="item.initial_height" class="text-lg font-semibold"
                  >Alturas: {{ item.initial_height }} -
                  {{ item.final_height }} cm</span
                >
              </div>

              <div class="flex flex-col gap-1">
                <template
                  v-for="(rank, rankIndex) in item.ranks"
                  :key="rankIndex"
                >
                  <Tag :value="rank.description"></Tag>
                </template>
              </div>

              <div class="flex flex-col md:items-end gap-4">
                <div v-if="item.special_condition">
                  <Tag
                    value="Condición Especial"
                    class="!bg-indigo-600 !text-white"
                  />
                </div>
                <div class="flex flex-row">
                  <template
                    v-for="(sex, sexIndex) in item.sexes"
                    :index="sexIndex"
                  >
                    <div class="bg-surface-100 p-1" style="border-radius: 30px">
                      <div
                        class="bg-surface-0 flex items-center gap-2 justify-center py-1 px-2"
                        style="
                          border-radius: 30px;
                          box-shadow: 0px 1px 2px 0px rgba(0, 0, 0, 0.04),
                            0px 1px 2px 0px rgba(0, 0, 0, 0.06);
                        "
                      >
                        <i
                          :class="`pi pi-${
                            sex.abbreviation === 'M' ? 'mars' : 'venus'
                          } text-${
                            sex.abbreviation === 'M' ? 'blue' : 'pink'
                          }-500`"
                        ></i>
                      </div>
                    </div>
                  </template>
                </div>
                <div class="flex flex-row-reverse md:flex-row gap-2">
                  <!-- <Button icon="pi pi-pencil" outlined label="editar"></Button> -->
                  <Button
                    @click="showCompetitors(item)"
                    icon="pi pi-list"
                    label="Ver Competidores"
                    :disabled="item.inventoryStatus === 'OUTOFSTOCK'"
                    class="flex-auto md:flex-initial whitespace-nowrap"
                  ></Button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </template>
    </DataView>
  </div>
</template>

<script setup>
import { defineAsyncComponent, ref, onMounted } from "vue";
import { CategoryService } from "@/service/CategoryService";
import { CompetitorService } from "@/service/CompetitorService";
import AppTitle from "@/components/tags/AppTitle.vue";
import { useDialog } from "primevue/usedialog";

const dynamicComponent = defineAsyncComponent(() =>
  import("@/views/category/components/CategoryCompetitorList.vue")
);
const sharedModalProps = {
  style: {
    width: "50vw",
  },
  breakpoints: {
    "960px": "80vw",
    "640px": "90vw",
  },
  modal: true,
  dismissableMask: true,
};

const dialog = useDialog();

const categories = ref([]);

onMounted(async () => {
  categories.value = await CategoryService.getCategories();
});

const showCompetitors = async (categoryData) => {
  const { id: categoryId, ...rest } = categoryData;
  const competitorsOnCategory =
    await CompetitorService.findByCategoryAndChampionShip(categoryId);

  dialog.open(dynamicComponent, {
    props: {
      header: "Competidores En la Categoria",
      ...sharedModalProps,
    },
    data: {
      competitors: competitorsOnCategory,
      categoryData,
    },
  });
};
</script>
