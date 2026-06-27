<script setup lang="ts">
import type { DocumentRecord, EventRecord, EventsPayload, EventStream, Finding, Summary, ValidationPayload } from '~/types/cockpit'
import heroBackground from '~/assets/images/relinium-hero-bg.png'

type Onglet = 'vue-ensemble' | 'evenements' | 'documents' | 'validation' | 'roadmap'

const config = useRuntimeConfig()
const apiBase = computed(() => String(config.public.apiBase || 'http://127.0.0.1:8000'))

const ongletActif = ref<Onglet>('vue-ensemble')
const evenementSelectionne = ref<string | null>(null)
const sectionDetails = ref<HTMLElement | null>(null)
const panneauSourcesOuvert = ref(false)
const rechercheVisible = ref(false)
const sectionRecherche = ref<HTMLElement | null>(null)
const heroStyle = computed(() => ({
  backgroundImage: `linear-gradient(90deg, rgba(255,255,255,0.96) 0%, rgba(255,255,255,0.9) 42%, rgba(240,248,252,0.72) 68%, rgba(235,247,252,0.58) 100%), url(${heroBackground})`
}))

const fetchJson = async <T,>(path: string): Promise<T> => {
  return await $fetch<T>(`${apiBase.value}${path}`)
}

const summaryReq = useAsyncData('summary', () => fetchJson<Summary>('/api/ssot/summary'))
const streamsReq = useAsyncData('streams', () => fetchJson<{ streams: EventStream[] }>('/api/events/streams'))
const eventsReq = useAsyncData('events', () => fetchJson<EventsPayload>('/api/events'))
const validationReq = useAsyncData('validation', () => fetchJson<ValidationPayload>('/api/validation/status'))

const chargement = computed(() => summaryReq.pending.value || streamsReq.pending.value || eventsReq.pending.value || validationReq.pending.value)
const erreurApi = computed(() => summaryReq.error.value || streamsReq.error.value || eventsReq.error.value || validationReq.error.value)

const summary = computed(() => summaryReq.data.value)
const streams = computed(() => streamsReq.data.value?.streams ?? [])
const events = computed(() => eventsReq.data.value?.events ?? [])
const documents = computed(() => eventsReq.data.value?.documents ?? [])
const validation = computed(() => validationReq.data.value)
const strictFindings = computed(() => validation.value?.strict.findings ?? [])
const baselineConnue = computed(() => validation.value?.known_findings.findings ?? [])
const baselineObsolete = computed(() => validation.value?.with_baseline.findings.filter((item) => item.code === 'BASELINE_STALE') ?? [])

const evenementsOrdonnes = computed(() => events.value.slice())
const anomaliesStrictes = computed(() => strictFindings.value)
const anomaliePrincipale = computed(() => anomaliesStrictes.value[0])

const evenementParDefaut = computed(() => {
  const eventAvecBaseline = evenementsOrdonnes.value.find((event) => event.validation?.status === 'baseline')
  return eventAvecBaseline ?? evenementsOrdonnes.value[0] ?? null
})

const evenementDetail = computed(() => {
  const cle = evenementSelectionne.value
  if (!cle) return evenementParDefaut.value
  return evenementsOrdonnes.value.find((event) => cleEvenement(event) === cle) ?? evenementParDefaut.value
})

const documentDuDetail = computed(() => {
  const event = evenementDetail.value
  if (!event?.path) return null
  return documents.value.find((doc) => doc.path === event.path) ?? null
})

const synthese = computed(() => {
  const strict = summary.value?.validation.strict_status
  const baseline = summary.value?.validation.with_baseline_status
  if (strict === 'pass') {
    return {
      ton: 'ok',
      titre: 'Socle SSOT valide.',
      texte: 'Aucune anomalie bloquante n’est détectée par le validateur minimal.'
    }
  }
  if (strict === 'failed' && baseline === 'pass') {
    return {
      ton: 'attention',
      titre: 'Socle exploitable avec baseline.',
      texte: 'Une anomalie historique est connue et maîtrisée.'
    }
  }
  return {
    ton: 'danger',
    titre: 'Intervention nécessaire.',
    texte: 'La validation avec baseline échoue ou une anomalie non maîtrisée est présente.'
  }
})

const cartesStatut = computed(() => [
  {
    titre: 'Validation stricte',
    valeur: libelleStatutValidation(summary.value?.validation.strict_status, true),
    texte: `${summary.value?.validation.strict_finding_count ?? 0} anomalie historique détectée`,
    ton: summary.value?.validation.strict_status === 'pass' ? 'ok' : 'danger'
  },
  {
    titre: 'Validation avec baseline',
    valeur: summary.value?.validation.with_baseline_status === 'pass' ? 'Socle exploitable' : 'À traiter',
    texte: `${summary.value?.validation.matched_baseline_count ?? 0} anomalie connue acceptée`,
    ton: summary.value?.validation.with_baseline_status === 'pass' ? 'ok' : 'danger'
  },
  {
    titre: 'Flux d’événements',
    valeur: `${summary.value?.counts.streams ?? 0} flux surveillé`,
    texte: 'Noyau événementiel actif',
    ton: 'info'
  },
  {
    titre: 'Événements',
    valeur: `${summary.value?.counts.events ?? 0} événements tracés`,
    texte: 'Historique append-only observé',
    ton: 'info'
  },
  {
    titre: 'Anomalies connues',
    valeur: `${summary.value?.validation.known_finding_count ?? 0} exception contrôlée`,
    texte: 'Baseline stricte par ligne brute',
    ton: 'attention'
  }
])

