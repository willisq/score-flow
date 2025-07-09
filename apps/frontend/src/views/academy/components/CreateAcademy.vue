<template></template>

<script setup>
import { inject } from "vue";

const dialogRef = inject("dialogRef");

const closeDialog = () => {
  dialogRef.value.close();
};
</script>
