<script setup lang="ts">
type AuthStatus = {
  authenticated: boolean
  mode: string
  oidcConfigured: boolean
  providerConfigured: boolean
  providerName: string
  devAuthEnabled: boolean
  user?: { displayName: string } | null
  currentOrganization?: { name: string } | null
}

const { graphql } = useGraphqlRequest()

const authReq = useAsyncData('auth-status-page', () => graphql<{ authStatus: AuthStatus }>(`
  query AuthStatusPage {
    authStatus {
      authenticated
      mode
      oidcConfigured
      providerConfigured
      providerName
      devAuthEnabled
      user { displayName }
      currentOrganization { name }
    }
  }
`))

const status = computed(() => authReq.data.value?.authStatus)
</script>

<template>
  <section class="w-full bg-slate-50 px-4 py-8 sm:px-6 lg:px-8">
    <div class="mx-auto max-w-3xl">
      <h1 class="text-3xl font-semibold text-slate-950">Connexion à Relinium</h1>
      <p class="mt-3 text-slate-700">
        Relinium utilise l’identité de votre organisation. Vos mots de passe professionnels ne sont pas stockés ici.
      </p>

      <div class="mt-6 rounded-lg border border-slate-200 bg-white p-5">
        <p v-if="authReq.pending.value" class="text-sm text-slate-600">Vérification de l’état d’authentification.</p>
        <div v-else-if="status?.authenticated" class="space-y-2">
          <p class="font-semibold text-emerald-800">Session active.</p>
          <p class="text-sm text-slate-600">{{ status.user?.displayName }} · {{ status.currentOrganization?.name || 'Organisation non sélectionnée' }}</p>
          <NuxtLink class="inline-flex h-9 items-center justify-center rounded-md bg-cyan-950 px-3 text-sm font-semibold text-white" to="/profil">Ouvrir le profil</NuxtLink>
        </div>
        <div v-else class="space-y-4">
          <div class="rounded-md bg-amber-50 p-3 text-sm text-amber-900 ring-1 ring-amber-200">
            <p v-if="status?.mode === 'oidc' && !status?.providerConfigured">OIDC est sélectionné mais le provider d’organisation n’est pas encore configuré.</p>
            <p v-else-if="status?.mode === 'dev' && !status?.devAuthEnabled">Le mode développement est sélectionné mais l’identité dev explicite est désactivée.</p>
            <p v-else-if="status?.mode === 'oidc'">Connexion organisation préparée pour {{ status.providerName || 'le provider configuré' }}.</p>
            <p v-else>La connexion OIDC sera activée après configuration du provider d’organisation.</p>
          </div>
          <div class="flex flex-wrap gap-2">
            <button class="inline-flex h-9 cursor-not-allowed items-center justify-center rounded-md bg-slate-200 px-3 text-sm font-semibold text-slate-500" type="button" disabled>
              Connexion organisation
            </button>
            <NuxtLink class="inline-flex h-9 items-center justify-center rounded-md bg-white px-3 text-sm font-semibold text-slate-700 ring-1 ring-slate-200" to="/demande-acces">Demander un accès</NuxtLink>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
