<script setup lang="ts">
const { graphql } = useGraphqlRequest()
const route = useRoute()

const accountType = computed(() => route.query.type === 'individual' ? 'individual' : 'company')
const isIndividual = computed(() => accountType.value === 'individual')

const organizationName = ref('')
const organizationType = ref(isIndividual.value ? 'independant' : 'entreprise')
const legalIdentifier = ref('')
const country = ref('France')
const officialWebsite = ref('')
const contactName = ref('')
const email = ref('')
const phone = ref('')
const role = ref('')
const authorized = ref(false)
const loading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

const verificationSteps = computed(() => isIndividual.value ? [
  'vérification email',
  'vérification téléphone',
  'validation identité et usage',
  'activation humaine'
] : [
  'vérification email professionnel',
  'vérification téléphone',
  'contrôle du domaine ou site officiel',
  'contrôle justificatif',
  'validation humaine'
])

const pageTitle = computed(() => isIndividual.value ? 'Créer un compte individuel' : 'Créer un compte entreprise')
const pageIntro = computed(() => isIndividual.value
  ? 'Préparez un accès personnel Relinium. Cette étape ne valide pas automatiquement votre compte.'
  : 'Préparez l’ouverture d’un espace Relinium pour votre organisation. Cette étape ne valide pas automatiquement votre compte.'
)
const identityTitle = computed(() => isIndividual.value ? 'Identité et usage' : 'Identité de l’organisation')
const submitLabel = computed(() => isIndividual.value ? 'Préparer mon compte' : 'Préparer la demande')

