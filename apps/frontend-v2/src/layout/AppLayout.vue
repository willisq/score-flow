<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { useLayout } from "@/layout/composables/useLayout";
import AppFooter from "./AppFooter.vue";
import AppSidebar from "./AppSidebar.vue";
import AppTopbar from "./AppTopbar.vue";

const { layoutConfig, layoutState, isSidebarActive } = useLayout();

const outsideClickListener = ref<((event: MouseEvent) => void) | null>(null);

watch(isSidebarActive, (newVal) => {
  if (newVal) {
    bindOutsideClickListener();
  } else {
    unbindOutsideClickListener();
  }
});

const containerClass = computed(() => ({
  "layout-overlay": layoutConfig.menuMode === "overlay",
  "layout-static": layoutConfig.menuMode === "static",
  "layout-static-inactive":
    layoutState.staticMenuDesktopInactive && layoutConfig.menuMode === "static",
  "layout-overlay-active": layoutState.overlayMenuActive,
  "layout-mobile-active": layoutState.staticMenuMobileActive,
}));

function bindOutsideClickListener(): void {
  if (!outsideClickListener.value) {
    outsideClickListener.value = (event: MouseEvent) => {
      if (isOutsideClicked(event)) {
        layoutState.overlayMenuActive = false;
        layoutState.staticMenuMobileActive = false;
        layoutState.menuHoverActive = false;
      }
    };
    document.addEventListener("click", outsideClickListener.value);
  }
}

function unbindOutsideClickListener(): void {
  if (outsideClickListener.value) {
    document.removeEventListener("click", outsideClickListener.value);
    outsideClickListener.value = null;
  }
}

function isOutsideClicked(event: MouseEvent): boolean {
  const sidebarEl = document.querySelector(".layout-sidebar");
  const topbarEl = document.querySelector(".layout-menu-button");
  const target = event.target as Node;

  return !(
    sidebarEl?.isSameNode(target) ||
    sidebarEl?.contains(target) ||
    topbarEl?.isSameNode(target) ||
    topbarEl?.contains(target)
  );
}
</script>

<template>
  <div class="layout-wrapper" :class="containerClass">
    <AppTopbar />
    <AppSidebar />
    <div class="layout-main-container">
      <div class="layout-main">
        <router-view />
      </div>
      <AppFooter />
    </div>
    <div class="layout-mask animate-fadein"></div>
    <DynamicDialog />
  </div>
  <Toast />
</template>
