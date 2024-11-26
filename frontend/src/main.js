import { createApp } from "vue";
import "@/assets/css/tailwind.css";
import "@/style.css"
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import * as ElementPlusIconsVue from "@element-plus/icons-vue"
import router from "@/router";
import App from "@/App.vue";

const app = createApp(App);

for(const [key, component] of Object.entries(ElementPlusIconsVue)){
    app.component(key, component)
}
app.use(router);
app.use(ElementPlus)
app.mount("#app");
// createApp(App).mount('#app')
