<script setup>
    import { ref, onMounted } from 'vue';

    import { useToast } from "vue-toastification";
    const toast = useToast()
    
    import { useUserStore } from '../stores/user';
    const userStore = useUserStore();      

    const users = ref(null);
    const isAddingDocument = ref(false);
    
    const document_types = ref([]); //ciselnik typu dokumentu

    const document_name = ref(null);
    const document_type = ref(null);
    const document_date_expiration = ref(null);
    document_date_expiration.value = new Date().toISOString().slice(0, 10);
    const document_notify = ref(true);

    const documents = ref(null);

    const set_default_values = () => {
        if (document_types.value.length > 0) {
            document_type.value = document_types.value[0].id;
        }         
        document_name.value = null;
        document_date_expiration.value = new Date().toISOString().slice(0, 10);
        document_notify.value = true;
        isAddingDocument.value = false;
    }

    const get_documents = async() => {
        try {
            const api_base_url = import.meta.env.VITE_API_BASE_URL;
            const access_token = userStore.accessToken;

            const response = await fetch(api_base_url + '/get_documents', { //BEZ KONCOVEHO LOMITKA, jinak FastAPI presmerovava na adresu bez lomitka, ale na HTTP
                headers: {
                    Authorization: `Bearer ${access_token}`,
                }
            });
            
            if (!response.ok) {
                if (response.status == 401) {
                    //toast.error("Přihlášení vypršelo.")
                    userStore.logout();
                }
                const errorDetails = await response.text();
                throw new Error(`Error: ${errorDetails}`);
            };

            const json = await response.json();
            //console.log(json);
            documents.value = json;
        } catch (error) {
            console.error(error.message);
        }
    }

    const get_document_types = async () => {
        try {
            const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;
            const response = await fetch(apiBaseUrl + '/document_types');
            
            if (!response.ok) {
                const errorDetails = await response.text();
                throw new Error(`Error: ${errorDetails}`);
            };

            const json = await response.json();
            document_types.value = json;

            if (document_types.value.length > 0) {
                document_type.value = document_types.value[0].id; // Nastavení prvního typu dokumentu jako výchozí hodnoty
            } 

        } catch (error) {
            console.error(error.message);
        }   
        return null;    
    }

    const submit = async (event) => {
        event.preventDefault();

        const formData = {};
        formData["document_type"] = document_type.value;
        formData["document_name"] = document_name.value;
        formData["document_date_expiration"] = document_date_expiration.value;
        formData["document_notify"] = document_notify.value;

        try {          
            const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;
            const access_token = userStore.accessToken;

            const response = await fetch(apiBaseUrl + '/add_document', {
                method: 'POST',
                body: JSON.stringify(formData),
                headers: {
                    Authorization: `Bearer ${access_token}`,
                    'Content-Type': 'application/json',
                }                
            });

            
            if (!response.ok) {
                // userStore.logout(); //doresit!!!
                if (response.status == 401) {
                    toast.error("Neplatné přihlašovací údaje.");
                    userStore.logout();
                    throw new Error("Neplatné přihlašovací údaje."); //funguje i jako return
                } 
                if (response.status == 403) {
                    toast.error("Uživatel je zablokován.");
                    throw new Error("Uživatel je zablokován."); 
                }
                toast.error("Chyba.");
                const errorDetails = await response.text();
                throw new Error(`${errorDetails}`);
            }

            //const data = await response.json();
            toast.success("Dokument uložen.")
        } catch (error) {
            console.error('Chyba:', error.message);
        }
        get_documents();
        set_default_values();
    }

    onMounted(() => {
        get_document_types();
        get_documents();
    })
</script>

<template>
    <div v-if="userStore.isLogged">
        <div class="header">
            <h1>
                Dokumenty
            </h1>
            <button type="button" class="btn btn-outline-primary" @click="isAddingDocument = !isAddingDocument">Přidat dokument</button>
        </div>
        <div class="center">
            <div v-if="isAddingDocument" class="addDocumentWrapper">
                <form class="addDocumentForm" @submit="submit">
                    <div class="mb-2">
                        <label for="document_name" class="form-label">Typ dokumentu</label>
                        <!-- <input type="text" class="form-control" v-model="document_types" placeholder="Typ" required> -->
                        <select class="form-select" v-model="document_type">
                            <option v-for="type in document_types" :value="type.id" :key="type.id">
                                {{ type.name }}
                            </option>
                        </select>
                    </div>
                    <div class="mb-2">
                        <label for="document_name" class="form-label">Název / číslo dokumentu</label>
                        <input type="text" class="form-control" v-model="document_name" id="document_name"placeholder="Název">
                    </div>
                    <div class="mb-3">
                        <label for="document_date_expiration" class="form-label">Datum expirace</label>
                        <input type="date" class="form-control" v-model="document_date_expiration" id="document_date_expiration" required>
                    </div> 
                    <div class="mb-3">
                        <input type="checkbox" class="form-check-input" v-model="document_notify" id="notify">
                        <label class="form-check-label ms-2" for="notify">Sledovat expiraci</label>
                    </div>       
                    <div class="text-center">
                        <button class="btn btn-primary mt-2"  type="submit">Přidat dokument</button>
                    </div>                                         
                </form>
            </div>
        
        </div>
        <table class="table" v-if="!isAddingDocument">
            <thead>
                <tr>
                    <th class="col-3">Název</th>
                    <th class="col-3">Typ</th>
                    <th class="col-3">Datum expirace</th>
                    <th class="col-3">Sledovat expiraci</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="document in documents">
                    <td>{{ document.name }}</td>
                    <td>{{ document.document_type }}</td>
                    <td>{{ document.date_expiration}}</td>
                    <td>{{ document.notify }}</td>
                </tr>
            </tbody>
        </table>        
    </div>
</template>

<style lang="css" scoped>
    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .center {   
        display: flex;
        justify-content: center;
        /* align-items: center; */
    }

    .addDocumentWrapper {
        width: 300px;
        background-color: var(--bs-tertiary-bg);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-radius: 10px;
        border: 1px solid var(--bs-border-color-translucent);
        padding: 1rem;    
    }
</style>