async function submitRequest(): Promise<void> {
  loading.value = true
  errorMessage.value = ''
  successMessage.value = ''
  try {
    const messageRedacted = [
      `Contexte: ${isIndividual.value ? 'creation compte individuel' : 'creation organisation'}`,
      `Type: ${organizationType.value}`,
      `Identifiant legal: ${legalIdentifier.value || 'non renseigne'}`,
      `Pays: ${country.value}`,
      `Site officiel: ${officialWebsite.value || 'non renseigne'}`,
      `Contact responsable: ${contactName.value}`,
      `Telephone professionnel: ${phone.value || 'non renseigne'}`,
      `Fonction: ${role.value || 'non renseignee'}`,
      `Declaration responsable: ${authorized.value ? 'oui' : 'non'}`
    ].join('\n')

    const data = await graphql<{ requestAccess: { emailRedacted: string } }>(`
      mutation RequestCompanyAccess($input: RequestAccessInput!) {
        requestAccess(input: $input) { id emailRedacted status }
      }
    `, {
      input: {
        email: email.value,
        organizationHint: organizationName.value || (isIndividual.value ? 'Compte individuel' : ''),
        requestedRole: isIndividual.value ? 'viewer' : 'admin',
        messageRedacted
      }
    })

    successMessage.value = `Demande préparée pour ${data.requestAccess.emailRedacted}. Aucun justificatif n a été téléversé.`
    organizationName.value = ''
    legalIdentifier.value = ''
    officialWebsite.value = ''
    contactName.value = ''
    email.value = ''
    phone.value = ''
    role.value = ''
    authorized.value = false
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'Demande impossible.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <section class="w-full bg-slate-50 px-4 py-8 sm:px-6 lg:px-8">
    <div class="mx-auto max-w-5xl">
      <div class="max-w-3xl">
        <h1 class="text-3xl font-semibold text-slate-950">{{ pageTitle }}</h1>
        <p class="mt-3 text-slate-700">
          {{ pageIntro }}
        </p>
      </div>

      <form class="mt-6 grid gap-5 lg:grid-cols-[minmax(0,1fr)_320px]" @submit.prevent="submitRequest">
        <div class="space-y-5">
          <section class="min-w-0 rounded-lg border border-slate-200 bg-white p-5">
            <h2 class="text-lg font-semibold text-slate-950">{{ identityTitle }}</h2>
            <div class="mt-4 grid gap-4 sm:grid-cols-2">
              <label class="block text-sm font-semibold text-slate-700">{{ isIndividual ? 'Nom affiché' : 'Nom de l’organisation' }}
                <input v-model="organizationName" class="mt-1 h-10 w-full rounded-md border border-slate-300 px-3 text-sm" type="text" :required="!isIndividual">
              </label>
              <label class="block text-sm font-semibold text-slate-700">Type
                <select v-model="organizationType" class="mt-1 h-10 w-full rounded-md border border-slate-300 px-3 text-sm">
                  <option value="entreprise">Entreprise</option>
                  <option value="association">Association</option>
                  <option value="collectivite">Collectivité</option>
                  <option value="independant">Indépendant</option>
                  <option value="autre">Autre</option>
                </select>
              </label>
              <label v-if="!isIndividual" class="block text-sm font-semibold text-slate-700">SIREN/SIRET ou identifiant légal
                <input v-model="legalIdentifier" class="mt-1 h-10 w-full rounded-md border border-slate-300 px-3 text-sm" type="text">
              </label>
              <label class="block text-sm font-semibold text-slate-700">Pays
                <input v-model="country" class="mt-1 h-10 w-full rounded-md border border-slate-300 px-3 text-sm" type="text" required>
              </label>
              <label v-if="!isIndividual" class="block text-sm font-semibold text-slate-700 sm:col-span-2">Site web officiel
                <input v-model="officialWebsite" class="mt-1 h-10 w-full rounded-md border border-slate-300 px-3 text-sm" type="url" placeholder="https://">
              </label>
            </div>
          </section>

          <section class="min-w-0 rounded-lg border border-slate-200 bg-white p-5">
            <h2 class="text-lg font-semibold text-slate-950">Contact responsable</h2>
            <div class="mt-4 grid gap-4 sm:grid-cols-2">
              <label class="block text-sm font-semibold text-slate-700">Nom/prénom
                <input v-model="contactName" class="mt-1 h-10 w-full rounded-md border border-slate-300 px-3 text-sm" type="text" required>
              </label>
              <label class="block text-sm font-semibold text-slate-700">{{ isIndividual ? 'Email' : 'Email professionnel' }}
                <input v-model="email" class="mt-1 h-10 w-full rounded-md border border-slate-300 px-3 text-sm" type="email" required>
              </label>
              <label class="block text-sm font-semibold text-slate-700">{{ isIndividual ? 'Téléphone' : 'Téléphone professionnel' }}
                <input v-model="phone" class="mt-1 h-10 w-full rounded-md border border-slate-300 px-3 text-sm" type="tel">
              </label>
              <label class="block text-sm font-semibold text-slate-700">{{ isIndividual ? 'Usage prévu' : 'Fonction' }}
                <input v-model="role" class="mt-1 h-10 w-full rounded-md border border-slate-300 px-3 text-sm" type="text">
              </label>
            </div>
            <label class="mt-4 flex gap-3 rounded-md bg-slate-50 p-3 text-sm text-slate-700 ring-1 ring-slate-200">
              <input v-model="authorized" class="mt-1 h-4 w-4 rounded border-slate-300" type="checkbox" required>
              <span>{{ isIndividual ? 'Je confirme demander cet accès pour mon propre usage.' : 'Je suis autorisé à demander l’ouverture d’un espace Relinium pour cette organisation.' }}</span>
            </label>
          </section>

          <section v-if="!isIndividual" class="min-w-0 rounded-lg border border-slate-200 bg-white p-5">
            <h2 class="text-lg font-semibold text-slate-950">Justificatif</h2>
            <div class="mt-4 rounded-md border border-dashed border-slate-300 bg-slate-50 p-4">
              <p class="text-sm font-semibold text-slate-800">Extrait Kbis / document légal</p>
              <p class="mt-1 text-sm text-slate-600">Téléversement sécurisé à venir. Aucun fichier n’est stocké dans cette version.</p>
              <button class="mt-3 inline-flex h-9 cursor-not-allowed items-center rounded-md bg-slate-200 px-3 text-sm font-semibold text-slate-500" type="button" disabled>
                Upload indisponible
              </button>
            </div>
          </section>
        </div>

        <aside class="space-y-5">
          <section class="min-w-0 rounded-lg border border-slate-200 bg-white p-5">
            <h2 class="text-lg font-semibold text-slate-950">Vérifications prévues</h2>
            <ul class="mt-4 space-y-3 text-sm text-slate-700">
              <li v-for="step in verificationSteps" :key="step" class="flex gap-2">
                <span class="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-cyan-700" aria-hidden="true" />
                <span>{{ step }}</span>
              </li>
            </ul>
          </section>

          <section class="min-w-0 rounded-lg border border-slate-200 bg-white p-5">
            <p class="text-sm leading-6 text-slate-700">
              Ne saisissez aucun mot de passe, token, clé API ou information bancaire. {{ isIndividual ? 'La validation porte sur l’identité et l’usage déclaré.' : 'La demande prépare un échange de validation, elle n’ouvre pas automatiquement l’accès.' }}
            </p>
            <p v-if="errorMessage" class="mt-4 rounded-md bg-red-50 p-3 text-sm text-red-800 ring-1 ring-red-200">{{ errorMessage }}</p>
            <p v-if="successMessage" class="mt-4 rounded-md bg-emerald-50 p-3 text-sm text-emerald-800 ring-1 ring-emerald-200">{{ successMessage }}</p>
            <button class="mt-4 inline-flex h-10 w-full items-center justify-center rounded-md bg-cyan-950 px-4 text-sm font-semibold text-white disabled:opacity-60" type="submit" :disabled="loading">
              {{ submitLabel }}
            </button>
            <NuxtLink class="mt-3 inline-flex text-sm font-semibold text-slate-600 hover:text-slate-950" to="/connexion">Retour aux accès</NuxtLink>
          </section>
        </aside>
      </form>
    </div>
  </section>
</template>
