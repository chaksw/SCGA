import './assets/main.css'
import axios from 'axios'
import { createApp } from 'vue'
import App from './App.vue'

// setting a default URL to response
axios.defaults.baseURL = 'httop://127.0.0.1:8000'

createApp(App).mount('#app')
