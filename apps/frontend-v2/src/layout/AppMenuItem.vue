<script setup lang="ts">
import { useLayout } from "@/layout/composables/useLayout";
import { onBeforeMount, ref, watch } from "vue";
import { useRoute } from "vue-router";

export interface MenuItem {
  label?: string;
  icon?: string;
  to?: string;
  url?: string;
  command?: (payload: { originalEvent: Event; item: MenuItem }) => void;
  items?: MenuItem[];
  class?: string;
  target?: string;
  visible?: boolean;
  disabled?: boolean;
  separator?: boolean;
}

const route = useRoute();
const { layoutState, setActiveMenuItem, toggleMenu } = useLayout();

const props = withDefaults(
  defineProps<{
    item: MenuItem;
    index: number;
    root?: boolean;
    parentItemKey?: string | null;
  }>(),
  {
    root: true,
    parentItemKey: null,
  },
);

const isActiveMenu = ref(false);
const itemKey = ref<string>("");

onBeforeMount(() => {
  itemKey.value = props.parentItemKey
    ? `${props.parentItemKey}-${props.index}`
    : String(props.index);

  const activeItem = layoutState.activeMenuItem;
  isActiveMenu.value =
    activeItem === itemKey.value || (activeItem ? activeItem.startsWith(`${itemKey.value}-`) : false);
});

watch(
  () => layoutState.activeMenuItem,
  (newVal) => {
    if (newVal) {
      isActiveMenu.value =
        newVal === itemKey.value || newVal.startsWith(`${itemKey.value}-`);
    } else {
      isActiveMenu.value = false;
    }
  },
);

function itemClick(event: Event, item: MenuItem): void {
  if (item.disabled) {
    event.preventDefault();
    return;
  }

  if (
    (item.to || item.url) &&
    (layoutState.staticMenuMobileActive || layoutState.overlayMenuActive)
  ) {
    toggleMenu();
  }

  if (item.command) {
    item.command({ originalEvent: event, item });
  }

  const foundItemKey = item.items
    ? isActiveMenu.value
      ? props.parentItemKey ?? ""
      : itemKey.value
    : itemKey.value;

  setActiveMenuItem(foundItemKey);
}

function checkActiveRoute(item: MenuItem): boolean {
  return route.path === item.to;
}
</script>

<template>
  <li :class="{ 'layout-root-menuitem': root, 'active-menuitem': isActiveMenu }">
    <div v-if="root && item.visible !== false" class="layout-menuitem-root-text">
      {{ item.label }}
    </div>
    <a
      v-if="(!item.to || item.items) && item.visible !== false"
      :href="item.url"
      :class="item.class"
      :target="item.target"
      tabindex="0"
      @click="itemClick($event, item)"
    >
      <i :class="item.icon" class="layout-menuitem-icon"></i>
      <span class="layout-menuitem-text">{{ item.label }}</span>
      <i v-if="item.items" class="pi pi-fw pi-angle-down layout-submenu-toggler"></i>
    </a>
    <router-link
      v-if="item.to && !item.items && item.visible !== false"
      :to="item.to"
      :class="[item.class, { 'active-route': checkActiveRoute(item) }]"
      tabindex="0"
      @click="itemClick($event, item)"
    >
      <i :class="item.icon" class="layout-menuitem-icon"></i>
      <span class="layout-menuitem-text">{{ item.label }}</span>
      <i v-if="item.items" class="pi pi-fw pi-angle-down layout-submenu-toggler"></i>
    </router-link>
    <Transition v-if="item.items && item.visible !== false" name="layout-submenu">
      <ul v-show="root ? true : isActiveMenu" class="layout-submenu">
        <AppMenuItem
          v-for="(child, i) in item.items"
          :key="i"
          :index="i"
          :item="child"
          :parent-item-key="itemKey"
          :root="false"
        />
      </ul>
    </Transition>
  </li>
</template>

<style lang="scss" scoped></style>
