<template>
  <div class="mb-6">
    <span class="text-4xl">{{ title }}</span>
  </div>
</template>
<script setup>
const props = defineProps({
  title: {
    type: String,
    required: true,
  },
});
</script>
