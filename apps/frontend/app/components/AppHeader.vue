<script setup lang="ts">
const menuOuvert = ref(false)

const route = useRoute()
const { isAuthenticated, displayName, currentOrganization } = useAuthStatus()

watch(
  () => route.fullPath,
  () => {
    menuOuvert.value = false
  }
)
</script>

<template>
  <header class="sticky top-0 z-40 w-screen max-w-full overflow-x-hidden border-b border-slate-200 bg-white/95 backdrop-blur">
    <div class="mx-auto flex h-[55px] w-full max-w-7xl items-center gap-2 px-3 sm:gap-4 sm:px-6 md:h-[63px] lg:px-8">
      <NuxtLink class="inline-flex min-w-0 shrink-0 items-center gap-2 outline-none focus-visible:ring-2 focus-visible:ring-cyan-700 focus-visible:ring-offset-2" to="/" aria-label="Accueil Relinium">
        <span class="inline-flex h-8 w-8 items-center justify-center rounded-lg bg-cyan-950 text-sm font-bold text-white">R</span>
        <span class="hidden text-[18px] font-bold leading-none tracking-normal text-slate-950 sm:inline">Relinium</span>
      </NuxtLink>

      <div class="hidden min-w-0 flex-1 items-center justify-center md:flex">
        <AppNav />
      </div>

      <div class="ml-auto flex w-[132px] min-w-0 shrink-0 items-center justify-end gap-1 md:w-auto">
        <button class="hidden h-8 w-8 items-center justify-center rounded-md text-slate-600 transition outline-none hover:bg-slate-50 hover:text-slate-950 focus-visible:ring-2 focus-visible:ring-cyan-700 focus-visible:ring-offset-2 md:inline-flex" aria-label="Rechercher" type="button">
          <svg aria-hidden="true" class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="7" />
            <path d="m20 20-3.5-3.5" />
          </svg>
        </button>
        <div class="hidden md:block">
          <ApiStatusBadge />
        </div>
        <button
          class="inline-flex h-8 w-8 shrink-0 items-center justify-center rounded-md text-slate-700 transition outline-none hover:bg-slate-50 focus-visible:ring-2 focus-visible:ring-cyan-700 focus-visible:ring-offset-2 md:hidden"
          :aria-expanded="menuOuvert"
          aria-controls="app-mobile-nav"
          aria-label="Ouvrir la navigation"
          type="button"
          @click="menuOuvert = !menuOuvert"
        >
          <svg v-if="!menuOuvert" aria-hidden="true" class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round">
            <path d="M4 7h16M4 12h16M4 17h16" />
          </svg>
          <svg v-else aria-hidden="true" class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round">
            <path d="M6 6l12 12M18 6 6 18" />
          </svg>
        </button>
        <div class="shrink-0">
          <AuthStatus />
        </div>
      </div>
    </div>

    <div v-show="menuOuvert" id="app-mobile-nav" class="border-t border-slate-200 bg-white px-4 py-3 md:hidden">
      <AppNav />
      <div class="mt-3 border-t border-slate-100 pt-3">
        <div v-if="isAuthenticated" class="space-y-1">
          <div class="px-3 pb-2">
            <p class="truncate text-sm font-semibold text-slate-950">{{ displayName }}</p>
            <p class="truncate text-xs text-slate-500">{{ currentOrganization?.name || 'Organisation non sélectionnée' }}</p>
          </div>
          <NuxtLink class="block rounded-md px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50" to="/profil">Mon profil</NuxtLink>
          <NuxtLink class="block rounded-md px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50" to="/securite">Sécurité</NuxtLink>
          <NuxtLink class="block rounded-md px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50" to="/organisation">Organisation</NuxtLink>
          <NuxtLink class="block rounded-md px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50" to="/deconnexion">Déconnexion</NuxtLink>
        </div>
        <div v-else class="space-y-1">
          <NuxtLink class="block rounded-md px-3 py-2 text-sm font-semibold text-slate-800 hover:bg-slate-50" to="/connexion">Connexion</NuxtLink>
          <NuxtLink class="block rounded-md px-3 py-2 text-sm font-medium text-slate-600 hover:bg-slate-50" to="/demande-acces">Demander un accès</NuxtLink>
        </div>
      </div>
    </div>
  </header>
</template>
