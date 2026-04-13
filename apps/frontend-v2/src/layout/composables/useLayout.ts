import { computed, reactive } from "vue";

interface LayoutConfig {
  preset: string;
  primary: string;
  surface: string | null;
  darkTheme: boolean;
  menuMode: string;
}

interface LayoutState {
  staticMenuDesktopInactive: boolean;
  overlayMenuActive: boolean;
  profileSidebarVisible: boolean;
  configSidebarVisible: boolean;
  staticMenuMobileActive: boolean;
  menuHoverActive: boolean;
  activeMenuItem: string | null;
}

const layoutConfig = reactive<LayoutConfig>({
  preset: "Aura",
  primary: "emerald",
  surface: null,
  darkTheme: false,
  menuMode: "static",
});

const layoutState = reactive<LayoutState>({
  staticMenuDesktopInactive: false,
  overlayMenuActive: false,
  profileSidebarVisible: false,
  configSidebarVisible: false,
  staticMenuMobileActive: false,
  menuHoverActive: false,
  activeMenuItem: null,
});

export function useLayout() {
  const setActiveMenuItem = (item: { value?: string } | string): void => {
    layoutState.activeMenuItem = typeof item === "string" ? item : (item.value ?? null);
  };

  const toggleDarkMode = (): void => {
    const toggle = () => {
      layoutConfig.darkTheme = !layoutConfig.darkTheme;
      document.documentElement.classList.toggle("app-dark");
    };

    if (document.startViewTransition) {
      document.startViewTransition(toggle);
    } else {
      toggle();
    }
  };

  const toggleMenu = (): void => {
    if (layoutConfig.menuMode === "overlay") {
      layoutState.overlayMenuActive = !layoutState.overlayMenuActive;
    }

    if (window.innerWidth > 991) {
      layoutState.staticMenuDesktopInactive = !layoutState.staticMenuDesktopInactive;
    } else {
      layoutState.staticMenuMobileActive = !layoutState.staticMenuMobileActive;
    }
  };

  const isSidebarActive = computed(
    () => layoutState.overlayMenuActive || layoutState.staticMenuMobileActive,
  );

  const isDarkTheme = computed(() => layoutConfig.darkTheme);

  return {
    layoutConfig,
    layoutState,
    toggleMenu,
    isSidebarActive,
    isDarkTheme,
    setActiveMenuItem,
    toggleDarkMode,
  };
}
