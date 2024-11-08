import { createApp } from "vue";

// Vuetify
import 'vuetify/styles'
import { createVuetify } from "vuetify";
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
// import 'material-design-icons-iconfont/dist/material-design-icons.css';


import App from "./App.vue";
import router from "./router";
import store from "./store";
import "./assets/css/main.css";

const vuetify = createVuetify({
    components,
    directives,
})

createApp(App).use(store).use(router).use(vuetify).mount("#app");
