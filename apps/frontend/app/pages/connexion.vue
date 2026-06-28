<script setup lang="ts">
const {
  pending,
  error,
  isAuthenticated,
  displayName,
  mode,
  providerConfigured,
  providerName,
  devAuthEnabled,
  currentOrganization
} = useAuthStatus()
</script>

<template>
  <section class="w-full bg-slate-50 px-4 py-8 sm:px-6 lg:px-8">
    <div class="mx-auto max-w-3xl">
      <h1 class="text-3xl font-semibold text-slate-950">Connexion à Relinium</h1>
      <p class="mt-3 max-w-2xl text-slate-700">
        Relinium utilise l’identité de votre organisation. Vos mots de passe professionnels ne sont pas stockés ici.
      </p>

      <div class="mt-6 rounded-lg border border-slate-200 bg-white p-5">
        <p v-if="pending" class="text-sm text-slate-600">Vérification de l’état d’authentification.</p>

        <div v-else-if="isAuthenticated" class="space-y-3">
          <div>
            <p class="font-semibold text-emerald-800">Session active.</p>
            <p class="mt-1 text-sm text-slate-600">{{ displayName }} · {{ currentOrganization?.name || 'Organisation non sélectionnée' }}</p>
          </div>
          <div class="flex flex-wrap gap-2">
            <NuxtLink class="inline-flex h-9 items-center justify-center rounded-md bg-cyan-950 px-3 text-sm font-semibold text-white" to="/profil">Ouvrir le profil</NuxtLink>
            <NuxtLink class="inline-flex h-9 items-center justify-center rounded-md bg-white px-3 text-sm font-semibold text-slate-700 ring-1 ring-slate-200" to="/">Retour au tableau de bord</NuxtLink>
          </div>
        </div>

        <div v-else class="space-y-4">
          <div v-if="error" class="rounded-md bg-amber-50 p-3 text-sm text-amber-900 ring-1 ring-amber-200">
            État auth indisponible. La connexion organisation ne peut pas être confirmée pour cet environnement.
          </div>
          <div v-else-if="mode === 'dev' && devAuthEnabled" class="rounded-md bg-slate-50 p-3 text-sm text-slate-700 ring-1 ring-slate-200">
            <p class="font-semibold text-slate-950">Mode développement local</p>
            <p class="mt-1">Cette identité locale sert au développement et ne correspond pas à une connexion production.</p>
          </div>
          <div v-else class="rounded-md bg-amber-50 p-3 text-sm text-amber-900 ring-1 ring-amber-200">
            <p v-if="mode === 'oidc' && providerConfigured">Connexion organisation préparée pour {{ providerName || 'le provider configuré' }}.</p>
            <p v-else>Connexion organisation non configurée dans cet environnement.</p>
          </div>

          <div class="flex flex-wrap gap-2">
            <button
              class="inline-flex h-10 items-center justify-center rounded-md bg-cyan-950 px-4 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:bg-slate-200 disabled:text-slate-500"
              type="button"
              :disabled="!providerConfigured"
            >
              Continuer avec l’identité de l’organisation
            </button>
            <NuxtLink class="inline-flex h-10 items-center justify-center rounded-md bg-white px-4 text-sm font-semibold text-slate-700 ring-1 ring-slate-200 hover:bg-slate-50" to="/demande-acces">Demander un accès</NuxtLink>
            <NuxtLink class="inline-flex h-10 items-center justify-center rounded-md px-2 text-sm font-semibold text-slate-600 hover:text-slate-950" to="/">Retour au tableau de bord</NuxtLink>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
