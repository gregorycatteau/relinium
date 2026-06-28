<script setup lang="ts">
const emit = defineEmits<{
  close: []
}>()

type SourceType = 'LOCAL_FOLDER' | 'NETWORK_SHARE' | 'SERVER' | 'CLOUD_GED' | 'OTHER'
type SourceStatus = 'DRAFT' | 'READY' | 'OBSERVED' | 'ERROR' | 'DISABLED'

type DataSource = {
  id: string
  label: string
  sourceType: SourceType
  status: SourceStatus
  locatorRef: string
  locatorHash: string
  readOnly: boolean
  includeHidden: boolean
  followSymlinks: boolean
  exclusions: string[]
  notesRedacted: string
  createdAt: string
  updatedAt: string
}

const { apiBase, graphql: graphqlRequest } = useGraphqlRequest()

const typeOptions: Array<{ value: SourceType, nom: string, description: string, exemple: string, statut: string }> = [
  {
    value: 'LOCAL_FOLDER',
    nom: 'Ordinateur local',
    description: 'Dossier présent sur cette machine',
    exemple: '/home/equipe/documents',
    statut: 'Disponible'
  },
  {
    value: 'NETWORK_SHARE',
    nom: 'Dossier réseau / NAS',
    description: 'Partage SMB, NFS ou dossier d’entreprise',
    exemple: '//nas/comptabilite',
    statut: 'Disponible'
  },
  {
    value: 'SERVER',
    nom: 'Serveur / VPS',
    description: 'Source distante par agent ou connexion sécurisée',
    exemple: 'serveur-documents-prod',
    statut: 'Préparé'
  },
  {
    value: 'CLOUD_GED',
    nom: 'Cloud / GED',
    description: 'SharePoint, Google Drive, Nextcloud ou outil métier',
    exemple: 'Espace GED direction',
    statut: 'Préparé'
  }
]

const statuts: Record<SourceStatus, string> = {
  DRAFT: 'Brouillon',
  READY: 'Prête',
  OBSERVED: 'Observée',
  ERROR: 'Erreur',
  DISABLED: 'Désactivée'
}

const typeLabels: Record<SourceType, string> = {
  LOCAL_FOLDER: 'Ordinateur local',
  NETWORK_SHARE: 'Dossier réseau / NAS',
  SERVER: 'Serveur / VPS',
  CLOUD_GED: 'Cloud / GED',
  OTHER: 'Autre source'
}

const sourceSelectionnee = ref<SourceType>('LOCAL_FOLDER')
const label = ref('')
const locatorRef = ref('')
const exclusionsText = ref('')
const includeHidden = ref(true)
const notesRedacted = ref('')
const mutationEnCours = ref(false)
const message = ref('')
const erreur = ref('')

const dataSourcesReq = useAsyncData(
  'source-registry-data-sources',
  () => graphqlRequest<{ dataSources: DataSource[] }>(`
    query DataSources {
      dataSources {
        id
        label
        sourceType
        status
        locatorRef
        locatorHash
        readOnly
        includeHidden
        followSymlinks
        exclusions
        notesRedacted
        createdAt
        updatedAt
      }
    }
  `),
  {
    default: () => ({ dataSources: [] })
  }
)

const sourcesDeclarees = computed(() => dataSourcesReq.data.value?.dataSources ?? [])
const chargement = computed(() => dataSourcesReq.pending.value)
const backendIndisponible = computed(() => Boolean(dataSourcesReq.error.value))

function preparerSource(type: SourceType): void {
  sourceSelectionnee.value = type
  const option = typeOptions.find((item) => item.value === type)
  if (!label.value && option) label.value = option.nom
  if (!locatorRef.value && option) locatorRef.value = option.exemple
  message.value = ''
  erreur.value = ''
}

function exclusions(): string[] {
  return exclusionsText.value
    .split('\n')
    .map((item) => item.trim())
    .filter(Boolean)
}

function statutClasse(statut: SourceStatus): string {
  if (statut === 'READY') return 'bg-emerald-50 text-emerald-800 ring-emerald-200'
  if (statut === 'OBSERVED') return 'bg-sky-50 text-sky-800 ring-sky-200'
  if (statut === 'ERROR') return 'bg-red-50 text-red-800 ring-red-200'
  if (statut === 'DISABLED') return 'bg-slate-100 text-slate-500 ring-slate-200'
  return 'bg-amber-50 text-amber-900 ring-amber-200'
}

function peutMarquerPrete(source: DataSource): boolean {
  return source.status === 'DRAFT' && Boolean(source.label && source.sourceType)
}

