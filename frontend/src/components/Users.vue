<script setup>
    import { ref, onMounted } from 'vue';

    // import { useToast } from "vue-toastification";
    // const toast = useToast()
    
    import { useUserStore } from '../stores/user';
    const userStore = useUserStore();      

    const users = ref(null);

    const getUsers = async() => {
        try {
            const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;
            const access_token = userStore.accessToken;

            const response = await fetch(apiBaseUrl + '/users', { //BEZ KONCOVEHO LOMITKA, jinak FastAPI presmerovava na adresu bez lomitka, ale na HTTP
                headers: {
                    // Authorization: 'Bearer ' + userStore.JWTtoken 
                    Authorization: `Bearer ${access_token}`,
                }
            });
            
            if (!response.ok) {
                if (response.status == 401) {
                    //toast.error("Přihlášení vypršelo.")
                    userStore.logout();
                }
                const errorDetails = await response.text();
                throw new Error(`${errorDetails}`);
            };

            const json = await response.json();
            //console.log(json);
            users.value = json;
        } catch (error) {
            console.error(error.message);
        }
    }

    onMounted(() => {
        getUsers();
    })
</script>

<template>
    <div v-if="userStore.isLogged">
        <h1>
            Temp: Users from DB
        </h1>

        <table class="table">
            <thead>
                <tr>
                <th scope="col">Jméno</th>
                <th scope="col">Příjmení</th>
                <th scope="col">E-mail</th>
                <th scope="col">Zablokován</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="user in users">
                    <td>{{ user.firstName }}</td>
                    <td>{{ user.lastName }}</td>
                    <td>{{ user.email }}</td>
                    <td>{{ user.disabled }}</td>
                </tr>
            </tbody>
        </table>        
    </div>
</template>

<style lang="css" scoped>

</style>