<script setup lang="ts">
defineProps<{
  name?: string;
  academy?: string;
  rankName?: string;
  weight?: number;
  isWinner?: boolean;
  isBye?: boolean;
  showDelete?: boolean;
  showMove?: boolean;
}>();

defineEmits<{
  (e: "delete"): void;
  (e: "move"): void;
}>();
</script>

<template>
  <div
    class="competitor-card flex flex-col items-start px-3 border-b border-surface-300 dark:border-surface-700 last:border-0 relative bg-surface-0 dark:bg-surface-800 group"
    :class="{ 'bg-primary-50 dark:bg-primary-900/20': isWinner }">
    <div class="flex justify-between w-full items-center h-1/2 pt-1">
      <span class="font-bold text-xs text-surface-900 dark:text-surface-100 uppercase" :title="name">{{ name }}</span>
      <div class="flex gap-1 no-print">
        <button v-if="showMove && name !== '---' && name !== 'BYE'" @click.stop="$emit('move')"
          class="p-1 hover:text-primary-500 transition-colors text-surface-400 opacity-0 group-hover:opacity-100 focus:opacity-100"
          title="Mover competidor de pirámide">
          <i class="pi pi-arrows-h text-xs"></i>
        </button>
        <button v-if="showDelete && name !== '---' && name !== 'BYE'" @click.stop="$emit('delete')"
          class="p-1 hover:text-red-500 transition-colors text-surface-400 opacity-0 group-hover:opacity-100 focus:opacity-100"
          title="Eliminar competidor">
          <i class="pi pi-trash text-xs"></i>
        </button>
      </div>
    </div>
    <div class="flex justify-between w-full text-[10px] text-surface-500 h-1/2 pb-1 items-start">
      <span class="italic pr-2" :title="academy">{{ academy || " " }}</span>
      <span v-if="rankName || weight" class="whitespace-nowrap italic opacity-70">
        {{ rankName }} {{ weight ? `(${weight}kg)` : '' }}
      </span>
    </div>
  </div>
</template>

<style scoped>
.competitor-card {
  min-width: 150px;
  max-width: 250px;
  width: 200px;
  height: 60px;
  justify-content: center;
}
</style>
