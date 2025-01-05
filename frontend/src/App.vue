<script setup>
    import { RouterLink, RouterView, useRouter } from 'vue-router'

    import { onMounted } from 'vue';

    import { useUserStore } from './stores/user';
    const userStore = useUserStore();

    const router = useRouter();

    import DarkModeSwitcher from './components/DarkModeSwitcher.vue';

    const logout = () => {
        userStore.removeAccessToken();
        //router.push('/login'); // redirect na login stranku
        router.push('/');
    };

    onMounted(() => {
        userStore.initializeTheme();
    });  
</script>

<template>
    <header>
        <nav>
            <RouterLink to="/">Reminder</RouterLink>
            <RouterLink to="/documents">Dokumenty</RouterLink>
            <RouterLink to="/users" v-if="userStore.isLogged">Uživatelé</RouterLink>
        </nav>        

        <div class="header-right">
            <!-- <div>Přihlášen: {{ userStore.isLogged }}</div> -->
            <RouterLink to="/login" class="btn btn-outline-primary" v-if="!userStore.isLogged">Přihlásit</RouterLink>
            <button class="btn btn-outline-primary" @click="logout()" v-if="userStore.isLogged">Odhlásit</button>
            <DarkModeSwitcher />
        </div>
    </header>
    <div class="main">
        <RouterView />    
    </div>
</template>

<style>
    :root {
        --topHeight: 60px;
        
    }

    body, html, #app {
        min-width: 100svw;
        min-height: 100svh;
        /* padding: 0 2rem 0 2rem; */
    }
    #app {
        
    }

    header {
        height: var(--topHeight);
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 2rem 0 2rem;
        background-color: var(--bs-secondary-bg);
    }

    .header-right {
        display: flex;
        gap: 15px;
        align-items: center;
    }

    .main {
        padding: 0 2rem 0 2rem;
        /* min-height: calc(100svh - var(--topHeight)); */
    }

    nav {
        display: flex;
        gap:15px;
    }   
    
    a {
        text-decoration: none;
        /* color: var(--bs-primary); */
    }
</style>
