<script setup lang="ts">
type FieldKey = 'organizationName' | 'legalIdentifier' | 'country' | 'officialWebsite' | 'contactName' | 'email' | 'phone' | 'role'
type PasswordStrength = 'faible' | 'correct' | 'fort'

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
const password = ref('')
const passwordConfirmation = ref('')
const authorized = ref(false)
const loading = ref(false)
const submitted = ref(false)
const errorMessage = ref('')
const successMessage = ref('')
const touched = reactive<Record<string, boolean>>({})

const fieldLabels: Record<FieldKey, string> = {
  organizationName: 'Nom affiché',
  legalIdentifier: 'Identifiant légal',
  country: 'Pays',
  officialWebsite: 'Site officiel',
  contactName: 'Nom',
  email: 'Email',
  phone: 'Téléphone',
  role: 'Usage prévu'
}

const maxLengths: Record<FieldKey, number> = {
  organizationName: 80,
  legalIdentifier: 80,
  country: 56,
  officialWebsite: 160,
  contactName: 80,
  email: 120,
  phone: 32,
  role: 280
}

const suspiciousPattern = /<script|javascript:|onerror=|onload=|bearer\s+|token=|api_key=|secret=|password=/i
const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

const pageTitle = computed(() => isIndividual.value ? 'Créer un compte individuel' : 'Créer un compte entreprise')
const pageIntro = computed(() => isIndividual.value
  ? 'Préparez votre accès personnel en quelques informations. L’activation reste vérifiée avant ouverture.'
  : 'Préparez l’ouverture d’un espace Relinium pour votre organisation. Cette étape ne valide pas automatiquement votre compte.'
)
const submitLabel = computed(() => {
  if (loading.value) return 'Préparation en cours'
  if (successMessage.value) return 'Demande préparée'
  return isIndividual.value ? 'Préparer ma demande' : 'Préparer la demande'
})

const displayName = computed(() => organizationName.value.trim() || contactName.value.trim())
const avatarInitials = computed(() => {
  const source = displayName.value || 'Votre nom'
  return source
    .split(/\s+/)
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0]?.toUpperCase())
    .join('') || 'VN'
})

const verificationSteps = computed(() => isIndividual.value ? [
  'Email vérifié ensuite',
  'Téléphone vérifié ensuite',
  'Activation humaine',
  'MFA à venir'
] : [
  'Email professionnel vérifié',
  'Téléphone vérifié ensuite',
  'Domaine ou site contrôlé',
  'Justificatif contrôlé',
  'Activation humaine'
])

const passwordChecks = computed(() => ({
  length: password.value.length >= 12,
  upper: /[A-Z]/.test(password.value),
  lower: /[a-z]/.test(password.value),
  digit: /\d/.test(password.value),
  special: /[^A-Za-z0-9]/.test(password.value)
}))

const passwordScore = computed(() => Object.values(passwordChecks.value).filter(Boolean).length)
const passwordStrength = computed<PasswordStrength>(() => {
  if (passwordScore.value >= 5 && password.value.length >= 16) return 'fort'
  if (passwordScore.value >= 5) return 'correct'
  return 'faible'
})
const passwordValid = computed(() => passwordScore.value === 5)
const passwordConfirmationValid = computed(() => password.value.length > 0 && password.value === passwordConfirmation.value)

const currentFields = computed<FieldKey[]>(() => isIndividual.value
  ? ['organizationName', 'email', 'phone', 'role']
  : ['organizationName', 'legalIdentifier', 'country', 'officialWebsite', 'contactName', 'email', 'phone', 'role']
)

const requiredFields = computed<FieldKey[]>(() => isIndividual.value
  ? ['organizationName', 'email', 'phone', 'role']
  : ['organizationName', 'country', 'contactName', 'email']
)

const values = computed<Record<FieldKey, string>>(() => ({
  organizationName: organizationName.value,
  legalIdentifier: legalIdentifier.value,
  country: country.value,
  officialWebsite: officialWebsite.value,
  contactName: contactName.value,
  email: email.value,
  phone: phone.value,
  role: role.value
}))

