<script setup>
    import { onMounted } from 'vue';
    import { RouterLink, RouterView, useRouter } from 'vue-router'
    const router = useRouter();

    import { useToast } from "vue-toastification";
    const toast = useToast()

    import { useUserStore } from './stores/user';
    const userStore = useUserStore();

    import DarkModeSwitcher from './components/DarkModeSwitcher.vue';

    //const logged_user = ref(null);

    const logout = () => {
        userStore.logout();
        toast.success("Odhlášení proběhlo úspěšně.")
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
            <RouterLink to="/documents" v-if="userStore.isLogged">Dokumenty</RouterLink>
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
        /* display: flex;
        flex-direction: column; */
        
    }
    
    header {
        height: var(--topHeight);
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 1.2rem 0 1.2rem;
        background-color: var(--bs-secondary-bg);
    }
    
    h1 {
        padding-bottom: 0.5rem;
    }
    .header-right {
        display: flex;
        gap: 15px;
        align-items: center;
    }
    
    .main {
        padding: 0.7rem 1.2rem 0 1.2rem;
        max-height: calc(100svh - var(--topHeight));
        max-width: 100svw;
        /* max-height: 100svw; */
        overflow-x: auto;
        overflow-y: auto;
    }

    nav {
        display: flex;
        gap:15px;
    }   
    
    a {
        text-decoration: none;
        /* color: var(--bs-primary); */
    }

    /* .top-right {
        margin-top: 30px;
    } */
</style>
