<script setup lang="ts">
type Etape = 'dossier' | 'preuve' | 'questionnaire' | 'timeline' | 'indicateurs' | 'rapports' | 'correlations'

type ScamCase = {
  id: string
  title: string
  status: string
  severity: string
  initialVector: string
  victimType: string
  summary: string
  createdAt: string
  custodyEvents: CustodyEvent[]
}

type CustodyEvent = {
  id: string
  action: string
  occurredAt: string
  eventHash: string
}

type QuestionnaireItem = {
  key: string
  label: string
  answerType: string
  why: string
  action: string
}

type TimelineEvent = {
  id: string
  occurredAt?: string | null
  eventType: string
  label: string
  source: string
  confidence: number
}

type Indicator = {
  id: string
  indicatorType: string
  valueRedacted: string
  valueHash: string
  riskLevel: string
  confidence: number
  notesRedacted: string
}

type Report = {
  id: string
  reportType: string
  status: string
  contentMarkdown: string
  sha256: string
}

type Correlation = {
  id: string
  targetCaseTitle: string
  correlationType: string
  score: number
  explanation: string
}

const { graphql } = useGraphqlRequest()

const etapes: Array<{ id: Etape, label: string }> = [
  { id: 'dossier', label: 'Dossier' },
  { id: 'preuve', label: 'Preuve' },
  { id: 'questionnaire', label: 'Questionnaire' },
  { id: 'timeline', label: 'Timeline' },
  { id: 'indicateurs', label: 'Indicateurs' },
  { id: 'rapports', label: 'Rapports' },
  { id: 'correlations', label: 'Corrélations' }
]

const etapeActive = ref<Etape>('dossier')
const chargement = ref(false)
const erreur = ref('')
const message = ref('')
const dossierSelectionne = ref<string | null>(null)

const dossiers = ref<ScamCase[]>([])
const questionnaire = ref<QuestionnaireItem[]>([])
const timeline = ref<TimelineEvent[]>([])
const indicateurs = ref<Indicator[]>([])
const rapports = ref<Report[]>([])
const correlations = ref<Correlation[]>([])
const dernierHash = ref('')
const derniersCustody = ref<CustodyEvent[]>([])

const nouveauDossier = reactive({
  title: '',
  victimType: 'individual',
  initialVector: 'email',
  summary: ''
})

const preuve = reactive({
  artifactType: 'eml',
  sourceDescription: '',
  rawText: ''
})

const reponses = reactive<Record<string, boolean | number | string>>({})
const rapportActif = ref<string | null>(null)

const dossierActif = computed(() => dossiers.value.find((dossier) => dossier.id === dossierSelectionne.value) || dossiers.value[0] || null)
const rapportsTries = computed(() => rapports.value.slice().sort((a, b) => a.reportType.localeCompare(b.reportType)))
const rapportPreview = computed(() => rapportsTries.value.find((rapport) => rapport.id === rapportActif.value) || rapportsTries.value[0] || null)

async function chargerBase(): Promise<void> {
  erreur.value = ''
  chargement.value = true
  try {
    const data = await graphql<{ scamCases: ScamCase[], scamQuestionnaireTemplate: QuestionnaireItem[] }>(`
      query AntiScamBase {
        scamCases { id title status severity initialVector victimType summary createdAt custodyEvents { id action occurredAt eventHash } }
        scamQuestionnaireTemplate { key label answerType why action }
      }
    `)
    dossiers.value = data.scamCases
    questionnaire.value = data.scamQuestionnaireTemplate
    if (!dossierSelectionne.value && dossiers.value[0]) {
      dossierSelectionne.value = dossiers.value[0].id
      await chargerDossierLie()
    }
  } catch (err) {
    erreur.value = messageErreurGraphql(err, 'Le module Anti-Scam attend les dépendances GraphQL du backend. Les écrans restent consultables, mais les dossiers ne peuvent pas être chargés pour l’instant.')
  } finally {
    chargement.value = false
  }
}

