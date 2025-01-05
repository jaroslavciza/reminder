<script setup>
    import { RouterLink } from 'vue-router';
</script>

<template>
  <div class="notFound">
    <i class="bi bi-exclamation-triangle display-3 text-warning"></i>
    <h3>Chyba 404 - nenalezeno</h3>
    <p>Tato stránka neexistuje</p>
    <RouterLink to="/">Zpět na úvodní stránku</RouterLink>
    </div>
</template>

<style scoped>
 .notFound {
    /* class="text-center flex flex-col justify-center items-center h-96" */
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    /* text-align: center; */
    min-height: calc(100svh - var(--topHeight));
 }
</style>