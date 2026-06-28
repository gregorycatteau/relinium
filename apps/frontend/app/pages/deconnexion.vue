<script setup lang="ts">
const { graphql } = useGraphqlRequest()
const erreur = ref('')

onMounted(async () => {
  try {
    await graphql('mutation Logout { logout { authenticated mode } }')
    await navigateTo('/connexion')
  } catch (error) {
    erreur.value = error instanceof Error ? error.message : 'Déconnexion impossible.'
  }
})
</script>

<template>
  <section class="w-full bg-slate-50 px-4 py-8 sm:px-6 lg:px-8">
    <div class="mx-auto max-w-3xl rounded-lg border border-slate-200 bg-white p-5">
      <h1 class="text-2xl font-semibold text-slate-950">Déconnexion</h1>
      <p class="mt-2 text-slate-600">Fermeture de la session Relinium.</p>
      <p v-if="erreur" class="mt-4 rounded-md bg-red-50 p-3 text-sm text-red-800 ring-1 ring-red-200">{{ erreur }}</p>
    </div>
  </section>
</template>
