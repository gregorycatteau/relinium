<script setup lang="ts">
const recherche = ref('')
</script>

<template>
  <section class="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm md:p-6" aria-labelledby="data-search-title">
    <div class="flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
      <div>
        <p class="text-sm font-semibold uppercase tracking-[0.16em] text-cyan-800">Recherche</p>
        <h2 id="data-search-title" class="mt-2 text-2xl font-semibold text-slate-950">Rechercher des données</h2>
        <p class="mt-2 max-w-3xl text-slate-600">
          Recherche locale à venir. Les sources doivent d’abord être chargées.
        </p>
      </div>
      <span class="w-fit rounded-full bg-slate-50 px-3 py-1 text-sm font-semibold text-slate-700 ring-1 ring-slate-200">
        Prototype
      </span>
    </div>

    <label class="mt-5 block">
      <span class="sr-only">Rechercher dans les données observées</span>
      <input
        v-model="recherche"
        class="h-11 w-full rounded-xl border border-slate-200 bg-slate-50 px-4 text-base text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-cyan-700 focus:bg-white focus:ring-2 focus:ring-cyan-100"
        placeholder="Rechercher un fichier, un chemin, un hash ou un événement…"
        type="search"
      >
    </label>

    <div class="mt-4 rounded-2xl bg-slate-50 p-4 text-slate-600 ring-1 ring-slate-200">
      <p class="font-semibold text-slate-800">La recherche sera disponible après chargement ou indexation des sources.</p>
      <p class="mt-1 text-sm leading-6">
        Aucun appel API n’est effectué depuis ce champ dans cette version.
      </p>
    </div>
  </section>
</template>
