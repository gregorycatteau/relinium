<script setup lang="ts">
const emit = defineEmits<{
  close: []
}>()

const sourceSelectionnee = ref<string | null>(null)

const sources = [
  {
    nom: 'Ordinateur local',
    description: 'Dossier présent sur cette machine',
    statut: 'Prototype'
  },
  {
    nom: 'Dossier réseau / NAS',
    description: 'Partage SMB, NFS ou dossier d’entreprise',
    statut: 'À connecter'
  },
  {
    nom: 'Serveur / VPS',
    description: 'Source distante par agent ou connexion sécurisée',
    statut: 'Prévu'
  },
  {
    nom: 'Cloud / GED',
    description: 'SharePoint, Google Drive, Nextcloud ou outil métier',
    statut: 'Prévu'
  }
]
</script>

<template>
  <section class="rounded-3xl border border-cyan-100 bg-white p-5 shadow-sm ring-1 ring-slate-200 md:p-6" aria-labelledby="source-setup-title">
    <div class="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
      <div>
        <p class="text-sm font-semibold uppercase tracking-[0.16em] text-cyan-800">Charger mes données</p>
        <h2 id="source-setup-title" class="mt-2 text-2xl font-semibold text-slate-950">Indiquer les sources à observer</h2>
        <p class="mt-2 max-w-3xl text-slate-600">
          Relinium ne copie pas vos fichiers. Il référence les sources, calcule des empreintes et conserve une trace vérifiable des observations.
        </p>
      </div>
      <button
        class="inline-flex h-9 items-center justify-center rounded-lg bg-slate-50 px-3 text-sm font-semibold text-slate-700 ring-1 ring-slate-200 transition hover:bg-slate-100 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-cyan-700 focus-visible:ring-offset-2"
        type="button"
        @click="emit('close')"
      >
        Fermer
      </button>
    </div>

    <div class="mt-5 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
      <article v-for="source in sources" :key="source.nom" class="rounded-2xl bg-slate-50 p-4 ring-1 ring-slate-200">
        <div class="flex min-h-[128px] flex-col justify-between gap-4">
          <div>
            <div class="flex items-start justify-between gap-3">
              <h3 class="text-base font-semibold text-slate-950">{{ source.nom }}</h3>
              <span class="shrink-0 rounded-full bg-white px-2.5 py-1 text-xs font-semibold text-slate-700 ring-1 ring-slate-200">
                {{ source.statut }}
              </span>
            </div>
            <p class="mt-2 text-sm leading-6 text-slate-600">{{ source.description }}</p>
          </div>
          <button
            class="inline-flex h-9 w-fit items-center justify-center rounded-lg bg-white px-3 text-sm font-semibold text-slate-800 ring-1 ring-slate-200 transition hover:bg-slate-100 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-cyan-700 focus-visible:ring-offset-2"
            type="button"
            @click="sourceSelectionnee = source.nom"
          >
            Préparer
          </button>
        </div>
      </article>
    </div>

    <div v-if="sourceSelectionnee" class="mt-5 rounded-2xl bg-slate-950 p-4 text-white">
      <p class="font-semibold">{{ sourceSelectionnee }} préparé côté interface</p>
      <p class="mt-1 text-sm leading-6 text-slate-200">
        La connexion réelle sera branchée plus tard, avec stockage sécurisé des secrets côté backend si la source l’exige.
      </p>
    </div>

    <div class="mt-5 grid gap-3 lg:grid-cols-[1fr_1fr]">
      <div class="rounded-2xl bg-cyan-50 p-4 text-cyan-950 ring-1 ring-cyan-100">
        <h3 class="font-semibold">Mode d’observation</h3>
        <ul class="mt-3 space-y-2 text-sm leading-6">
          <li>Mode lecture seule</li>
          <li>Aucun fichier n’est importé</li>
          <li>Les identifiants ne doivent pas être saisis tant que le stockage sécurisé n’est pas activé</li>
        </ul>
      </div>
      <div class="rounded-2xl bg-amber-50 p-4 text-amber-950 ring-1 ring-amber-100">
        <h3 class="font-semibold">Identifiants sécurisés: à venir</h3>
        <p class="mt-2 text-sm leading-6">
          Les identifiants ne sont pas encore stockés dans ce prototype. La gestion des secrets devra passer par un stockage chiffré côté backend.
        </p>
        <p class="mt-2 text-sm leading-6">
          La suite devra prévoir rotation, audit d’accès et séparation opérateur/admin.
        </p>
      </div>
    </div>
  </section>
</template>
