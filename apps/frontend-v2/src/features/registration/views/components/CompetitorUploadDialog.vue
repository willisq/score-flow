<script setup lang="ts">
import { ref, inject } from "vue";
import { useToast } from "primevue/usetoast";
import { CompetitorService } from "../../services/CompetitorService";

const dialogRef = inject<any>("dialogRef");
const toast = useToast();

const file = ref<File | null>(null);
const uploading = ref(false);

function onFileSelect(event: { files: File[] }): void {
  file.value = event.files[0] ?? null;
}

async function onUpload(): Promise<void> {
  if (!file.value) return;

  uploading.value = true;
  try {
    const results = await CompetitorService.uploadExcel(file.value);
    toast.add({
      severity: "success",
      summary: "Éxito",
      detail: `${results.length} competidores registrados.`,
      life: 3000,
    });
    dialogRef?.value?.close();
  } catch {
    toast.add({
      severity: "error",
      summary: "Error",
      detail: "No se pudo procesar el archivo.",
      life: 5000,
    });
  } finally {
    uploading.value = false;
  }
}

async function downloadTemplate(): Promise<void> {
  try {
    const blob = await CompetitorService.downloadTemplate();
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "plantilla_competidores.xlsx";
    link.click();
    window.URL.revokeObjectURL(url);
  } catch {
    toast.add({
      severity: "error",
      summary: "Error",
      detail: "No se pudo descargar la plantilla.",
      life: 5000,
    });
  }
}
</script>

<template>
  <div class="flex flex-col gap-4 p-2">
    <div class="flex flex-col gap-2">
      <p class="text-surface-500 dark:text-surface-400 text-sm">
        Suba un archivo Excel (.xlsx) con los datos de los competidores.
      </p>
      <Button
        label="Descargar Plantilla"
        icon="pi pi-download"
        severity="secondary"
        text
        @click="downloadTemplate"
      />
    </div>

    <FileUpload
      mode="basic"
      accept=".xlsx,.xls"
      :maxFileSize="5000000"
      chooseLabel="Seleccionar Archivo"
      :auto="false"
      @select="onFileSelect"
    />

    <div v-if="file" class="text-sm text-surface-600 dark:text-surface-300">
      <i class="pi pi-file mr-1"></i> {{ file.name }}
    </div>

    <Button
      label="Subir y Registrar"
      icon="pi pi-upload"
      :loading="uploading"
      :disabled="!file"
      @click="onUpload"
    />
  </div>
</template>
