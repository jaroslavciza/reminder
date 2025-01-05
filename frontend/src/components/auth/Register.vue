<script setup>
    import { ref } from 'vue';

    import { useRouter } from 'vue-router'
    const router = useRouter();

    import { useToast } from "vue-toastification";
    const toast = useToast()
    
    import { useUserStore } from '../../stores/user';
    const userStore = useUserStore();
    
    const email = ref('');
    const password = ref('');
    const firstName = ref('');
    const lastName = ref('');
    
    const submit = async (event) => {
        event.preventDefault();

        const formData = {};
        formData["email"] = email.value;
        formData["password"] = password.value;
        formData["firstName"] = firstName.value;
        formData["lastName"] = lastName.value;

        try {
            const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;

            const response = await fetch(apiBaseUrl + '/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },                
                body: JSON.stringify(formData),
            });
          
            if (response.ok) {
                const data = await response.json();
                if (data.access_token) {
                    userStore.setAccessToken(data.access_token);
                    toast.success("Registrace proběhla úspěšně.");
                    router.push('/');
                }
            } else {
                toast.error("Neznámá chyba při registraci.");
                console.error("Neznámá chyba při registraci.");
            }
            // const data = await response.json();
            // //console.log(data)

            // if (data.access_token) {
            //     userStore.setAccessToken(data.access_token);
            //     router.go(-1); //vrátí se na předchozí stránku před přihlášením
            // } else {
            //     console.log ("Neplatné přihlašovací údaje.") //dodělat toast
            // }

        } catch (error) {
            console.error('Chyba:', error.message);
        }

    }
</script>

<template>
    <main>
        <div class="registerBox">
            <h1>Registrace</h1>
            <form class="registerForm" @submit="submit">
                <div>
                    <input type="email" class="form-control" v-model="email" placeholder="E-mail" required>
                </div>
                <div>
                    <input type="password" class="form-control" v-model="password" placeholder="Heslo" required>
                </div>
                <div>
                    <input type="text" class="form-control" v-model="firstName" id="firstName" placeholder="Jméno" required>
                </div>
                <div>
                    <input type="text" class="form-control" v-model="lastName" id="lastName" placeholder="Příjmení" required>
                </div>                                
                <button class="btn btn-primary mt-2"  type="submit">Registrovat se</button>
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

    .registerBox {
        width: 300px;
        height: 385px;
        /* background-color: rgba(255,255,255,0.1); */
        background-color: var(--bs-tertiary-bg);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-radius: 10px;
        border: 1px solid var(--bs-border-color-translucent);
        text-align: center;
        padding: 1.5rem;        
    }

    .registerForm {
        /* padding: 1rem 2rem 0 2rem; */
        /* max-width: 1000px; */
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
