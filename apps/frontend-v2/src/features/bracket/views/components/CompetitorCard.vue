<script setup lang="ts">
defineProps<{
  name?: string;
  academy?: string;
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
    class="flex flex-col items-start px-3 py-2 border-b border-surface-200 dark:border-surface-700 last:border-0 relative bg-surface-100 dark:bg-surface-800 opacity-60 group">
    <div class="flex justify-between w-full items-center">
      <span class="font-semibold text-sm w-full break-words" :title="name">{{ name }}</span>
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
    <span class="text-xs text-surface-400 w-full break-words" :title="academy">{{ academy || "" }}</span>
  </div>
</template>