const onglets: Array<{ id: Onglet, label: string, aide: string }> = [
  { id: 'vue-ensemble', label: 'Vue d’ensemble', aide: 'Décision rapide' },
  { id: 'evenements', label: 'Événements', aide: 'Noyau événementiel' },
  { id: 'documents', label: 'Documents', aide: 'Artefacts référencés' },
  { id: 'validation', label: 'Validation', aide: 'Contrôles et baseline' },
  { id: 'roadmap', label: 'Feuille de route', aide: 'Progression v0.1' }
]

// Produit une clé stable pour relier une carte d’événement à son panneau de détail.
function cleEvenement(event: EventRecord): string {
  return `${event.stream_path}:${event.line}`
}

// Traduit les statuts techniques du backend en libellés lisibles pour un humain.
function libelleStatutTechnique(value?: string): string {
  const labels: Record<string, string> = {
    hash_ok: 'Hash valide',
    baseline: 'Baseline',
    anomaly: 'Anomalie',
    unchecked: 'Non vérifié',
    pass: 'Valide',
    failed: 'Échec'
  }
  return labels[value || ''] || 'Non vérifié'
}

// Traduit les types d’événements sans masquer leur identifiant technique.
function libelleKind(kind?: string): string {
  const labels: Record<string, string> = {
    schema_event: 'Schéma',
    policy_event: 'Politique',
    crypto_event: 'Crypto',
    ingestion_event: 'Ingestion',
    evidence_event: 'Preuve',
    analysis_event: 'Analyse'
  }
  return labels[kind || ''] || 'Événement'
}

// Donne une lecture métier au statut de validation global.
function libelleStatutValidation(value?: string, strict = false): string {
  if (value === 'pass') return 'Valide'
  if (value === 'failed' && strict) return 'Échec attendu'
  if (value === 'failed') return 'Échec'
  return 'Inconnu'
}

// Abrège les hashes longs tout en conservant la valeur complète dans l’attribut title.
function hashCourt(value?: string): string {
  return value ? `${value.slice(0, 12)}…${value.slice(-8)}` : 'Non disponible'
}

// Extrait un nom court exploitable à partir d’un chemin SSOT.
function nomCourt(path?: string): string {
  if (!path) return 'Document non exposé'
  const parts = path.split('/')
  return parts[parts.length - 1] || path
}

// Déduit un type documentaire simple depuis le chemin ou l’extension.
function typeDocument(doc: DocumentRecord): string {
  if (doc.path.includes('/validation/')) return 'Règle de validation'
  if (doc.path.includes('/schema/')) return 'Schéma'
  if (doc.path.includes('/policies/')) return 'Politique'
  return 'Document SSOT'
}

// Sélectionne un événement sans déclencher d’écriture serveur.
function selectionnerEvenement(event: EventRecord): void {
  evenementSelectionne.value = cleEvenement(event)
  ongletActif.value = 'evenements'
}

function ouvrirOnglet(onglet: Onglet): void {
  ongletActif.value = onglet
  nextTick(() => {
    sectionDetails.value?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  })
}

function ouvrirSources(): void {
  panneauSourcesOuvert.value = true
  rechercheVisible.value = false
  nextTick(() => {
    document.getElementById('source-setup-title')?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  })
}

function ouvrirRecherche(): void {
  rechercheVisible.value = true
  panneauSourcesOuvert.value = false
  nextTick(() => {
    sectionRecherche.value?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  })
}

// Classe visuelle centralisée pour garder une palette cohérente.
function classeTon(ton?: string): string {
  const classes: Record<string, string> = {
    ok: 'bg-emerald-50 text-emerald-800 ring-emerald-200',
    attention: 'bg-amber-50 text-amber-900 ring-amber-200',
    danger: 'bg-red-50 text-red-800 ring-red-200',
    info: 'bg-sky-50 text-sky-800 ring-sky-200'
  }
  return classes[ton || ''] || 'bg-slate-50 text-slate-700 ring-slate-200'
}

function statutVersTon(value?: string): string {
  if (value === 'hash_ok' || value === 'pass' || value === 'ok') return 'ok'
  if (value === 'baseline') return 'attention'
  if (value === 'failed' || value === 'anomaly') return 'danger'
  return 'info'
}