async function chargerDossierLie(): Promise<void> {
  if (!dossierActif.value) return
  const caseId = dossierActif.value.id
  const data = await graphql<{ timeline: TimelineEvent[], indicators: Indicator[], reports: Report[], correlations: Correlation[] }>(`
    query ScamCaseDetails($caseId: String!) {
      timeline: scamCaseTimeline(caseId: $caseId) { id occurredAt eventType label source confidence }
      indicators: scamCaseIndicators(caseId: $caseId) { id indicatorType valueRedacted valueHash riskLevel confidence notesRedacted }
      reports: scamCaseReports(caseId: $caseId) { id reportType status contentMarkdown sha256 }
      correlations: scamCaseCorrelations(caseId: $caseId) { id targetCaseTitle correlationType score explanation }
    }
  `, { caseId })
  timeline.value = data.timeline
  indicateurs.value = data.indicators
  rapports.value = data.reports
  correlations.value = data.correlations
  rapportActif.value = data.reports[0]?.id || null
}

async function creerDossier(): Promise<void> {
  if (!nouveauDossier.title.trim()) {
    erreur.value = 'Le titre du dossier est requis.'
    return
  }
  erreur.value = ''
  message.value = ''
  chargement.value = true
  try {
    const data = await graphql<{ createScamCase: ScamCase }>(`
      mutation CreateScamCase($input: CreateScamCaseInput!) {
        createScamCase(input: $input) { id title status severity initialVector victimType summary createdAt custodyEvents { id action occurredAt eventHash } }
      }
    `, {
      input: {
        title: nouveauDossier.title,
        victimType: nouveauDossier.victimType,
        initialVector: nouveauDossier.initialVector,
        summary: nouveauDossier.summary
      }
    })
    dossiers.value = [data.createScamCase, ...dossiers.value.filter((item) => item.id !== data.createScamCase.id)]
    dossierSelectionne.value = data.createScamCase.id
    message.value = 'Dossier anti-scam créé.'
    etapeActive.value = 'preuve'
    await chargerDossierLie()
  } catch (err) {
    erreur.value = messageErreurGraphql(err, 'Création impossible tant que GraphQL est indisponible.')
  } finally {
    chargement.value = false
  }
}

async function ajouterPreuve(): Promise<void> {
  if (!dossierActif.value) return
  if (!preuve.rawText.trim()) {
    erreur.value = 'Colle un email, SMS, récit ou texte limité pour calculer le hash.'
    return
  }
  erreur.value = ''
  message.value = ''
  chargement.value = true
  try {
    const data = await graphql<{ addScamArtifact: { artifact: { sha256: string }, custodyEvents: CustodyEvent[], indicators: Indicator[] } }>(`
      mutation AddScamArtifact($input: AddScamArtifactInput!) {
        addScamArtifact(input: $input) {
          artifact { id sha256 artifactType integrityStatus sizeBytes }
          custodyEvents { id action occurredAt eventHash }
          indicators { id indicatorType valueRedacted valueHash riskLevel confidence notesRedacted }
        }
      }
    `, {
      input: {
        caseId: dossierActif.value.id,
        artifactType: preuve.artifactType,
        rawText: preuve.rawText,
        sourceDescription: preuve.sourceDescription
      }
    })
    dernierHash.value = data.addScamArtifact.artifact.sha256
    derniersCustody.value = data.addScamArtifact.custodyEvents
    indicateurs.value = data.addScamArtifact.indicators
    message.value = 'Preuve hashée et indicateurs extraits sans interaction externe.'
    etapeActive.value = 'questionnaire'
    await chargerDossierLie()
  } catch (err) {
    erreur.value = messageErreurGraphql(err, 'Ingestion impossible tant que GraphQL est indisponible.')
  } finally {
    chargement.value = false
  }
}

async function repondre(question: QuestionnaireItem): Promise<void> {
  if (!dossierActif.value) return
  const valeur = reponses[question.key]
  erreur.value = ''
  try {
    await graphql(`
      mutation AnswerScamQuestion($input: AnswerScamQuestionInput!) {
        answerScamQuestion(input: $input) { id questionKey answeredAt }
      }
    `, {
      input: {
        caseId: dossierActif.value.id,
        questionKey: question.key,
        value: valeur,
        confidence: 0.8
      }
    })
    message.value = 'Réponse enregistrée et timeline mise à jour.'
    await chargerDossierLie()
  } catch (err) {
    erreur.value = messageErreurGraphql(err, 'Réponse non enregistrée tant que GraphQL est indisponible.')
  }
}

