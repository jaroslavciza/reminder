<script setup>
    import { useUserStore } from '@/stores/user';

    const userStore = useUserStore();   
</script>

<template>
    <div>
        <i class="bi" :class="userStore.isDarkMode ? 'bi-moon-stars-fill' : 'bi-sun-fill'" @click="userStore.toggleDarkMode"></i>
    </div>
</template>

<style lang="css" scoped>
    i {
        cursor: pointer;
    }
</style>