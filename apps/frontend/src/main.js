import Aura from "@primeuix/themes/aura";
import PrimeVue from "primevue/config";
import ConfirmationService from "primevue/confirmationservice";
import DialogService from "primevue/dialogservice";
import ToastService from "primevue/toastservice";
import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";

import { es } from "primelocale/js/es.js";

import "@/assets/styles.scss";

const app = createApp(App);

app.use(router);
app.use(PrimeVue, {
  locale: es,
  theme: {
    preset: Aura,
    options: {
      darkModeSelector: ".app-dark",
    },
  },
});
app.use(ToastService);
app.use(ConfirmationService);
app.use(DialogService);

app.mount("#app");