async function genererRapports(): Promise<void> {
  if (!dossierActif.value) return
  erreur.value = ''
  chargement.value = true
  try {
    const data = await graphql<{ generateScamReports: Report[] }>(`
      mutation GenerateScamReports($caseId: String!) {
        generateScamReports(caseId: $caseId) { id reportType status contentMarkdown sha256 }
      }
    `, { caseId: dossierActif.value.id })
    rapports.value = data.generateScamReports
    rapportActif.value = rapports.value[0]?.id || null
    message.value = 'Rapports Markdown générés en brouillon. Aucun envoi externe.'
    etapeActive.value = 'rapports'
    await chargerBase()
    await chargerDossierLie()
  } catch (err) {
    erreur.value = messageErreurGraphql(err, 'Génération impossible tant que GraphQL est indisponible.')
  } finally {
    chargement.value = false
  }
}

async function marquerRelu(report: Report): Promise<void> {
  const data = await graphql<{ markReportReviewed: Report }>(`
    mutation MarkReportReviewed($reportId: String!) {
      markReportReviewed(reportId: $reportId) { id reportType status contentMarkdown sha256 }
    }
  `, { reportId: report.id })
  rapports.value = rapports.value.map((item) => item.id === data.markReportReviewed.id ? data.markReportReviewed : item)
  message.value = 'Rapport marqué comme relu.'
}

function selectionnerDossier(id: string): void {
  dossierSelectionne.value = id
  chargerDossierLie()
}

function libelle(value: string): string {
  const labels: Record<string, string> = {
    draft: 'Brouillon',
    active: 'Actif',
    ready_for_review: 'À relire',
    reported: 'Signalé',
    closed: 'Clos',
    low: 'Faible',
    medium: 'Moyen',
    high: 'Élevé',
    critical: 'Critique',
    email: 'Email',
    sms: 'SMS',
    call: 'Appel',
    chat: 'Messagerie',
    document: 'Document',
    usb: 'Clé USB',
    website: 'Faux site',
    bank_transaction: 'Transaction bancaire',
    remote_access: 'Accès distant',
    individual: 'Particulier',
    company: 'Entreprise',
    association: 'Association',
    public_entity: 'Entité publique',
    unknown: 'Inconnu',
    victim: 'Victime',
    authorities: 'Autorités',
    bank: 'Banque',
    technical: 'Technique',
    company_report: 'Entreprise',
    draft_report: 'Brouillon',
    reviewed: 'Relu'
  }
  return labels[value] || value
}

function hashCourt(value?: string): string {
  return value ? `${value.slice(0, 12)}…${value.slice(-8)}` : 'Non disponible'
}

function classeRisque(value?: string): string {
  if (value === 'critical' || value === 'high') return 'bg-red-50 text-red-800 ring-red-200'
  if (value === 'medium') return 'bg-amber-50 text-amber-900 ring-amber-200'
  return 'bg-emerald-50 text-emerald-800 ring-emerald-200'
}

function messageErreurGraphql(err: unknown, fallback: string): string {
  const responseData = (err as { response?: { _data?: { error?: string } } })?.response?._data
  if (responseData?.error?.includes('GraphQL dependencies')) {
    return 'GraphQL indisponible: dépendances backend non installées. Le shell Relinium reste utilisable; les actions Anti-Scam seront disponibles quand GraphQL sera prêt.'
  }
  if (err instanceof Error && err.message) return err.message
  return fallback
}

onMounted(chargerBase)
</script>

