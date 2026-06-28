<script setup lang="ts">
type AuthStatus = {
  authenticated: boolean
  mode: string
  devAuthEnabled: boolean
  user?: {
    displayName: string
    avatarInitials: string
    emailRedacted: string
  } | null
  currentOrganization?: {
    name: string
  } | null
}

const ouvert = ref(false)
const route = useRoute()
const { graphql } = useGraphqlRequest()

const authReq = useAsyncData(
  'auth-status-menu',
  () => graphql<{ authStatus: AuthStatus }>(`
    query AuthStatusMenu {
      authStatus {
        authenticated
        mode
        devAuthEnabled
        user { displayName avatarInitials emailRedacted }
        currentOrganization { name }
      }
    }
  `),
  { default: () => ({ authStatus: { authenticated: false, mode: 'disabled', devAuthEnabled: false } }) }
)

const status = computed(() => authReq.data.value.authStatus)
const initials = computed(() => status.value.user?.avatarInitials || 'U')

watch(
  () => route.fullPath,
  () => {
    ouvert.value = false
    authReq.refresh()
  }
)
</script>

<template>
  <div class="relative">
    <NuxtLink
      v-if="!status.authenticated"
      class="inline-flex h-8 items-center gap-2 rounded-md px-2 text-sm font-semibold text-slate-700 transition outline-none hover:bg-slate-50 focus-visible:ring-2 focus-visible:ring-cyan-700 focus-visible:ring-offset-2"
      to="/connexion"
    >
      <span class="inline-flex h-7 w-7 items-center justify-center rounded-full bg-slate-100 text-slate-700 ring-1 ring-slate-200" aria-hidden="true">
        <svg class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
          <path d="M20 21a8 8 0 0 0-16 0" />
          <circle cx="12" cy="7" r="4" />
        </svg>
      </span>
      <span class="hidden sm:inline">Connexion</span>
    </NuxtLink>

    <button
      v-else
      class="inline-flex h-8 items-center gap-1 rounded-md px-1.5 text-slate-700 transition outline-none hover:bg-slate-50 focus-visible:ring-2 focus-visible:ring-cyan-700 focus-visible:ring-offset-2"
      :aria-expanded="ouvert"
      aria-haspopup="menu"
      aria-label="Menu utilisateur"
      title="Menu utilisateur"
      type="button"
      @click="ouvert = !ouvert"
    >
      <span class="inline-flex h-8 w-8 items-center justify-center rounded-full bg-cyan-950 text-xs font-bold text-white">{{ initials }}</span>
      <svg aria-hidden="true" class="hidden h-3.5 w-3.5 text-slate-500 sm:block" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M5.23 7.21a.75.75 0 0 1 1.06.02L10 11.17l3.71-3.94a.75.75 0 1 1 1.08 1.04l-4.25 4.5a.75.75 0 0 1-1.08 0l-4.25-4.5a.75.75 0 0 1 .02-1.06Z" clip-rule="evenodd" />
      </svg>
    </button>

    <div v-if="ouvert && status.authenticated" class="absolute right-0 top-10 z-50 w-60 overflow-hidden rounded-lg border border-slate-200 bg-white py-1 shadow-lg" role="menu">
      <div class="border-b border-slate-100 px-3 py-2">
        <p class="truncate text-sm font-semibold text-slate-950">{{ status.user?.displayName }}</p>
        <p class="truncate text-xs text-slate-500">{{ status.currentOrganization?.name || 'Organisation non sélectionnée' }}</p>
        <p v-if="status.mode === 'dev'" class="mt-1 text-xs font-semibold text-amber-800">Mode développement</p>
      </div>
      <NuxtLink class="block px-3 py-2 text-sm text-slate-700 outline-none hover:bg-slate-50 focus-visible:bg-slate-50" role="menuitem" to="/profil">Profil</NuxtLink>
      <NuxtLink class="block px-3 py-2 text-sm text-slate-700 outline-none hover:bg-slate-50 focus-visible:bg-slate-50" role="menuitem" to="/securite">Sécurité</NuxtLink>
      <NuxtLink class="block px-3 py-2 text-sm text-slate-700 outline-none hover:bg-slate-50 focus-visible:bg-slate-50" role="menuitem" to="/organisation">Organisation</NuxtLink>
      <NuxtLink class="block px-3 py-2 text-sm text-slate-700 outline-none hover:bg-slate-50 focus-visible:bg-slate-50" role="menuitem" to="/deconnexion">Déconnexion</NuxtLink>
    </div>
  </div>
</template>
