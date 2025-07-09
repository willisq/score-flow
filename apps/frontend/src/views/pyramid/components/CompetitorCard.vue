<template>
    <div class="flex flex-col items-start">
        <span class="name font-semibold">{{
            name
        }}</span>
        <span class="text-sm">{{academy}}</span>
    </div>
</template>

<script setup>
const props = defineProps({
    name: {
        type: String,
        required: false,
        default: '---'
    },
    academy: {
        type: String,
        required: false,
        default: null
    }
})
</script>