// Ces garde-fous UX complètent les validations serveur, ils ne sont pas une frontière de sécurité.
function fieldIssue(field: FieldKey): string {
  const value = values.value[field].trim()
  if (requiredFields.value.includes(field) && !value) return 'Ce champ est nécessaire.'
  if (value.length > maxLengths[field]) return `${fieldLabels[field]} doit rester sous ${maxLengths[field]} caractères.`
  if (value && suspiciousPattern.test(value)) {
    return 'Ce champ semble contenir une valeur technique ou sensible. Retirez les secrets avant de continuer.'
  }
  if (field === 'email' && value && !emailPattern.test(value)) return 'Indiquez un email valide.'
  if (field === 'officialWebsite' && value && !/^https?:\/\/[^\s]+\.[^\s]+$/i.test(value)) return 'Utilisez une URL complète, par exemple https://exemple.fr.'
  return ''
}

function fieldValid(field: FieldKey): boolean {
  return fieldIssue(field) === ''
}

function shouldShowFieldIssue(field: FieldKey): boolean {
  return Boolean((touched[field] || submitted.value) && fieldIssue(field))
}

function markTouched(field: FieldKey): void {
  touched[field] = true
}

function normalizeText(field: FieldKey, value: string): string {
  return value.trim().slice(0, maxLengths[field])
}

const formValid = computed(() => {
  const fieldsValid = currentFields.value.every((field) => fieldValid(field))
  if (!authorized.value || !fieldsValid) return false
  if (isIndividual.value) return passwordValid.value && passwordConfirmationValid.value
  return true
})

const passwordHint = computed(() => {
  if (!password.value && !submitted.value) return ''
  if (!passwordValid.value) return '12 caractères minimum, avec majuscule, minuscule, chiffre et caractère spécial.'
  return ''
})

const confirmationHint = computed(() => {
  if (!passwordConfirmation.value && !submitted.value) return ''
  if (!passwordConfirmationValid.value) return 'Les deux mots de passe doivent être identiques.'
  return ''
})

