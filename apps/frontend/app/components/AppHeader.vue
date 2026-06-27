<script setup lang="ts">
const menuOuvert = ref(false)

const route = useRoute()

watch(
  () => route.fullPath,
  () => {
    menuOuvert.value = false
  }
)
</script>

<template>
  <header class="sticky top-0 z-40 w-full border-b border-slate-200 bg-white/95 backdrop-blur">
    <div class="mx-auto flex max-w-7xl items-center gap-3 px-4 py-3 sm:px-6 lg:px-8">
      <NuxtLink class="min-w-0 shrink-0" to="/" aria-label="Accueil Relinium">
        <span class="block text-base font-bold tracking-normal text-slate-950">Relinium</span>
        <span class="block text-xs font-semibold text-cyan-800">Cockpit de preuve</span>
      </NuxtLink>

      <div class="hidden min-w-0 flex-1 justify-center lg:flex">
        <AppNav />
      </div>

      <div class="ml-auto flex min-w-0 shrink-0 items-center gap-2">
        <ApiStatusBadge />
        <div class="hidden md:block">
          <AuthStatus />
        </div>
        <button
          class="inline-flex h-10 w-10 items-center justify-center rounded-full bg-slate-50 text-slate-800 ring-1 ring-slate-200 lg:hidden"
          :aria-expanded="menuOuvert"
          aria-controls="app-mobile-nav"
          aria-label="Ouvrir la navigation"
          type="button"
          @click="menuOuvert = !menuOuvert"
        >
          <span class="text-lg leading-none">{{ menuOuvert ? '×' : '☰' }}</span>
        </button>
      </div>
    </div>

    <div v-show="menuOuvert" id="app-mobile-nav" class="border-t border-slate-200 bg-white px-4 py-3 lg:hidden">
      <div class="mb-3 md:hidden">
        <AuthStatus />
      </div>
      <AppNav />
    </div>
  </header>
</template>
