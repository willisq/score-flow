<script setup lang="ts">
defineProps<{
  name?: string;
  academy?: string;
  isWinner?: boolean;
  isBye?: boolean;
}>();
</script>

<template>
  <div
    class="flex flex-col items-start px-3 py-2 border-b border-surface-200 dark:border-surface-700 last:border-0 relative bg-surface-100 dark:bg-surface-800 opacity-60">
    <div class="flex justify-between w-full">
      <span class="font-semibold text-sm truncate w-full" :title="name">{{ name }}</span>
    </div>
    <span class="text-xs text-surface-400 truncate w-full" :title="academy">{{ academy || "" }}</span>
  </div>
</template>