async function submitRequest(): Promise<void> {
  submitted.value = true
  currentFields.value.forEach((field) => markTouched(field))
  if (isIndividual.value) {
    touched.password = true
    touched.passwordConfirmation = true
  }
  if (!formValid.value) return

  loading.value = true
  errorMessage.value = ''
  successMessage.value = ''
  try {
    const trimmedName = normalizeText('organizationName', organizationName.value)
    const trimmedEmail = normalizeText('email', email.value)
    const trimmedPhone = normalizeText('phone', phone.value)
    const trimmedRole = normalizeText('role', role.value)
    const messageRedacted = isIndividual.value
      ? [
          'Contexte: creation compte individuel',
          `Nom affiche: ${trimmedName}`,
          `Telephone: ${trimmedPhone}`,
          `Usage prevu: ${trimmedRole}`,
          `Declaration secrets: ${authorized.value ? 'confirmee' : 'non confirmee'}`,
          'Mot de passe: non transmis par cette mutation'
        ].join('\n')
      : [
          'Contexte: creation organisation',
          `Type: ${organizationType.value}`,
          `Identifiant legal: ${normalizeText('legalIdentifier', legalIdentifier.value) || 'non renseigne'}`,
          `Pays: ${normalizeText('country', country.value)}`,
          `Site officiel: ${normalizeText('officialWebsite', officialWebsite.value) || 'non renseigne'}`,
          `Contact responsable: ${normalizeText('contactName', contactName.value)}`,
          `Telephone professionnel: ${trimmedPhone || 'non renseigne'}`,
          `Fonction: ${trimmedRole || 'non renseignee'}`,
          `Declaration responsable: ${authorized.value ? 'oui' : 'non'}`
        ].join('\n')

    const data = await graphql<{ requestAccess: { emailRedacted: string } }>(`
      mutation RequestCompanyAccess($input: RequestAccessInput!) {
        requestAccess(input: $input) { id emailRedacted status }
      }
    `, {
      input: {
        email: trimmedEmail,
        organizationHint: trimmedName || (isIndividual.value ? 'Compte individuel' : ''),
        requestedRole: isIndividual.value ? 'viewer' : 'admin',
        messageRedacted
      }
    })

    successMessage.value = isIndividual.value
      ? `Demande préparée pour ${data.requestAccess.emailRedacted}. L’activation nécessitera une validation.`
      : `Demande préparée pour ${data.requestAccess.emailRedacted}. Aucun justificatif n’a été téléversé.`
    organizationName.value = ''
    legalIdentifier.value = ''
    officialWebsite.value = ''
    contactName.value = ''
    email.value = ''
    phone.value = ''
    role.value = ''
    password.value = ''
    passwordConfirmation.value = ''
    authorized.value = false
    submitted.value = false
    Object.keys(touched).forEach((key) => {
      touched[key] = false
    })
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'Demande impossible.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <section class="min-h-[calc(100vh-4rem)] w-full overflow-x-hidden bg-sky-50 px-4 py-8 text-slate-950 sm:px-6 lg:px-8">
    <div class="mx-auto max-w-6xl overflow-hidden">
      <div class="max-w-3xl min-w-0">
        <p class="text-sm font-semibold text-cyan-800">Accès Relinium</p>
        <h1 class="mt-2 max-w-full text-3xl font-semibold tracking-normal text-slate-950 sm:text-4xl">{{ pageTitle }}</h1>
        <p class="mt-3 max-w-2xl text-wrap text-base leading-7 text-slate-600">
          {{ pageIntro }}
        </p>
      </div>

      <form class="mt-8 grid max-w-full gap-6 lg:grid-cols-[minmax(0,1fr)_320px]" novalidate @submit.prevent="submitRequest">
        <div class="min-w-0 max-w-full rounded-lg bg-white p-5 shadow-sm ring-1 ring-slate-200/70 sm:p-7">
          <div class="flex items-center gap-2 text-xs font-semibold uppercase tracking-normal text-slate-500">
            <span class="h-1.5 w-8 rounded-full bg-cyan-700" aria-hidden="true" />
            <span>{{ isIndividual ? 'Demande personnelle' : 'Demande organisation' }}</span>
          </div>

          <div v-if="isIndividual" class="mt-7 space-y-8">
            <section>
              <h2 class="text-lg font-semibold text-slate-950">Votre identité</h2>
              <div class="mt-4 grid gap-4 sm:grid-cols-2">
                <label class="block text-sm font-semibold text-slate-700 sm:col-span-2">
                  Nom affiché
                  <span class="relative mt-2 block">
                    <span class="pointer-events-none absolute inset-y-0 left-3 flex items-center text-slate-400" aria-hidden="true">◎</span>
                    <input
                      v-model="organizationName"
                      :maxlength="maxLengths.organizationName"
                      :aria-invalid="shouldShowFieldIssue('organizationName')"
                      class="h-12 w-full rounded-lg bg-slate-50 py-2 pl-10 pr-10 text-sm outline-none ring-1 ring-slate-200 transition focus:bg-white focus:ring-2 focus:ring-cyan-700"
                      :class="shouldShowFieldIssue('organizationName') ? 'ring-red-300 focus:ring-red-500' : fieldValid('organizationName') && organizationName.trim() ? 'ring-emerald-200' : ''"
                      type="text"
                      autocomplete="name"
                      placeholder="Ex. Grégory Catteau"
                      @blur="markTouched('organizationName')"
                    >
                    <span v-if="fieldValid('organizationName') && organizationName.trim()" class="pointer-events-none absolute inset-y-0 right-3 flex items-center text-emerald-600" aria-hidden="true">✓</span>
                  </span>
                  <span v-if="shouldShowFieldIssue('organizationName')" class="mt-2 block animate-[fadeIn_.18s_ease-out] text-xs font-medium text-red-700">{{ fieldIssue('organizationName') }}</span>
                </label>

                <label class="block text-sm font-semibold text-slate-700">
                  Email
                  <span class="relative mt-2 block">
                    <span class="pointer-events-none absolute inset-y-0 left-3 flex items-center text-slate-400" aria-hidden="true">@</span>
                    <input
                      v-model="email"
                      :maxlength="maxLengths.email"
                      :aria-invalid="shouldShowFieldIssue('email')"
                      class="h-12 w-full rounded-lg bg-slate-50 py-2 pl-10 pr-10 text-sm outline-none ring-1 ring-slate-200 transition focus:bg-white focus:ring-2 focus:ring-cyan-700"
                      :class="shouldShowFieldIssue('email') ? 'ring-red-300 focus:ring-red-500' : fieldValid('email') && email.trim() ? 'ring-emerald-200' : ''"
                      type="email"
                      autocomplete="email"
                      placeholder="vous@exemple.fr"
                      @blur="markTouched('email')"
                    >
                    <span v-if="fieldValid('email') && email.trim()" class="pointer-events-none absolute inset-y-0 right-3 flex items-center text-emerald-600" aria-hidden="true">✓</span>
                  </span>
                  <span v-if="shouldShowFieldIssue('email')" class="mt-2 block animate-[fadeIn_.18s_ease-out] text-xs font-medium text-red-700">{{ fieldIssue('email') }}</span>
                </label>

                <label class="block text-sm font-semibold text-slate-700">
                  Téléphone
                  <span class="relative mt-2 block">
                    <span class="pointer-events-none absolute inset-y-0 left-3 flex items-center text-slate-400" aria-hidden="true">☎</span>
                    <input
                      v-model="phone"
                      :maxlength="maxLengths.phone"
                      :aria-invalid="shouldShowFieldIssue('phone')"
                      class="h-12 w-full rounded-lg bg-slate-50 py-2 pl-10 pr-10 text-sm outline-none ring-1 ring-slate-200 transition focus:bg-white focus:ring-2 focus:ring-cyan-700"
                      :class="shouldShowFieldIssue('phone') ? 'ring-red-300 focus:ring-red-500' : fieldValid('phone') && phone.trim() ? 'ring-emerald-200' : ''"
                      type="tel"
                      autocomplete="tel"
                      placeholder="06 12 34 56 78"
                      @blur="markTouched('phone')"
                    >
                    <span v-if="fieldValid('phone') && phone.trim()" class="pointer-events-none absolute inset-y-0 right-3 flex items-center text-emerald-600" aria-hidden="true">✓</span>
                  </span>
                  <span v-if="shouldShowFieldIssue('phone')" class="mt-2 block animate-[fadeIn_.18s_ease-out] text-xs font-medium text-red-700">{{ fieldIssue('phone') }}</span>
                </label>
              </div>
            </section>

            <section>
              <h2 class="text-lg font-semibold text-slate-950">Sécurité du compte</h2>
              <p class="mt-2 rounded-lg bg-cyan-50 px-4 py-3 text-sm leading-6 text-cyan-950 ring-1 ring-cyan-100">
                Cette version prépare la demande. Le stockage du mot de passe sera activé avec l’authentification définitive.
              </p>
              <div class="mt-4 grid gap-4 sm:grid-cols-2">
                <label class="block text-sm font-semibold text-slate-700">
                  Mot de passe
                  <span class="relative mt-2 block">
                    <span class="pointer-events-none absolute inset-y-0 left-3 flex items-center text-slate-400" aria-hidden="true">⌘</span>
                    <input
                      v-model="password"
                      :aria-invalid="Boolean(passwordHint && (touched.password || submitted))"
                      class="h-12 w-full rounded-lg bg-slate-50 py-2 pl-10 pr-10 text-sm outline-none ring-1 ring-slate-200 transition focus:bg-white focus:ring-2 focus:ring-cyan-700"
                      :class="passwordHint && (touched.password || submitted) ? 'ring-red-300 focus:ring-red-500' : passwordValid ? 'ring-emerald-200' : ''"
                      type="password"
                      autocomplete="new-password"
                      placeholder="12 caractères minimum"
                      @blur="touched.password = true"
                    >
                    <span v-if="passwordValid" class="pointer-events-none absolute inset-y-0 right-3 flex items-center text-emerald-600" aria-hidden="true">✓</span>
                  </span>
                  <span v-if="passwordHint && (touched.password || submitted)" class="mt-2 block animate-[fadeIn_.18s_ease-out] text-xs font-medium text-red-700">{{ passwordHint }}</span>
                </label>

                <label class="block text-sm font-semibold text-slate-700">
                  Confirmer le mot de passe
                  <span class="relative mt-2 block">
                    <span class="pointer-events-none absolute inset-y-0 left-3 flex items-center text-slate-400" aria-hidden="true">✓</span>
                    <input
                      v-model="passwordConfirmation"
                      :aria-invalid="Boolean(confirmationHint && (touched.passwordConfirmation || submitted))"
                      class="h-12 w-full rounded-lg bg-slate-50 py-2 pl-10 pr-10 text-sm outline-none ring-1 ring-slate-200 transition focus:bg-white focus:ring-2 focus:ring-cyan-700"
                      :class="confirmationHint && (touched.passwordConfirmation || submitted) ? 'ring-red-300 focus:ring-red-500' : passwordConfirmationValid ? 'ring-emerald-200' : ''"
                      type="password"
                      autocomplete="new-password"
                      placeholder="Répétez le mot de passe"
                      @blur="touched.passwordConfirmation = true"
                    >
                    <span v-if="passwordConfirmationValid" class="pointer-events-none absolute inset-y-0 right-3 flex items-center text-emerald-600" aria-hidden="true">✓</span>
                  </span>
                  <span v-if="confirmationHint && (touched.passwordConfirmation || submitted)" class="mt-2 block animate-[fadeIn_.18s_ease-out] text-xs font-medium text-red-700">{{ confirmationHint }}</span>
                </label>
              </div>
              <div class="mt-4">
                <div class="flex items-center justify-between text-xs font-semibold text-slate-600">
                  <span>Force du mot de passe</span>
                  <span class="capitalize" :class="passwordStrength === 'fort' ? 'text-emerald-700' : passwordStrength === 'correct' ? 'text-cyan-800' : 'text-amber-700'">{{ passwordStrength }}</span>
                </div>
                <div class="mt-2 grid grid-cols-3 gap-2">
                  <span class="h-1.5 rounded-full" :class="passwordScore >= 2 ? 'bg-amber-500' : 'bg-slate-200'" />
                  <span class="h-1.5 rounded-full" :class="passwordValid ? 'bg-cyan-700' : 'bg-slate-200'" />
                  <span class="h-1.5 rounded-full" :class="passwordStrength === 'fort' ? 'bg-emerald-600' : 'bg-slate-200'" />
                </div>
              </div>
            </section>

            <section>
              <h2 class="text-lg font-semibold text-slate-950">Photo de profil</h2>
              <div class="mt-4 flex flex-col items-center gap-4 rounded-lg bg-slate-50 p-5 ring-1 ring-slate-200 sm:flex-row sm:items-center">
                <div class="flex h-20 w-20 shrink-0 items-center justify-center rounded-full bg-cyan-950 text-xl font-semibold text-white shadow-sm">
                  {{ avatarInitials }}
                </div>
                <div class="min-w-0 text-center sm:text-left">
                  <button class="inline-flex h-10 cursor-not-allowed items-center justify-center rounded-lg bg-slate-200 px-4 text-sm font-semibold text-slate-500" type="button" disabled>
                    Choisir une image
                  </button>
                  <p class="mt-2 text-wrap text-sm leading-6 text-slate-600">Avatar optionnel. Le téléversement sécurisé sera activé plus tard.</p>
                </div>
              </div>
            </section>

            <section>
              <h2 class="text-lg font-semibold text-slate-950">Usage prévu</h2>
              <label class="mt-4 block text-sm font-semibold text-slate-700">
                Décrivez en une phrase pourquoi vous ouvrez un accès.
                <textarea
                  v-model="role"
                  :maxlength="maxLengths.role"
                  :aria-invalid="shouldShowFieldIssue('role')"
                  class="mt-2 min-h-28 w-full resize-none rounded-lg bg-slate-50 p-4 text-sm outline-none ring-1 ring-slate-200 transition focus:bg-white focus:ring-2 focus:ring-cyan-700"
                  :class="shouldShowFieldIssue('role') ? 'ring-red-300 focus:ring-red-500' : fieldValid('role') && role.trim() ? 'ring-emerald-200' : ''"
                  placeholder="Ex. cartographier mes dossiers, suivre des preuves, préparer un audit…"
                  @blur="markTouched('role')"
                />
                <span class="mt-2 flex items-center justify-between gap-3 text-xs">
                  <span v-if="shouldShowFieldIssue('role')" class="animate-[fadeIn_.18s_ease-out] font-medium text-red-700">{{ fieldIssue('role') }}</span>
                  <span v-else class="text-slate-500">280 caractères maximum.</span>
                  <span class="shrink-0 text-slate-500">{{ role.length }}/280</span>
                </span>
              </label>
            </section>
          </div>

          <div v-else class="mt-7 space-y-6">
            <section>
              <h2 class="text-lg font-semibold text-slate-950">Identité de l’organisation</h2>
              <div class="mt-4 grid gap-4 sm:grid-cols-2">
                <label class="block text-sm font-semibold text-slate-700">Nom de l’organisation
                  <input v-model="organizationName" :maxlength="maxLengths.organizationName" class="mt-2 h-11 w-full rounded-lg bg-slate-50 px-3 text-sm outline-none ring-1 ring-slate-200 transition focus:bg-white focus:ring-2 focus:ring-cyan-700" type="text" placeholder="Ex. Relinium SAS" @blur="markTouched('organizationName')">
                  <span v-if="shouldShowFieldIssue('organizationName')" class="mt-2 block text-xs font-medium text-red-700">{{ fieldIssue('organizationName') }}</span>
                </label>
                <label class="block text-sm font-semibold text-slate-700">Type
                  <select v-model="organizationType" class="mt-2 h-11 w-full rounded-lg bg-slate-50 px-3 text-sm outline-none ring-1 ring-slate-200 transition focus:bg-white focus:ring-2 focus:ring-cyan-700">
                    <option value="entreprise">Entreprise</option>
                    <option value="association">Association</option>
                    <option value="collectivite">Collectivité</option>
                    <option value="independant">Indépendant</option>
                    <option value="autre">Autre</option>
                  </select>
                </label>
                <label class="block text-sm font-semibold text-slate-700">SIREN/SIRET ou identifiant légal
                  <input v-model="legalIdentifier" :maxlength="maxLengths.legalIdentifier" class="mt-2 h-11 w-full rounded-lg bg-slate-50 px-3 text-sm outline-none ring-1 ring-slate-200 transition focus:bg-white focus:ring-2 focus:ring-cyan-700" type="text" placeholder="Ex. 123 456 789" @blur="markTouched('legalIdentifier')">
                  <span v-if="shouldShowFieldIssue('legalIdentifier')" class="mt-2 block text-xs font-medium text-red-700">{{ fieldIssue('legalIdentifier') }}</span>
                </label>
                <label class="block text-sm font-semibold text-slate-700">Pays
                  <input v-model="country" :maxlength="maxLengths.country" class="mt-2 h-11 w-full rounded-lg bg-slate-50 px-3 text-sm outline-none ring-1 ring-slate-200 transition focus:bg-white focus:ring-2 focus:ring-cyan-700" type="text" placeholder="France" @blur="markTouched('country')">
                  <span v-if="shouldShowFieldIssue('country')" class="mt-2 block text-xs font-medium text-red-700">{{ fieldIssue('country') }}</span>
                </label>
                <label class="block text-sm font-semibold text-slate-700 sm:col-span-2">Site web officiel
                  <input v-model="officialWebsite" :maxlength="maxLengths.officialWebsite" class="mt-2 h-11 w-full rounded-lg bg-slate-50 px-3 text-sm outline-none ring-1 ring-slate-200 transition focus:bg-white focus:ring-2 focus:ring-cyan-700" type="url" placeholder="https://exemple.fr" @blur="markTouched('officialWebsite')">
                  <span v-if="shouldShowFieldIssue('officialWebsite')" class="mt-2 block text-xs font-medium text-red-700">{{ fieldIssue('officialWebsite') }}</span>
                </label>
              </div>
            </section>

            <section>
              <h2 class="text-lg font-semibold text-slate-950">Vos coordonnées</h2>
              <div class="mt-4 grid gap-4 sm:grid-cols-2">
                <label class="block text-sm font-semibold text-slate-700">Nom/prénom
                  <input v-model="contactName" :maxlength="maxLengths.contactName" class="mt-2 h-11 w-full rounded-lg bg-slate-50 px-3 text-sm outline-none ring-1 ring-slate-200 transition focus:bg-white focus:ring-2 focus:ring-cyan-700" type="text" placeholder="Ex. Claire Martin" @blur="markTouched('contactName')">
                  <span v-if="shouldShowFieldIssue('contactName')" class="mt-2 block text-xs font-medium text-red-700">{{ fieldIssue('contactName') }}</span>
                </label>
                <label class="block text-sm font-semibold text-slate-700">Email professionnel
                  <input v-model="email" :maxlength="maxLengths.email" class="mt-2 h-11 w-full rounded-lg bg-slate-50 px-3 text-sm outline-none ring-1 ring-slate-200 transition focus:bg-white focus:ring-2 focus:ring-cyan-700" type="email" placeholder="vous@organisation.fr" @blur="markTouched('email')">
                  <span v-if="shouldShowFieldIssue('email')" class="mt-2 block text-xs font-medium text-red-700">{{ fieldIssue('email') }}</span>
                </label>
                <label class="block text-sm font-semibold text-slate-700">Téléphone professionnel
                  <input v-model="phone" :maxlength="maxLengths.phone" class="mt-2 h-11 w-full rounded-lg bg-slate-50 px-3 text-sm outline-none ring-1 ring-slate-200 transition focus:bg-white focus:ring-2 focus:ring-cyan-700" type="tel" placeholder="01 23 45 67 89" @blur="markTouched('phone')">
                  <span v-if="shouldShowFieldIssue('phone')" class="mt-2 block text-xs font-medium text-red-700">{{ fieldIssue('phone') }}</span>
                </label>
                <label class="block text-sm font-semibold text-slate-700">Fonction
                  <input v-model="role" :maxlength="maxLengths.role" class="mt-2 h-11 w-full rounded-lg bg-slate-50 px-3 text-sm outline-none ring-1 ring-slate-200 transition focus:bg-white focus:ring-2 focus:ring-cyan-700" type="text" placeholder="Ex. Responsable conformité" @blur="markTouched('role')">
                  <span v-if="shouldShowFieldIssue('role')" class="mt-2 block text-xs font-medium text-red-700">{{ fieldIssue('role') }}</span>
                </label>
              </div>
            </section>

            <section>
              <h2 class="text-lg font-semibold text-slate-950">Justificatif</h2>
              <div class="mt-4 rounded-lg border border-dashed border-slate-300 bg-slate-50 p-4">
                <p class="text-sm font-semibold text-slate-800">Extrait Kbis / document légal</p>
                <p class="mt-1 text-sm text-slate-600">Téléversement sécurisé à venir. Aucun fichier n’est stocké dans cette version.</p>
                <button class="mt-3 inline-flex h-9 cursor-not-allowed items-center rounded-lg bg-slate-200 px-3 text-sm font-semibold text-slate-500" type="button" disabled>
                  Upload indisponible
                </button>
              </div>
            </section>
          </div>

          <label class="mt-8 flex gap-3 rounded-lg bg-slate-50 p-4 text-sm leading-6 text-slate-700 ring-1 ring-slate-200">
            <input v-model="authorized" class="mt-1 h-4 w-4 rounded border-slate-300 text-cyan-800 focus:ring-cyan-700" type="checkbox">
            <span>{{ isIndividual ? 'Je confirme que cette demande ne contient aucun mot de passe, token, clé API ou donnée bancaire.' : 'Je suis autorisé à demander l’ouverture d’un espace Relinium pour cette organisation.' }}</span>
          </label>
        </div>

        <aside class="space-y-5 lg:pt-0">
          <section class="rounded-lg bg-white p-5 shadow-sm ring-1 ring-slate-200/70">
            <h2 class="text-base font-semibold text-slate-950">Vérifications prévues</h2>
            <ul class="mt-4 space-y-3 text-sm text-slate-700">
              <li v-for="step in verificationSteps" :key="step" class="flex items-center gap-3">
                <span class="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-cyan-50 text-xs font-semibold text-cyan-800 ring-1 ring-cyan-100">✓</span>
                <span>{{ step }}</span>
              </li>
            </ul>
          </section>

          <section class="rounded-lg bg-white p-5 shadow-sm ring-1 ring-slate-200/70">
            <p class="text-sm leading-6 text-slate-700">
              Le front aide à éviter les erreurs, mais la validation serveur reste indispensable avant activation.
            </p>
            <p v-if="errorMessage" class="mt-4 rounded-lg bg-red-50 p-3 text-sm text-red-800 ring-1 ring-red-200">{{ errorMessage }}</p>
            <p v-if="successMessage" class="mt-4 rounded-lg bg-emerald-50 p-3 text-sm text-emerald-800 ring-1 ring-emerald-200">{{ successMessage }}</p>
            <button
              class="mt-4 inline-flex min-h-11 w-full items-center justify-center rounded-lg px-4 py-2 text-center text-sm font-semibold transition disabled:cursor-not-allowed disabled:bg-slate-200 disabled:text-slate-500"
              :class="formValid ? 'bg-cyan-950 text-white shadow-sm hover:bg-cyan-900' : 'bg-slate-200 text-slate-500'"
              type="submit"
              :disabled="loading || !formValid"
            >
              {{ submitLabel }}
            </button>
            <NuxtLink class="mt-3 inline-flex text-sm font-semibold text-slate-600 hover:text-slate-950" to="/connexion">Retour aux accès</NuxtLink>
          </section>
        </aside>
      </form>
    </div>
  </section>
</template>

<style scoped>
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-2px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
