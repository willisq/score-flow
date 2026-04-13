<script setup lang="ts">
import { useLayout } from "@/layout/composables/useLayout";

const { toggleMenu, toggleDarkMode, isDarkTheme } = useLayout();
</script>

<template>
  <div class="layout-topbar">
    <div class="layout-topbar-logo-container">
      <button class="layout-menu-button layout-topbar-action" @click="toggleMenu">
        <i class="pi pi-bars"></i>
      </button>
      <router-link to="/" class="layout-topbar-logo">
        <span class="text-xl font-bold">ScoreFlow</span>
      </router-link>
    </div>

    <div class="layout-topbar-actions">
      <div class="layout-config-menu">
        <button type="button" class="layout-topbar-action" @click="toggleDarkMode">
          <i :class="['pi', isDarkTheme ? 'pi-moon' : 'pi-sun']"></i>
        </button>
      </div>
    </div>
  </div>
</template>
