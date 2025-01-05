// import './assets/main.css'
import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'



const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')

// environment proměnná pro URL na API (produkční vs develop prostředí)
app.config.globalProperties.$apiBaseUrl = import.meta.env.VITE_API_BASE_URL;
