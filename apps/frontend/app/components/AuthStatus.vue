<script setup lang="ts">
const menuOpen = ref(false)
const route = useRoute()
const {
  pending,
  error,
  refresh,
  isAuthenticated,
  displayName,
  initials,
  mode,
  currentOrganization
} = useAuthStatus()

const showLoading = computed(() => pending.value && !isAuthenticated.value && !error.value)
const loginTitle = computed(() => error.value ? 'Connexion organisation à configurer' : 'Connexion')

watch(
  () => route.fullPath,
  () => {
    menuOpen.value = false
    refresh()
  }
)
</script>

<template>
  <div class="relative">
    <span
      v-if="showLoading"
      class="inline-flex h-8 w-[104px] items-center justify-center rounded-md border border-slate-200 bg-white"
      aria-label="Chargement de l'état auth"
    >
      <span class="h-4 w-4 rounded-full border-2 border-slate-200 border-t-slate-500" aria-hidden="true" />
    </span>

    <NuxtLink
      v-else-if="!isAuthenticated"
      class="inline-flex h-9 max-h-9 items-center justify-center rounded-md border border-slate-200 bg-white px-3 text-sm font-semibold text-slate-800 transition outline-none hover:border-slate-300 hover:bg-slate-50 focus-visible:ring-2 focus-visible:ring-cyan-700 focus-visible:ring-offset-2"
      to="/connexion"
      :title="loginTitle"
    >
      Connexion
    </NuxtLink>

    <button
      v-else
      class="inline-flex h-9 items-center gap-1 rounded-md px-1.5 text-slate-700 transition outline-none hover:bg-slate-50 focus-visible:ring-2 focus-visible:ring-cyan-700 focus-visible:ring-offset-2"
      :aria-expanded="menuOpen"
      aria-haspopup="menu"
      aria-label="Menu utilisateur"
      title="Menu utilisateur"
      type="button"
      @click="menuOpen = !menuOpen"
    >
      <span class="inline-flex h-8 w-8 items-center justify-center rounded-full bg-cyan-950 text-xs font-bold text-white">{{ initials }}</span>
      <svg aria-hidden="true" class="hidden h-3.5 w-3.5 text-slate-500 sm:block" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M5.23 7.21a.75.75 0 0 1 1.06.02L10 11.17l3.71-3.94a.75.75 0 1 1 1.08 1.04l-4.25 4.5a.75.75 0 0 1-1.08 0l-4.25-4.5a.75.75 0 0 1 .02-1.06Z" clip-rule="evenodd" />
      </svg>
    </button>

    <div v-if="menuOpen && isAuthenticated" class="absolute right-0 top-10 z-50 w-64 overflow-hidden rounded-lg border border-slate-200 bg-white py-1 shadow-lg" role="menu">
      <div class="border-b border-slate-100 px-3 py-2">
        <p class="truncate text-sm font-semibold text-slate-950">{{ displayName }}</p>
        <p class="truncate text-xs text-slate-500">{{ currentOrganization?.name || 'Organisation non sélectionnée' }}</p>
        <p v-if="mode === 'dev'" class="mt-1 text-xs font-semibold text-amber-800">Mode développement local</p>
      </div>
      <NuxtLink class="block px-3 py-2 text-sm text-slate-700 outline-none hover:bg-slate-50 focus-visible:bg-slate-50" role="menuitem" to="/profil">Mon profil</NuxtLink>
      <NuxtLink class="block px-3 py-2 text-sm text-slate-700 outline-none hover:bg-slate-50 focus-visible:bg-slate-50" role="menuitem" to="/securite">Sécurité</NuxtLink>
      <NuxtLink class="block px-3 py-2 text-sm text-slate-700 outline-none hover:bg-slate-50 focus-visible:bg-slate-50" role="menuitem" to="/organisation">Organisation</NuxtLink>
      <NuxtLink class="block border-t border-slate-100 px-3 py-2 text-sm text-slate-700 outline-none hover:bg-slate-50 focus-visible:bg-slate-50" role="menuitem" to="/deconnexion">Déconnexion</NuxtLink>
    </div>
  </div>
</template>
