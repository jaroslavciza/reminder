import { defineStore } from 'pinia';
import { ref, computed } from 'vue'

export const useUserStore = defineStore('user', () => {
    const isDarkMode = ref(null);
    const logged_user = ref(null);

    const accessToken = ref(localStorage.getItem('accessToken') || null);  // Načteme token z localstorage(kvuli persistenci pri refresh), pokud existuje
    const isLogged = computed(() => !!accessToken.value);  // Kontrola, zda je uživatel přihlášený

    // Inicializace režimu podle systému
    const initializeTheme = () => {
      const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      isDarkMode.value = systemPrefersDark;

      //při změně nastavení systému, přepne režim v aplikaci
      window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        if (isDarkMode.value === null) {
            isDarkMode.value = e.matches;
        }
      });

      updateThemeClass();
    };

    const toggleDarkMode = () => {
        isDarkMode.value = !isDarkMode.value;
        updateThemeClass();
    };

    const updateThemeClass = () => {
        if (isDarkMode.value) {
          document.body.setAttribute('data-bs-theme', 'dark');
        } else {
          document.body.setAttribute('data-bs-theme', 'light');
        }
    };  
      
    const setAccessToken = (token) => {
        accessToken.value = token;
        localStorage.setItem('accessToken', token);  // Uložíme do localStorage
    }; 

    const logout = () => {
        accessToken.value = null;
        localStorage.removeItem('accessToken');  // Smažeme z localStorage
      };      

    return { isDarkMode, initializeTheme, toggleDarkMode, isLogged, setAccessToken, logout, logged_user, accessToken}
});