<template>
  <section class="w-full max-w-full overflow-x-hidden bg-[#eef2f5] px-4 py-6 sm:px-6 lg:px-8">
    <div class="mx-auto max-w-7xl">
      <div class="mb-6">
        <p class="text-sm font-semibold uppercase tracking-[0.16em] text-teal-700">Relinium Anti-Scam</p>
        <h1 class="mt-1 text-3xl font-semibold tracking-normal">Relinium Anti-Scam</h1>
        <p class="mt-2 max-w-3xl text-slate-600">Chaîne de conservation, questionnaire, timeline et rapports.</p>
        <div class="mt-5 grid gap-3 md:grid-cols-4">
          <p class="rounded-lg bg-white p-3 text-sm font-semibold text-slate-700 ring-1 ring-slate-200">1. Preuve</p>
          <p class="rounded-lg bg-white p-3 text-sm font-semibold text-slate-700 ring-1 ring-slate-200">2. Questionnaire</p>
          <p class="rounded-lg bg-white p-3 text-sm font-semibold text-slate-700 ring-1 ring-slate-200">3. Timeline</p>
          <p class="rounded-lg bg-white p-3 text-sm font-semibold text-slate-700 ring-1 ring-slate-200">4. Rapports</p>
        </div>
      </div>

      <section class="grid max-w-full gap-6 lg:grid-cols-[minmax(0,320px)_minmax(0,1fr)]">
      <aside class="space-y-4">
        <section class="rounded-lg bg-white p-4 shadow-sm ring-1 ring-slate-200">
          <div class="flex items-center justify-between gap-3">
            <h2 class="text-lg font-semibold">Dossiers</h2>
            <button class="rounded-lg bg-teal-700 px-3 py-2 text-sm font-semibold text-white" type="button" @click="etapeActive = 'dossier'">
              Nouveau
            </button>
          </div>
          <div class="mt-4 space-y-2">
            <button
              v-for="dossier in dossiers"
              :key="dossier.id"
              class="w-full rounded-lg p-3 text-left ring-1 transition"
              :class="dossierActif?.id === dossier.id ? 'bg-slate-950 text-white ring-slate-950' : 'bg-slate-50 text-slate-800 ring-slate-200 hover:bg-white'"
              type="button"
              @click="selectionnerDossier(dossier.id)"
            >
              <span class="block font-semibold">{{ dossier.title }}</span>
              <span class="mt-1 block text-sm opacity-75">{{ libelle(dossier.initialVector) }} · {{ libelle(dossier.status) }}</span>
            </button>
            <p v-if="dossiers.length === 0" class="text-sm text-slate-600">Aucun dossier pour l’instant.</p>
          </div>
        </section>

        <nav class="rounded-lg bg-white p-3 shadow-sm ring-1 ring-slate-200">
          <button
            v-for="etape in etapes"
            :key="etape.id"
            class="mb-2 w-full rounded-lg px-3 py-2 text-left text-sm font-semibold last:mb-0"
            :class="etapeActive === etape.id ? 'bg-teal-700 text-white' : 'bg-slate-50 text-slate-700 hover:bg-slate-100'"
            type="button"
            @click="etapeActive = etape.id"
          >
            {{ etape.label }}
          </button>
        </nav>
      </aside>

      <div class="space-y-4">
        <div v-if="chargement" class="rounded-lg bg-white p-4 text-slate-700 ring-1 ring-slate-200">Traitement en cours…</div>
        <div v-if="erreur" class="rounded-lg bg-red-50 p-4 text-red-900 ring-1 ring-red-200">{{ erreur }}</div>
        <div v-if="message" class="rounded-lg bg-emerald-50 p-4 text-emerald-900 ring-1 ring-emerald-200">{{ message }}</div>

        <section v-if="dossierActif" class="grid gap-3 md:grid-cols-4">
          <article class="rounded-lg bg-white p-4 ring-1 ring-slate-200">
            <p class="text-sm font-semibold text-slate-500">Statut</p>
            <p class="mt-1 text-lg font-semibold">{{ libelle(dossierActif.status) }}</p>
          </article>
          <article class="rounded-lg bg-white p-4 ring-1 ring-slate-200">
            <p class="text-sm font-semibold text-slate-500">Risque</p>
            <p class="mt-1 w-fit rounded-lg px-2 py-1 text-sm font-semibold ring-1" :class="classeRisque(dossierActif.severity)">{{ libelle(dossierActif.severity) }}</p>
          </article>
          <article class="rounded-lg bg-white p-4 ring-1 ring-slate-200">
            <p class="text-sm font-semibold text-slate-500">Vecteur</p>
            <p class="mt-1 text-lg font-semibold">{{ libelle(dossierActif.initialVector) }}</p>
          </article>
          <article class="rounded-lg bg-white p-4 ring-1 ring-slate-200">
            <p class="text-sm font-semibold text-slate-500">Indicateurs</p>
            <p class="mt-1 text-lg font-semibold">{{ indicateurs.length }}</p>
          </article>
        </section>

        <section v-show="etapeActive === 'dossier'" class="rounded-lg bg-white p-5 shadow-sm ring-1 ring-slate-200">
          <h2 class="text-xl font-semibold">Créer un dossier anti-scam</h2>
          <div class="mt-5 grid gap-4 md:grid-cols-2">
            <label class="block">
              <span class="text-sm font-semibold text-slate-600">Titre minimisé</span>
              <input v-model="nouveauDossier.title" class="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2" placeholder="Ex: SMS colis suspect - victime A" type="text">
            </label>
            <label class="block">
              <span class="text-sm font-semibold text-slate-600">Type de victime</span>
              <select v-model="nouveauDossier.victimType" class="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2">
                <option value="individual">Particulier</option>
                <option value="company">Entreprise</option>
                <option value="association">Association</option>
                <option value="public_entity">Entité publique</option>
                <option value="unknown">Inconnu</option>
              </select>
            </label>
            <label class="block">
              <span class="text-sm font-semibold text-slate-600">Vecteur initial</span>
              <select v-model="nouveauDossier.initialVector" class="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2">
                <option value="email">Email</option>
                <option value="sms">SMS</option>
                <option value="call">Appel</option>
                <option value="chat">Messagerie</option>
                <option value="document">Document</option>
                <option value="usb">Clé USB</option>
                <option value="website">Faux site</option>
                <option value="bank_transaction">Transaction bancaire</option>
                <option value="remote_access">Accès distant</option>
                <option value="other">Autre</option>
              </select>
            </label>
            <label class="block md:col-span-2">
              <span class="text-sm font-semibold text-slate-600">Résumé court</span>
              <textarea v-model="nouveauDossier.summary" class="mt-1 min-h-28 w-full rounded-lg border border-slate-300 px-3 py-2" placeholder="Décrire les faits sans secret ni donnée excessive." />
            </label>
          </div>
          <button class="mt-5 rounded-lg bg-teal-700 px-4 py-3 font-semibold text-white" type="button" @click="creerDossier">
            Créer le dossier anti-scam
          </button>
        </section>

        <section v-show="etapeActive === 'preuve'" class="rounded-lg bg-white p-5 shadow-sm ring-1 ring-slate-200">
          <h2 class="text-xl font-semibold">Ajouter une preuve</h2>
          <p class="mt-2 text-slate-600">Colle un EML, SMS, récit ou extrait texte. Le backend calcule le SHA-256 et extrait les indicateurs sans visiter les liens.</p>
          <div class="mt-5 grid gap-4 md:grid-cols-2">
            <label class="block">
              <span class="text-sm font-semibold text-slate-600">Type d’artefact</span>
              <select v-model="preuve.artifactType" class="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2">
                <option value="eml">Email brut EML</option>
                <option value="sms_text">SMS</option>
                <option value="call_note">Note d’appel</option>
                <option value="document">Document</option>
                <option value="url">URL</option>
                <option value="bank_record">Relevé bancaire</option>
                <option value="log_export">Export journal</option>
                <option value="other">Autre</option>
              </select>
            </label>
            <label class="block">
              <span class="text-sm font-semibold text-slate-600">Source</span>
              <input v-model="preuve.sourceDescription" class="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2" placeholder="Ex: email transféré par la victime" type="text">
            </label>
            <label class="block md:col-span-2">
              <span class="text-sm font-semibold text-slate-600">Contenu texte limité</span>
              <textarea v-model="preuve.rawText" class="mt-1 min-h-56 w-full rounded-lg border border-slate-300 px-3 py-2 font-mono text-sm" placeholder="Coller ici l’EML, le SMS ou le récit." />
            </label>
          </div>
          <button class="mt-5 rounded-lg bg-teal-700 px-4 py-3 font-semibold text-white" type="button" @click="ajouterPreuve">
            Calculer le hash et extraire
          </button>
          <div v-if="dernierHash" class="mt-5 rounded-lg bg-slate-50 p-4 ring-1 ring-slate-200">
            <p class="font-semibold">SHA-256</p>
            <p class="mt-1 break-all font-mono text-sm">{{ dernierHash }}</p>
            <div class="mt-3 grid gap-2 md:grid-cols-2">
              <p v-for="event in derniersCustody" :key="event.id" class="rounded-lg bg-white p-3 text-sm ring-1 ring-slate-200">
                {{ libelle(event.action) }} · <span class="font-mono">{{ hashCourt(event.eventHash) }}</span>
              </p>
            </div>
          </div>
        </section>

        <section v-show="etapeActive === 'questionnaire'" class="rounded-lg bg-white p-5 shadow-sm ring-1 ring-slate-200">
          <h2 class="text-xl font-semibold">Questionnaire guidé</h2>
          <div class="mt-5 grid gap-4">
            <article v-for="question in questionnaire" :key="question.key" class="rounded-lg bg-slate-50 p-4 ring-1 ring-slate-200">
              <div class="grid gap-4 lg:grid-cols-[1fr_220px]">
                <div>
                  <h3 class="font-semibold">{{ question.label }}</h3>
                  <p class="mt-1 text-sm text-slate-600">{{ question.why }}</p>
                  <p class="mt-1 text-sm text-teal-800">{{ question.action }}</p>
                </div>
                <div class="flex items-center gap-2">
                  <template v-if="question.answerType === 'boolean'">
                    <label class="flex items-center gap-2 rounded-lg bg-white px-3 py-2 ring-1 ring-slate-200">
                      <input v-model="reponses[question.key]" :value="true" type="radio">
                      Oui
                    </label>
                    <label class="flex items-center gap-2 rounded-lg bg-white px-3 py-2 ring-1 ring-slate-200">
                      <input v-model="reponses[question.key]" :value="false" type="radio">
                      Non
                    </label>
                  </template>
                  <input v-else v-model="reponses[question.key]" class="w-full rounded-lg border border-slate-300 px-3 py-2" min="0" type="number">
                  <button class="rounded-lg bg-slate-950 px-3 py-2 text-sm font-semibold text-white" type="button" @click="repondre(question)">
                    Enregistrer
                  </button>
                </div>
              </div>
            </article>
          </div>
        </section>

        <section v-show="etapeActive === 'timeline'" class="rounded-lg bg-white p-5 shadow-sm ring-1 ring-slate-200">
          <h2 class="text-xl font-semibold">Timeline probatoire</h2>
          <div class="mt-5 space-y-3">
            <article v-for="event in timeline" :key="event.id" class="rounded-lg bg-slate-50 p-4 ring-1 ring-slate-200">
              <p class="font-semibold">{{ event.label }}</p>
              <p class="mt-1 text-sm text-slate-600">{{ event.occurredAt || 'Date inconnue' }} · {{ event.source }} · confiance {{ Math.round(event.confidence * 100) }} %</p>
            </article>
            <p v-if="timeline.length === 0" class="text-slate-600">La timeline sera alimentée par les preuves et le questionnaire.</p>
          </div>
        </section>

        <section v-show="etapeActive === 'indicateurs'" class="rounded-lg bg-white p-5 shadow-sm ring-1 ring-slate-200">
          <h2 class="text-xl font-semibold">Indicateurs extraits</h2>
          <div class="mt-5 grid gap-3 md:grid-cols-2">
            <article v-for="indicator in indicateurs" :key="indicator.id" class="rounded-lg bg-slate-50 p-4 ring-1 ring-slate-200">
              <div class="flex items-start justify-between gap-3">
                <p class="font-semibold">{{ indicator.indicatorType }}</p>
                <span class="rounded-lg px-2 py-1 text-xs font-semibold ring-1" :class="classeRisque(indicator.riskLevel)">{{ libelle(indicator.riskLevel) }}</span>
              </div>
              <p class="mt-2 break-all font-mono text-sm">{{ indicator.valueRedacted }}</p>
              <p class="mt-2 break-all text-xs text-slate-500">Hash valeur: {{ hashCourt(indicator.valueHash) }}</p>
              <p class="mt-1 text-sm text-slate-600">{{ indicator.notesRedacted }}</p>
            </article>
            <p v-if="indicateurs.length === 0" class="text-slate-600">Aucun indicateur extrait pour ce dossier.</p>
          </div>
        </section>

        <section v-show="etapeActive === 'rapports'" class="rounded-lg bg-white p-5 shadow-sm ring-1 ring-slate-200">
          <div class="flex flex-col justify-between gap-3 md:flex-row md:items-center">
            <div>
              <h2 class="text-xl font-semibold">Rapports Markdown</h2>
              <p class="mt-1 text-slate-600">Brouillons relisibles. Aucune soumission automatique.</p>
            </div>
            <button class="rounded-lg bg-teal-700 px-4 py-3 font-semibold text-white" type="button" @click="genererRapports">
              Générer les rapports
            </button>
          </div>
          <div class="mt-5 grid gap-4 lg:grid-cols-[220px_1fr]">
            <div class="space-y-2">
              <button
                v-for="report in rapportsTries"
                :key="report.id"
                class="w-full rounded-lg p-3 text-left ring-1"
                :class="rapportPreview?.id === report.id ? 'bg-slate-950 text-white ring-slate-950' : 'bg-slate-50 text-slate-800 ring-slate-200'"
                type="button"
                @click="rapportActif = report.id"
              >
                <span class="block font-semibold">{{ libelle(report.reportType) }}</span>
                <span class="text-sm opacity-75">{{ libelle(report.status) }}</span>
              </button>
            </div>
            <article v-if="rapportPreview" class="rounded-lg bg-slate-50 p-4 ring-1 ring-slate-200">
              <div class="mb-3 flex flex-col justify-between gap-3 md:flex-row md:items-center">
                <p class="break-all text-sm text-slate-600">SHA-256 rapport: <span class="font-mono">{{ rapportPreview.sha256 }}</span></p>
                <button class="rounded-lg bg-slate-950 px-3 py-2 text-sm font-semibold text-white" type="button" @click="marquerRelu(rapportPreview)">
                  Marquer relu
                </button>
              </div>
              <pre class="max-h-[560px] overflow-auto whitespace-pre-wrap rounded-lg bg-white p-4 text-sm leading-6 ring-1 ring-slate-200">{{ rapportPreview.contentMarkdown }}</pre>
            </article>
            <p v-else class="text-slate-600">Génère les rapports après avoir ajouté les premières preuves.</p>
          </div>
        </section>

        <section v-show="etapeActive === 'correlations'" class="rounded-lg bg-white p-5 shadow-sm ring-1 ring-slate-200">
          <h2 class="text-xl font-semibold">Corrélations multi-cas</h2>
          <p class="mt-1 text-slate-600">Les recoupements sont indicatifs et doivent être relus avant transmission.</p>
          <div class="mt-5 space-y-3">
            <article v-for="correlation in correlations" :key="correlation.id" class="rounded-lg bg-slate-50 p-4 ring-1 ring-slate-200">
              <p class="font-semibold">{{ correlation.targetCaseTitle }}</p>
              <p class="mt-1 text-sm text-slate-600">{{ correlation.correlationType }} · score {{ Math.round(correlation.score * 100) }} %</p>
              <p class="mt-2 text-sm">{{ correlation.explanation }}</p>
            </article>
            <p v-if="correlations.length === 0" class="text-slate-600">Aucune corrélation trouvée pour ce dossier.</p>
          </div>
        </section>
      </div>
      </section>
    </div>
  </section>
</template>