function statutRoadmap(status: string): string {
  const labels: Record<string, string> = {
    substantial: 'Solide',
    prototype: 'Prototype',
    stub: 'À construire',
    empty: 'À initialiser',
    partial: 'Partiel',
    'minimal validator': 'Validateur minimal',
    'first dashboard': 'Première version'
  }
  return labels[status] || status
}
</script>

<template>
  <section class="w-full max-w-full overflow-x-hidden bg-[#edf3f8] px-4 py-6 sm:px-6 lg:px-8">
    <div class="mx-auto max-w-7xl">
      <section class="-mx-4 -mt-6 mb-6 overflow-hidden border-b border-slate-200 bg-white bg-cover bg-[position:67%_center] sm:-mx-6 md:bg-[position:center_center] lg:relative lg:left-1/2 lg:w-screen lg:-translate-x-1/2" :style="heroStyle">
        <div class="mx-auto grid max-w-7xl gap-5 px-4 py-5 sm:px-6 lg:grid-cols-[minmax(0,1fr)_340px] lg:px-8 lg:py-4">
          <div class="min-w-0">
            <div>
              <div class="flex flex-wrap items-center gap-x-3 gap-y-1 text-xs font-semibold uppercase tracking-[0.14em] text-cyan-800">
                <span>Tableau de bord</span>
                <span class="inline-flex items-center gap-2 text-emerald-800">
                  <span class="h-1.5 w-1.5 rounded-full bg-emerald-500" aria-hidden="true" />
                  Données lues en local
                </span>
              </div>
              <h1 class="mt-4 max-w-3xl text-3xl font-semibold leading-tight tracking-normal text-slate-950 sm:text-4xl">
                Tableau de bord des preuves
              </h1>
              <p class="mt-3 max-w-3xl text-base leading-7 text-slate-600">
                Commencez par déclarer les sources à observer. Relinium les lit en lecture seule, calcule les empreintes utiles et vous permet ensuite de suivre les événements ou de rechercher des informations.
              </p>
              <p class="mt-3 rounded-xl bg-cyan-50 px-3 py-2 text-sm leading-5 text-cyan-950 ring-1 ring-cyan-100 lg:hidden">
                Lecture seule: Relinium observe vos fichiers sans les modifier.
              </p>
            </div>

            <div class="mt-4 flex flex-col gap-2 sm:flex-row">
              <button class="inline-flex h-10 items-center justify-center rounded-lg bg-cyan-950 px-4 text-sm font-semibold text-white shadow-sm transition hover:bg-cyan-900 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-cyan-700 focus-visible:ring-offset-2" type="button" @click="ouvrirSources">
                Charger mes données
              </button>
              <button class="inline-flex h-10 items-center justify-center rounded-lg bg-white px-4 text-sm font-semibold text-slate-800 ring-1 ring-slate-200 transition hover:bg-slate-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-cyan-700 focus-visible:ring-offset-2" type="button" @click="ouvrirOnglet('evenements')">
                Consulter les événements
              </button>
              <button class="inline-flex h-10 items-center justify-center rounded-lg bg-white px-4 text-sm font-semibold text-slate-800 ring-1 ring-slate-200 transition hover:bg-slate-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-cyan-700 focus-visible:ring-offset-2" type="button" @click="ouvrirRecherche">
                Rechercher des données
              </button>
            </div>

            <div class="mt-4 grid gap-2 sm:grid-cols-3 sm:gap-3">
              <div class="rounded-xl border border-slate-200 bg-slate-50 px-3 py-3 sm:px-4 lg:grid lg:grid-cols-[auto_1fr] lg:items-center lg:gap-x-3 lg:py-2.5">
                <p class="text-2xl font-semibold leading-none text-slate-950">{{ summary?.counts.streams ?? '—' }}</p>
                <div>
                  <p class="mt-2 text-sm font-semibold text-slate-800 lg:mt-0">{{ (summary?.counts.streams ?? 0) > 1 ? 'sources observées' : 'source observée' }}</p>
                  <p class="mt-1 text-xs leading-5 text-slate-500">Source observée</p>
                </div>
              </div>
              <div class="rounded-xl border border-slate-200 bg-slate-50 px-3 py-3 sm:px-4 lg:grid lg:grid-cols-[auto_1fr] lg:items-center lg:gap-x-3 lg:py-2.5">
                <p class="text-2xl font-semibold leading-none text-slate-950">{{ summary?.counts.events ?? '—' }}</p>
                <div>
                  <p class="mt-2 text-sm font-semibold text-slate-800 lg:mt-0">{{ (summary?.counts.events ?? 0) > 1 ? 'événements enregistrés' : 'événement enregistré' }}</p>
                  <p class="mt-1 text-xs leading-5 text-slate-500">Historique disponible</p>
                </div>
              </div>
              <div class="rounded-xl border border-slate-200 bg-slate-50 px-3 py-3 sm:px-4 lg:grid lg:grid-cols-[auto_1fr] lg:items-center lg:gap-x-3 lg:py-2.5">
                <p class="text-2xl font-semibold leading-none text-slate-950">{{ summary?.validation.known_finding_count ?? '—' }}</p>
                <div>
                  <p class="mt-2 text-sm font-semibold text-slate-800 lg:mt-0">{{ (summary?.validation.known_finding_count ?? 0) > 1 ? 'écarts connus' : 'écart connu' }}</p>
                  <p class="mt-1 text-xs leading-5 text-slate-500">Exception contrôlée</p>
                </div>
              </div>
            </div>
          </div>

          <aside class="hidden rounded-2xl border border-cyan-100 bg-cyan-50/60 p-3.5 lg:block">
            <div class="flex items-start justify-between gap-3">
              <div>
                <p class="text-sm font-semibold text-cyan-950">Comment lire ce tableau de bord</p>
                <p class="mt-1 text-xs leading-5 text-cyan-900">Lecture seule: Relinium observe vos fichiers sans les modifier.</p>
              </div>
              <span class="rounded-full bg-white px-2.5 py-1 text-xs font-semibold text-emerald-800 ring-1 ring-emerald-100">Lecture seule</span>
            </div>
            <ol class="mt-3 space-y-2">
              <li class="flex gap-3">
                <span class="mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-white text-xs font-semibold text-cyan-900 ring-1 ring-cyan-100">1</span>
                <div>
                  <p class="text-sm font-semibold text-slate-950">Vous indiquez les sources</p>
                  <p class="mt-1 text-sm leading-5 text-slate-600">Dossiers locaux, réseau, serveur ou cloud.</p>
                </div>
              </li>
              <li class="flex gap-3">
                <span class="mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-white text-xs font-semibold text-cyan-900 ring-1 ring-cyan-100">2</span>
                <div>
                  <p class="text-sm font-semibold text-slate-950">Relinium observe en lecture seule</p>
                  <p class="mt-1 text-sm leading-5 text-slate-600">Les fichiers ne sont pas copiés ni modifiés.</p>
                </div>
              </li>
              <li class="flex gap-3">
                <span class="mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-white text-xs font-semibold text-cyan-900 ring-1 ring-cyan-100">3</span>
                <div>
                  <p class="text-sm font-semibold text-slate-950">Vous exploitez les preuves</p>
                  <p class="mt-1 text-sm leading-5 text-slate-600">Événements, recherches, écarts et rapports.</p>
                </div>
              </li>
            </ol>
          </aside>
        </div>
      </section>

      <div v-if="panneauSourcesOuvert" class="mb-6">
        <SourceSetupPanel @close="panneauSourcesOuvert = false" />
      </div>

      <div v-if="rechercheVisible" ref="sectionRecherche" class="mb-6">
        <DataSearchPanel />
      </div>

      <div v-if="chargement" class="rounded-3xl bg-white p-6 text-slate-700 shadow-sm ring-1 ring-slate-200">
        Chargement du tableau de bord SSOT…
      </div>

      <div v-else-if="erreurApi" class="rounded-3xl bg-red-50 p-6 text-red-900 shadow-sm ring-1 ring-red-200">
        <h2 class="text-xl font-semibold">API indisponible</h2>
        <p class="mt-2">Le cockpit ne peut pas charger les données. Vérifie que le backend Django tourne sur {{ apiBase }}.</p>
      </div>

      <div v-else class="space-y-6">
        <section class="rounded-3xl p-5 shadow-sm ring-1 md:p-6" :class="classeTon(synthese.ton)">
          <div class="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
            <div>
              <p class="text-sm font-semibold uppercase tracking-[0.18em] opacity-80">Synthèse en 5 secondes</p>
              <h2 class="mt-2 text-2xl font-semibold">{{ synthese.titre }}</h2>
              <p class="mt-2 max-w-3xl text-base">{{ synthese.texte }}</p>
            </div>
            <div class="grid gap-2 text-sm sm:grid-cols-2 lg:min-w-[360px]">
              <button class="rounded-2xl bg-white/70 px-4 py-3 text-left font-semibold shadow-sm ring-1 ring-current/10 transition hover:bg-white" type="button" @click="ongletActif = 'validation'">
                Comprendre la validation
              </button>
              <button class="rounded-2xl bg-white/70 px-4 py-3 text-left font-semibold shadow-sm ring-1 ring-current/10 transition hover:bg-white" type="button" @click="ongletActif = 'evenements'">
                Voir les événements
              </button>
            </div>
          </div>
        </section>

        <section class="grid gap-4 md:grid-cols-2 xl:grid-cols-5">
          <article v-for="carte in cartesStatut" :key="carte.titre" class="rounded-3xl bg-white p-5 shadow-sm ring-1 ring-slate-200">
            <p class="text-sm font-semibold text-slate-500">{{ carte.titre }}</p>
            <p class="mt-3 text-2xl font-semibold leading-tight" :class="classeTon(carte.ton).split(' ')[1]">{{ carte.valeur }}</p>
            <p class="mt-2 text-base text-slate-600">{{ carte.texte }}</p>
          </article>
        </section>

        <section v-if="anomaliePrincipale" class="rounded-3xl bg-white p-5 shadow-sm ring-1 ring-amber-200 md:p-6">
          <div class="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
            <div>
              <span class="inline-flex rounded-full px-3 py-1 text-sm font-semibold ring-1" :class="classeTon('attention')">Anomalie historique</span>
              <h2 class="mt-3 text-2xl font-semibold text-slate-950">{{ anomaliePrincipale.event_id }}</h2>
              <p class="mt-2 text-slate-700">
                Cette anomalie bloque le mode strict, mais elle est acceptée par une baseline stricte liée à la ligne brute du stream.
              </p>
            </div>
            <button class="rounded-2xl bg-slate-950 px-4 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-slate-800" type="button" @click="ongletActif = 'validation'">
              Voir le détail
            </button>
          </div>
          <div class="mt-5 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
            <div class="rounded-2xl bg-amber-50 p-4 ring-1 ring-amber-100">
              <p class="text-sm font-semibold text-amber-900">Statut</p>
              <p class="mt-1 text-slate-800">Acceptée par baseline</p>
            </div>
            <div class="rounded-2xl bg-slate-50 p-4 ring-1 ring-slate-200">
              <p class="text-sm font-semibold text-slate-600">Impact</p>
              <p class="mt-1 text-slate-800">La validation stricte échoue.</p>
            </div>
            <div class="rounded-2xl bg-slate-50 p-4 ring-1 ring-slate-200">
              <p class="text-sm font-semibold text-slate-600">Raison</p>
              <p class="mt-1 text-slate-800">Hash tronqué dans un stream append-only.</p>
            </div>
            <div class="rounded-2xl bg-slate-50 p-4 ring-1 ring-slate-200">
              <p class="text-sm font-semibold text-slate-600">Action recommandée</p>
              <p class="mt-1 text-slate-800">Conserver en baseline stricte, ne pas modifier le stream.</p>
            </div>
          </div>
        </section>

        <nav ref="sectionDetails" class="sticky top-[65px] z-10 rounded-3xl border border-slate-200 bg-[#edf3f8]/95 px-3 py-3 backdrop-blur">
          <div class="flex gap-2 overflow-x-auto pb-1">
            <button
              v-for="onglet in onglets"
              :key="onglet.id"
              type="button"
              class="shrink-0 rounded-2xl px-4 py-3 text-left transition"
              :class="ongletActif === onglet.id ? 'bg-slate-950 text-white shadow-sm' : 'bg-white text-slate-700 ring-1 ring-slate-200 hover:bg-slate-50'"
              @click="ongletActif = onglet.id"
            >
              <span class="block text-sm font-semibold">{{ onglet.label }}</span>
              <span class="block text-xs opacity-70">{{ onglet.aide }}</span>
            </button>
          </div>
        </nav>

        <section v-show="ongletActif === 'vue-ensemble'" class="grid gap-6 xl:grid-cols-[1fr_380px]">
          <div class="rounded-3xl bg-white p-5 shadow-sm ring-1 ring-slate-200 md:p-6">
            <h2 class="text-2xl font-semibold">Où regarder en premier ?</h2>
            <div class="mt-5 grid gap-4 md:grid-cols-3">
              <button class="rounded-3xl bg-sky-50 p-5 text-left ring-1 ring-sky-100 transition hover:bg-sky-100" type="button" @click="ongletActif = 'validation'">
                <p class="text-lg font-semibold text-sky-900">Validation</p>
                <p class="mt-2 text-slate-700">Comprendre pourquoi le strict échoue et pourquoi la baseline reste sûre.</p>
              </button>
              <button class="rounded-3xl bg-emerald-50 p-5 text-left ring-1 ring-emerald-100 transition hover:bg-emerald-100" type="button" @click="ongletActif = 'evenements'">
                <p class="text-lg font-semibold text-emerald-900">Noyau événementiel</p>
                <p class="mt-2 text-slate-700">Voir les événements, leurs cibles et leur statut de hash.</p>
              </button>
              <button class="rounded-3xl bg-amber-50 p-5 text-left ring-1 ring-amber-100 transition hover:bg-amber-100" type="button" @click="ongletActif = 'roadmap'">
                <p class="text-lg font-semibold text-amber-900">Feuille de route</p>
                <p class="mt-2 text-slate-700">Identifier les zones solides et celles à construire.</p>
              </button>
            </div>
          </div>

          <div class="rounded-3xl bg-white p-5 shadow-sm ring-1 ring-slate-200 md:p-6">
            <h2 class="text-xl font-semibold">Flux surveillés</h2>
            <div class="mt-4 space-y-3">
              <article v-for="stream in streams" :key="stream.path" class="rounded-2xl bg-slate-50 p-4 ring-1 ring-slate-200">
                <div class="flex items-start justify-between gap-3">
                  <div>
                    <p class="font-semibold text-slate-900">{{ stream.tenant }}</p>
                    <p class="mt-1 break-all font-mono text-sm text-slate-500">{{ stream.path }}</p>
                  </div>
                  <span class="rounded-full bg-white px-3 py-1 text-sm font-semibold text-slate-700 ring-1 ring-slate-200">{{ stream.event_count }}</span>
                </div>
                <div class="mt-3 flex flex-wrap gap-2">
                  <span v-for="(count, kind) in stream.kinds" :key="kind" class="rounded-full bg-white px-3 py-1 text-sm text-slate-700 ring-1 ring-slate-200">
                    {{ libelleKind(kind) }} {{ count }}
                  </span>
                </div>
              </article>
            </div>
          </div>
        </section>

        <section v-show="ongletActif === 'evenements'" class="grid gap-6 xl:grid-cols-[1fr_420px]">
          <div class="rounded-3xl bg-white p-5 shadow-sm ring-1 ring-slate-200 md:p-6">
            <div class="flex flex-col gap-2 md:flex-row md:items-end md:justify-between">
              <div>
                <h2 class="text-2xl font-semibold">Noyau événementiel</h2>
                <p class="mt-1 text-slate-600">Événements append-only lus depuis les streams existants.</p>
              </div>
              <span class="rounded-full bg-sky-50 px-3 py-1 text-sm font-semibold text-sky-800 ring-1 ring-sky-100">{{ events.length }} événements</span>
            </div>

            <div class="mt-5 space-y-3">
              <button
                v-for="event in evenementsOrdonnes"
                :key="cleEvenement(event)"
                type="button"
                class="w-full rounded-3xl p-4 text-left shadow-sm ring-1 transition hover:-translate-y-0.5 hover:shadow-md"
                :class="cleEvenement(event) === cleEvenement(evenementDetail as EventRecord) ? 'bg-slate-950 text-white ring-slate-950' : 'bg-white ring-slate-200'"
                @click="selectionnerEvenement(event)"
              >
                <div class="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
                  <div>
                    <p class="font-mono text-sm font-semibold">{{ event.id }}</p>
                    <p class="mt-1 text-sm opacity-75">{{ libelleKind(event.kind) }} · {{ event.event_type }}</p>
                  </div>
                  <span class="w-fit rounded-full px-3 py-1 text-sm font-semibold ring-1" :class="classeTon(statutVersTon(event.validation?.status))">
                    {{ libelleStatutTechnique(event.validation?.status) }}
                  </span>
                </div>
                <div class="mt-4 grid gap-2 text-sm md:grid-cols-[1fr_180px_150px]">
                  <span class="break-all"><span class="opacity-60">Cible:</span> <span class="font-mono">{{ event.path || 'non exposée' }}</span></span>
                  <span :title="event.hash_sha256" class="font-mono"><span class="opacity-60">Hash:</span> {{ hashCourt(event.hash_sha256) }}</span>
                  <span><span class="opacity-60">Date:</span> {{ event.timestamp }}</span>
                </div>
              </button>

              <p v-if="evenementsOrdonnes.length === 0" class="rounded-2xl bg-slate-50 p-4 text-slate-600 ring-1 ring-slate-200">Aucun événement disponible.</p>
            </div>
          </div>

          <aside class="rounded-3xl bg-white p-5 shadow-sm ring-1 ring-slate-200 md:p-6 xl:sticky xl:top-28 xl:self-start">
            <h2 class="text-xl font-semibold">Détail événement</h2>
            <div v-if="evenementDetail" class="mt-5 space-y-4">
              <div>
                <p class="text-sm font-semibold text-slate-500">Identifiant</p>
                <p class="mt-1 break-all font-mono text-base font-semibold">{{ evenementDetail.id }}</p>
              </div>
              <div class="grid gap-3 sm:grid-cols-2 xl:grid-cols-1">
                <div class="rounded-2xl bg-slate-50 p-4 ring-1 ring-slate-200">
                  <p class="text-sm font-semibold text-slate-500">Type</p>
                  <p class="mt-1">{{ libelleKind(evenementDetail.kind) }} · {{ evenementDetail.event_type }}</p>
                </div>
                <div class="rounded-2xl bg-slate-50 p-4 ring-1 ring-slate-200">
                  <p class="text-sm font-semibold text-slate-500">Statut</p>
                  <p class="mt-1">{{ libelleStatutTechnique(evenementDetail.validation?.status) }}</p>
                </div>
              </div>
              <dl class="space-y-3 text-sm">
                <div>
                  <dt class="font-semibold text-slate-500">Stream</dt>
                  <dd class="mt-1 break-all font-mono">{{ evenementDetail.stream_path }}</dd>
                </div>
                <div>
                  <dt class="font-semibold text-slate-500">Ligne</dt>
                  <dd class="mt-1">{{ evenementDetail.line }}</dd>
                </div>
                <div>
                  <dt class="font-semibold text-slate-500">Chemin cible</dt>
                  <dd class="mt-1 break-all font-mono">{{ evenementDetail.path || 'Non exposé' }}</dd>
                </div>
                <div>
                  <dt class="font-semibold text-slate-500">Hash déclaré</dt>
                  <dd class="mt-1 break-all font-mono" :title="evenementDetail.hash_sha256">{{ hashCourt(evenementDetail.hash_sha256) }}</dd>
                </div>
                <div>
                  <dt class="font-semibold text-slate-500">Hash réel</dt>
                  <dd class="mt-1 break-all font-mono" :title="documentDuDetail?.actual_hash">{{ hashCourt(documentDuDetail?.actual_hash || evenementDetail.validation?.actual_hash) }}</dd>
                </div>
              </dl>
              <div class="rounded-2xl p-4 ring-1" :class="classeTon(statutVersTon(evenementDetail.validation?.status))">
                <p class="font-semibold">Explication</p>
                <p v-if="evenementDetail.validation?.status === 'baseline'" class="mt-1">
                  Cette ligne contient une anomalie historique connue. Elle reste visible, mais elle est maîtrisée par une baseline stricte liée au hash exact de la ligne brute.
                </p>
                <p v-else-if="evenementDetail.validation?.status === 'hash_ok'" class="mt-1">
                  Le fichier ciblé existe et son hash réel correspond au hash déclaré dans le stream.
                </p>
                <p v-else class="mt-1">
                  Cet événement demande une vérification complémentaire.
                </p>
              </div>
            </div>
            <p v-else class="mt-4 text-slate-600">Aucun événement sélectionné.</p>
          </aside>
        </section>

        <section v-show="ongletActif === 'documents'" class="rounded-3xl bg-white p-5 shadow-sm ring-1 ring-slate-200 md:p-6">
          <div class="flex flex-col gap-2 md:flex-row md:items-end md:justify-between">
            <div>
              <h2 class="text-2xl font-semibold">Documents référencés</h2>
              <p class="mt-1 text-slate-600">Artefacts ciblés par les événements du noyau événementiel.</p>
            </div>
            <span class="rounded-full bg-slate-50 px-3 py-1 text-sm font-semibold text-slate-700 ring-1 ring-slate-200">{{ documents.length }} documents</span>
          </div>
          <div class="mt-5 grid gap-4 md:grid-cols-2 xl:grid-cols-3">
            <article v-for="doc in documents" :key="doc.path" class="rounded-3xl bg-slate-50 p-5 ring-1 ring-slate-200">
              <div class="flex items-start justify-between gap-3">
                <div>
                  <h3 class="break-all text-lg font-semibold">{{ nomCourt(doc.path) }}</h3>
                  <p class="mt-1 text-sm text-slate-500">{{ typeDocument(doc) }}</p>
                </div>
                <span class="rounded-full px-3 py-1 text-sm font-semibold ring-1" :class="classeTon(doc.hash_status === 'ok' ? 'ok' : 'danger')">
                  {{ doc.hash_status === 'ok' ? 'Hash valide' : 'Anomalie' }}
                </span>
              </div>
              <p class="mt-4 break-all font-mono text-sm text-slate-600">{{ doc.path }}</p>
              <div class="mt-4 grid gap-2 text-sm">
                <p><span class="font-semibold text-slate-500">Fichier:</span> {{ doc.exists ? 'présent' : 'manquant' }}</p>
                <p :title="doc.declared_hash"><span class="font-semibold text-slate-500">Hash déclaré:</span> <span class="font-mono">{{ hashCourt(doc.declared_hash) }}</span></p>
                <p :title="doc.actual_hash"><span class="font-semibold text-slate-500">Hash réel:</span> <span class="font-mono">{{ hashCourt(doc.actual_hash) }}</span></p>
              </div>
              <button class="mt-5 rounded-2xl bg-white px-4 py-2 text-sm font-semibold text-slate-800 ring-1 ring-slate-200 transition hover:bg-slate-100" type="button" @click="ongletActif = 'evenements'">
                Inspecter
              </button>
            </article>
            <p v-if="documents.length === 0" class="text-slate-600">Aucun document référencé.</p>
          </div>
        </section>

        <section v-show="ongletActif === 'validation'" class="grid gap-6 xl:grid-cols-[1fr_420px]">
          <div class="rounded-3xl bg-white p-5 shadow-sm ring-1 ring-slate-200 md:p-6">
            <h2 class="text-2xl font-semibold">Validation pédagogique</h2>
            <div class="mt-5 grid gap-4 md:grid-cols-2">
              <article class="rounded-3xl bg-red-50 p-5 ring-1 ring-red-100">
                <p class="text-sm font-semibold uppercase tracking-[0.16em] text-red-700">Mode strict</p>
                <h3 class="mt-2 text-2xl font-semibold text-red-800">Échoue</h3>
                <p class="mt-2 text-red-900">Le validateur détecte une anomalie historique dans un stream append-only.</p>
              </article>
              <article class="rounded-3xl bg-emerald-50 p-5 ring-1 ring-emerald-100">
                <p class="text-sm font-semibold uppercase tracking-[0.16em] text-emerald-700">Avec baseline</p>
                <h3 class="mt-2 text-2xl font-semibold text-emerald-800">Passe</h3>
                <p class="mt-2 text-emerald-900">L’anomalie connue correspond exactement à la baseline stricte.</p>
              </article>
            </div>

            <div class="mt-6 space-y-4 text-slate-700">
              <div class="rounded-2xl bg-slate-50 p-4 ring-1 ring-slate-200">
                <h3 class="font-semibold text-slate-950">Pourquoi ce n’est pas grave actuellement</h3>
                <p class="mt-1">L’écart est identifié, localisé à une ligne précise et documenté par le hash SHA-256 de la ligne brute. Le stream n’est pas réécrit.</p>
              </div>
              <div class="rounded-2xl bg-slate-50 p-4 ring-1 ring-slate-200">
                <h3 class="font-semibold text-slate-950">Pourquoi ça reste sécurisé</h3>
                <p class="mt-1">La baseline ne masque pas une famille d’erreurs. Elle accepte uniquement cette anomalie exacte: même stream, même ligne, même code, même événement et même hash de ligne.</p>
              </div>
              <div class="rounded-2xl bg-slate-50 p-4 ring-1 ring-slate-200">
                <h3 class="font-semibold text-slate-950">Ce qui ferait échouer la baseline</h3>
                <p class="mt-1">Une ligne modifiée, une anomalie supplémentaire, un code différent, un événement différent ou une entrée devenue obsolète feraient échouer la validation avec baseline.</p>
              </div>
            </div>
          </div>

          <aside class="rounded-3xl bg-white p-5 shadow-sm ring-1 ring-slate-200 md:p-6">
            <h2 class="text-xl font-semibold">Anomalies connues</h2>
            <div class="mt-4 space-y-3">
              <article v-for="(finding, index) in baselineConnue" :key="index" class="rounded-2xl bg-amber-50 p-4 ring-1 ring-amber-100">
                <p class="font-semibold text-amber-900">{{ (finding as any).event_id }}</p>
                <p class="mt-2 text-sm text-amber-950">{{ (finding as any).message_fragment }}</p>
                <p class="mt-2 break-all font-mono text-sm text-amber-800">{{ (finding as any).stream_path }}:{{ (finding as any).line }}</p>
                <p class="mt-2 break-all font-mono text-sm text-amber-700" :title="(finding as any).raw_line_sha256">{{ hashCourt((finding as any).raw_line_sha256) }}</p>
              </article>
              <p v-if="baselineConnue.length === 0" class="text-slate-600">Aucune anomalie connue.</p>
            </div>
            <div v-if="baselineObsolete.length" class="mt-5 rounded-2xl bg-red-50 p-4 text-red-900 ring-1 ring-red-200">
              Une entrée de baseline est obsolète. La validation avec baseline doit rester en échec.
            </div>
          </aside>
        </section>

        <section v-show="ongletActif === 'roadmap'" class="rounded-3xl bg-white p-5 shadow-sm ring-1 ring-slate-200 md:p-6">
          <h2 class="text-2xl font-semibold">Feuille de route v0.1</h2>
          <p class="mt-1 text-slate-600">Lecture rapide de la maturité du socle Relinium.</p>
          <div class="mt-6 grid gap-4 md:grid-cols-2 xl:grid-cols-3">
            <article v-for="item in summary?.roadmap" :key="item.label" class="rounded-3xl bg-slate-50 p-5 ring-1 ring-slate-200">
              <div class="flex items-start justify-between gap-3">
                <div>
                  <h3 class="text-lg font-semibold">{{ item.label }}</h3>
                  <p class="mt-1 text-slate-600">{{ statutRoadmap(item.status) }}</p>
                </div>
                <span class="rounded-full px-3 py-1 text-sm font-semibold ring-1" :class="item.progress >= 70 ? classeTon('ok') : item.progress >= 30 ? classeTon('attention') : classeTon('info')">
                  {{ item.progress }} %
                </span>
              </div>
              <div class="mt-5 h-3 overflow-hidden rounded-full bg-white ring-1 ring-slate-200">
                <div class="h-full rounded-full" :class="item.progress >= 70 ? 'bg-emerald-500' : item.progress >= 30 ? 'bg-amber-500' : 'bg-sky-500'" :style="{ width: `${item.progress}%` }" />
              </div>
            </article>
          </div>
        </section>
      </div>
    </div>
  </section>
</template>
