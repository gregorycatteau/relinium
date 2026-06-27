<script setup lang="ts">
const ouvert = ref(false)

const actions = ['Profil', 'Préférences', 'Sécurité', 'Déconnexion']
</script>

<template>
  <div class="relative">
    <button
      class="inline-flex h-8 items-center gap-1 rounded-md px-1.5 text-slate-700 transition outline-none hover:bg-slate-50 focus-visible:ring-2 focus-visible:ring-cyan-700 focus-visible:ring-offset-2"
      :aria-expanded="ouvert"
      aria-haspopup="menu"
      aria-label="Menu utilisateur"
      title="Menu utilisateur"
      type="button"
      @click="ouvert = !ouvert"
    >
      <span class="inline-flex h-8 w-8 items-center justify-center rounded-full bg-cyan-950 text-xs font-bold text-white">GC</span>
      <svg aria-hidden="true" class="hidden h-3.5 w-3.5 text-slate-500 sm:block" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M5.23 7.21a.75.75 0 0 1 1.06.02L10 11.17l3.71-3.94a.75.75 0 1 1 1.08 1.04l-4.25 4.5a.75.75 0 0 1-1.08 0l-4.25-4.5a.75.75 0 0 1 .02-1.06Z" clip-rule="evenodd" />
      </svg>
    </button>

    <div v-if="ouvert" class="absolute right-0 top-10 z-50 w-44 overflow-hidden rounded-lg border border-slate-200 bg-white py-1 shadow-lg" role="menu">
      <button
        v-for="action in actions"
        :key="action"
        class="block w-full px-3 py-2 text-left text-sm text-slate-700 outline-none hover:bg-slate-50 focus-visible:bg-slate-50"
        role="menuitem"
        type="button"
      >
        {{ action }}
      </button>
    </div>
  </div>
</template>