async function creerSource(): Promise<void> {
  mutationEnCours.value = true
  message.value = ''
  erreur.value = ''
  try {
    await graphqlRequest<{ createDataSource: DataSource }>(
      `
        mutation CreateDataSource($input: CreateDataSourceInput!) {
          createDataSource(input: $input) {
            id
            label
            sourceType
            status
          }
        }
      `,
      {
        input: {
          label: label.value,
          sourceType: sourceSelectionnee.value,
          locatorRef: locatorRef.value,
          includeHidden: includeHidden.value,
          exclusions: exclusions(),
          notesRedacted: notesRedacted.value
        }
      }
    )
    label.value = ''
    locatorRef.value = ''
    exclusionsText.value = ''
    notesRedacted.value = ''
    includeHidden.value = true
    message.value = 'Source déclarée en brouillon.'
    await dataSourcesReq.refresh()
  } catch (error) {
    erreur.value = error instanceof Error ? error.message : 'Création impossible.'
  } finally {
    mutationEnCours.value = false
  }
}

async function marquerPrete(source: DataSource): Promise<void> {
  mutationEnCours.value = true
  message.value = ''
  erreur.value = ''
  try {
    await graphqlRequest<{ markDataSourceReady: DataSource }>(
      `
        mutation MarkDataSourceReady($id: String!) {
          markDataSourceReady(id: $id) {
            id
            status
          }
        }
      `,
      { id: source.id }
    )
    message.value = 'Source marquée prête. Aucun scan n’a été lancé.'
    await dataSourcesReq.refresh()
  } catch (error) {
    erreur.value = error instanceof Error ? error.message : 'Mise à jour impossible.'
  } finally {
    mutationEnCours.value = false
  }
}
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
      <article v-for="source in typeOptions" :key="source.value" class="rounded-2xl bg-slate-50 p-4 ring-1 ring-slate-200">
        <div class="flex min-h-[150px] flex-col justify-between gap-4">
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
            @click="preparerSource(source.value)"
          >
            Préparer
          </button>
        </div>
      </article>
    </div>

    <div class="mt-5 rounded-2xl bg-amber-50 p-4 text-amber-950 ring-1 ring-amber-100">
      <p class="font-semibold">Ne saisissez aucun mot de passe ni token dans ce champ.</p>
      <p class="mt-1 text-sm leading-6">
        Les identifiants ne sont pas stockés dans cette version. La gestion des secrets devra passer par un stockage chiffré côté backend.
      </p>
    </div>

    <form class="mt-5 grid gap-4 rounded-2xl bg-slate-50 p-4 ring-1 ring-slate-200 lg:grid-cols-2" @submit.prevent="creerSource">
      <label class="block">
        <span class="text-sm font-semibold text-slate-700">Nom de la source</span>
        <input v-model="label" class="mt-1 h-10 w-full rounded-lg border border-slate-200 bg-white px-3 text-sm outline-none focus:border-cyan-700 focus:ring-2 focus:ring-cyan-100" placeholder="Ex. Dossier comptabilité" required>
      </label>

      <label class="block">
        <span class="text-sm font-semibold text-slate-700">Type</span>
        <select v-model="sourceSelectionnee" class="mt-1 h-10 w-full rounded-lg border border-slate-200 bg-white px-3 text-sm outline-none focus:border-cyan-700 focus:ring-2 focus:ring-cyan-100">
          <option v-for="source in typeOptions" :key="source.value" :value="source.value">{{ source.nom }}</option>
          <option value="OTHER">Autre source</option>
        </select>
      </label>

      <label class="block lg:col-span-2">
        <span class="text-sm font-semibold text-slate-700">Référence, chemin ou description non secrète</span>
        <input v-model="locatorRef" class="mt-1 h-10 w-full rounded-lg border border-slate-200 bg-white px-3 text-sm outline-none focus:border-cyan-700 focus:ring-2 focus:ring-cyan-100" placeholder="Ex. /srv/partage, //nas/service, Espace GED direction">
      </label>

      <label class="block">
        <span class="text-sm font-semibold text-slate-700">Exclusions</span>
        <textarea v-model="exclusionsText" class="mt-1 min-h-24 w-full rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm outline-none focus:border-cyan-700 focus:ring-2 focus:ring-cyan-100" placeholder="Un motif par ligne, ex. cache/ ou *.tmp" />
      </label>

      <label class="block">
        <span class="text-sm font-semibold text-slate-700">Note interne</span>
        <textarea v-model="notesRedacted" class="mt-1 min-h-24 w-full rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm outline-none focus:border-cyan-700 focus:ring-2 focus:ring-cyan-100" placeholder="Contexte non sensible pour reconnaître la source." />
      </label>

      <div class="flex flex-col gap-3 lg:col-span-2">
        <label class="inline-flex items-center gap-2 text-sm font-semibold text-slate-700">
          <input v-model="includeHidden" class="h-4 w-4 rounded border-slate-300 text-cyan-800 focus:ring-cyan-700" type="checkbox">
          Inclure les fichiers cachés
        </label>
        <p class="text-sm leading-6 text-slate-600">Mode lecture seule obligatoire. Les liens symboliques ne sont pas suivis en v0.1.</p>
        <button class="inline-flex h-10 w-fit items-center justify-center rounded-lg bg-cyan-950 px-4 text-sm font-semibold text-white shadow-sm transition hover:bg-cyan-900 disabled:cursor-not-allowed disabled:opacity-60" :disabled="mutationEnCours" type="submit">
          Créer la source
        </button>
      </div>
    </form>

    <p v-if="message" class="mt-4 rounded-2xl bg-emerald-50 p-4 text-sm font-semibold text-emerald-800 ring-1 ring-emerald-100">{{ message }}</p>
    <p v-if="erreur" class="mt-4 rounded-2xl bg-red-50 p-4 text-sm font-semibold text-red-800 ring-1 ring-red-100">{{ erreur }}</p>

    <div class="mt-5">
      <div class="flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h3 class="text-xl font-semibold text-slate-950">Sources déclarées</h3>
          <p class="mt-1 text-sm text-slate-600">Aucun scan n’est lancé automatiquement depuis ce registre.</p>
        </div>
        <button class="w-fit rounded-lg bg-white px-3 py-2 text-sm font-semibold text-slate-700 ring-1 ring-slate-200 transition hover:bg-slate-50" type="button" @click="dataSourcesReq.refresh()">
          Actualiser
        </button>
      </div>

      <p v-if="chargement" class="mt-4 rounded-2xl bg-slate-50 p-4 text-slate-600 ring-1 ring-slate-200">Chargement des sources déclarées…</p>
      <p v-else-if="backendIndisponible" class="mt-4 rounded-2xl bg-red-50 p-4 text-red-900 ring-1 ring-red-100">
        Registre des sources indisponible. Vérifiez que le backend Django et GraphQL sont lancés sur {{ apiBase }}.
      </p>
      <p v-else-if="sourcesDeclarees.length === 0" class="mt-4 rounded-2xl bg-slate-50 p-4 text-slate-600 ring-1 ring-slate-200">
        Aucune source déclarée. Commencez par ajouter un dossier local ou une source réseau.
      </p>

      <div v-else class="mt-4 grid gap-3 lg:grid-cols-2">
        <article v-for="source in sourcesDeclarees" :key="source.id" class="rounded-2xl bg-white p-4 ring-1 ring-slate-200">
          <div class="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
            <div>
              <h4 class="font-semibold text-slate-950">{{ source.label }}</h4>
              <p class="mt-1 text-sm text-slate-600">{{ typeLabels[source.sourceType] }}</p>
            </div>
            <span class="w-fit rounded-full px-3 py-1 text-sm font-semibold ring-1" :class="statutClasse(source.status)">
              {{ statuts[source.status] }}
            </span>
          </div>
          <dl class="mt-4 space-y-2 text-sm">
            <div>
              <dt class="font-semibold text-slate-500">Référence</dt>
              <dd class="mt-1 break-all text-slate-700">{{ source.locatorRef || 'Non renseignée' }}</dd>
            </div>
            <div>
              <dt class="font-semibold text-slate-500">Empreinte</dt>
              <dd class="mt-1 font-mono text-slate-700">{{ source.locatorHash ? `${source.locatorHash.slice(0, 12)}…` : 'Non disponible' }}</dd>
            </div>
          </dl>
          <div class="mt-4 flex flex-wrap gap-2 text-xs font-semibold text-slate-600">
            <span class="rounded-full bg-slate-50 px-2.5 py-1 ring-1 ring-slate-200">Lecture seule</span>
            <span class="rounded-full bg-slate-50 px-2.5 py-1 ring-1 ring-slate-200">{{ source.includeHidden ? 'Fichiers cachés inclus' : 'Fichiers cachés ignorés' }}</span>
            <span class="rounded-full bg-slate-50 px-2.5 py-1 ring-1 ring-slate-200">Liens symboliques ignorés</span>
          </div>
          <button v-if="peutMarquerPrete(source)" class="mt-4 rounded-lg bg-slate-950 px-3 py-2 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-60" :disabled="mutationEnCours" type="button" @click="marquerPrete(source)">
            Marquer prête
          </button>
        </article>
      </div>
    </div>

    <div class="mt-5 grid gap-3 lg:grid-cols-[1fr_1fr]">
      <div class="rounded-2xl bg-cyan-50 p-4 text-cyan-950 ring-1 ring-cyan-100">
        <h3 class="font-semibold">Mode d’observation</h3>
        <ul class="mt-3 space-y-2 text-sm leading-6">
          <li>Mode lecture seule</li>
          <li>Aucun fichier n’est importé</li>
          <li>Aucun identifiant ne doit être saisi dans ce prototype</li>
        </ul>
      </div>
      <div class="rounded-2xl bg-slate-50 p-4 text-slate-700 ring-1 ring-slate-200">
        <h3 class="font-semibold text-slate-950">Scanner Go: étape suivante</h3>
        <p class="mt-2 text-sm leading-6">
          Commande future préparée: relinium-cartography-scan --root &lt;source&gt; --mode presence --out &lt;snapshot.ndjson&gt;
        </p>
      </div>
    </div>
  </section>
</template>
