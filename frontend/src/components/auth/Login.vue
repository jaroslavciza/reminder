<script setup>
    import { ref } from 'vue';
    import { RouterLink, useRouter } from 'vue-router';
    const router = useRouter();

    import { useToast } from "vue-toastification";
    const toast = useToast()

    import Users from '../Users.vue';

    import { useUserStore } from '../../stores/user';
    const userStore = useUserStore();    

    const email = ref('');
    const password = ref('');

    const submit = async (event) => {
        event.preventDefault();
        userStore.logout();

        const formData = new FormData();
        formData.append("username", email.value);
        formData.append("password", password.value);

        try {
            //https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/#oauth2passwordrequestform
            //kvůli OAuth2 se musi odeslat data jako "username" a "password" z formu
            //dale se muze poslat scope 
            //  users:read or users:write are common examples.
            //  instagram_basic is used by Facebook / Instagram.
            //  https://www.googleapis.com/auth/drive is used by Google.
            
            const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;
            const response = await fetch(apiBaseUrl + '/login', {
                method: 'POST',
                body: formData,
            });

            
            if (!response.ok) {
                if (response.status == 401) {
                    toast.error("Neplatné přihlašovací údaje.");
                    throw new Error("Neplatné přihlašovací údaje."); //funguje i jako return
                } 
                if (response.status == 403) {
                    toast.error("Uživatel je zablokován.");
                    throw new Error("Uživatel je zablokován."); 
                }
                toast.error("Chyba při přihlašování.");
                throw new Error('Chyba při přihlašování.');
            }
            
            const data = await response.json();
            if (data.access_token) {
                userStore.setAccessToken(data.access_token);
                toast.success("Přihlášení proběhlo úspěšně.");
                router.go(-1); //vrátí se na předchozí stránku před přihlášením
            } else {
                toast.error("Neplatné příhlášení.");
                console.log ("Neplatné příhlášení.");
            }
        } catch (error) {
            console.error('Chyba:', error.message);
        }
    }
</script>

<template>
    <Users v-if="userStore.isLogged"/>
    <main>
        <div class="loginBox">
            <h1>Přihlášení</h1>
            <form class="loginForm" @submit="submit">
                <div>
                    <input type="email" id="username" v-model="email" class="form-control" placeholder="E-mail" required>
                </div>
                <div>
                    <input type="password" v-model="password" class="form-control" placeholder="Heslo" required>
                </div>
                <div class="options">
                    <a href="#">Zapomenuté heslo?</a>
                </div>
                <button class="btn btn-primary" type="submit">Přihlásit se</button>
                <p>
                    Nemáte účet? <RouterLink to="/register">Registrovat se</RouterLink>
                </p>
            </form>
        </div>
    </main>
</template>

<style scoped>
    main {   
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: calc(100svh - var(--topHeight));
    }

    .loginBox {
        width: 300px;
        background-color: var(--bs-tertiary-bg);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-radius: 10px;
        border: 1px solid var(--bs-border-color-translucent);
        text-align: center;
        padding: 1.5rem;        
    }

    .loginForm {
        padding-top: 1.5rem;;
        display: flex;
        gap: 15px;
        flex-direction: column;
    }

    .options {
        text-align: end;
        margin-top: -0.8rem;
        margin-bottom: 0.5rem;;
    }
</style>
