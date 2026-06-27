<template>
  <div class="flex min-w-0 items-center gap-2">
    <span class="hidden rounded-full bg-cyan-50 px-2.5 py-1 text-xs font-semibold text-cyan-800 ring-1 ring-cyan-200 sm:inline-flex">
      Local
    </span>
    <button
      class="min-w-0 rounded-full bg-slate-50 px-3 py-1.5 text-sm font-semibold text-slate-700 ring-1 ring-slate-200 transition hover:bg-white"
      title="Authentification simulée pour le MVP local"
      type="button"
    >
      Opérateur local
    </button>
    <button
      class="hidden rounded-full bg-white px-3 py-1.5 text-sm font-semibold text-slate-700 ring-1 ring-slate-200 transition hover:bg-slate-50 md:inline-flex"
      type="button"
    >
      Connexion
    </button>
  </div>
</template>
