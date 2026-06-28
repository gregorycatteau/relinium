<script setup lang="ts">
type FieldKey = 'firstName' | 'lastName' | 'organizationName' | 'legalIdentifier' | 'country' | 'officialWebsite' | 'contactName' | 'email' | 'phone' | 'role'
type PasswordStrength = 'faible' | 'correct' | 'fort'

const { graphql } = useGraphqlRequest()
const route = useRoute()

const accountType = computed(() => route.query.type === 'individual' ? 'individual' : 'company')
const isIndividual = computed(() => accountType.value === 'individual')

const firstName = ref('')
const lastName = ref('')
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
const avatarInput = ref<HTMLInputElement | null>(null)
const avatarPreviewUrl = ref('')
const avatarObjectUrl = ref('')
const avatarRemoteUrl = ref('')
const avatarSourceLabel = ref('')
const avatarError = ref('')
const authorized = ref(false)
const loading = ref(false)
const submitted = ref(false)
const errorMessage = ref('')
const successMessage = ref('')
const touched = reactive<Record<string, boolean>>({})

const fieldLabels: Record<FieldKey, string> = {
  firstName: 'Prénom',
  lastName: 'Nom',
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
  firstName: 48,
  lastName: 48,
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
const frenchNameError = 'Veuillez entrer un Nom ou un Prénom valide. Seuls les caractères utf8 FR sont acceptés.'
const frenchUppercaseLetters = 'A-ZÀÂÄÇÉÈÊËÎÏÔÖÙÛÜŸÆŒ'
const frenchLowercaseLetters = 'a-zàâäçéèêëîïôöùûüÿæœ'
const frenchNameCharacters = new RegExp(`^[${frenchUppercaseLetters}${frenchLowercaseLetters}-]+$`, 'u')
const frenchNameUppercaseSegment = new RegExp(`^[${frenchUppercaseLetters}]+$`, 'u')
const frenchNameCapitalizedSegment = new RegExp(`^[${frenchUppercaseLetters}][${frenchLowercaseLetters}]+$`, 'u')
const maxAvatarSize = 5 * 1024 * 1024

const pageTitle = computed(() => isIndividual.value ? 'Créer un compte individuel' : 'Créer un compte entreprise')
const pageIntro = computed(() => isIndividual.value
  ? 'Préparez votre accès personnel en quelques informations. L’activation reste vérifiée avant ouverture.'
  : 'Préparez l’ouverture d’un espace Relinium pour votre organisation. Cette étape ne valide pas automatiquement votre compte.'
)
const individualName = computed(() => [firstName.value.trim(), lastName.value.trim()].filter(Boolean).join(' '))
const displayName = computed(() => individualName.value || organizationName.value.trim() || contactName.value.trim())
const avatarInitials = computed(() => {
  const source = displayName.value || 'Votre nom'
  return source
    .split(/\s+/)
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0]?.toUpperCase())
    .join('') || 'VN'
})
const hasAvatarPreview = computed(() => avatarPreviewUrl.value.length > 0)

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
  ? ['lastName', 'firstName', 'email', 'phone', 'role']
  : ['organizationName', 'legalIdentifier', 'country', 'officialWebsite', 'contactName', 'email', 'phone', 'role']
)

const requiredFields = computed<FieldKey[]>(() => isIndividual.value
  ? ['lastName', 'firstName', 'email', 'phone', 'role']
  : ['organizationName', 'country', 'contactName', 'email']
)

const values = computed<Record<FieldKey, string>>(() => ({
  firstName: firstName.value,
  lastName: lastName.value,
  organizationName: organizationName.value,
  legalIdentifier: legalIdentifier.value,
  country: country.value,
  officialWebsite: officialWebsite.value,
  contactName: contactName.value,
  email: email.value,
  phone: phone.value,
  role: role.value
}))

function isValidFrenchName(value: string): boolean {
  if (value.length < 2 || value.length > 48) return false
  if (!frenchNameCharacters.test(value)) return false
  return value.split('-').every((segment) => {
    if (segment.length < 2) return false
    return frenchNameUppercaseSegment.test(segment) || frenchNameCapitalizedSegment.test(segment)
  })
}

// Ces garde-fous UX complètent les validations serveur, ils ne sont pas une frontière de sécurité.
function fieldIssue(field: FieldKey): string {
  const value = values.value[field].trim()
  if (requiredFields.value.includes(field) && !value) return 'Ce champ est nécessaire.'
  if ((field === 'firstName' || field === 'lastName') && value && !isValidFrenchName(value)) return frenchNameError
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

function isFieldComplete(field: FieldKey): boolean {
  return values.value[field].trim().length > 0 && fieldValid(field)
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

function clearAvatarObjectUrl(): void {
  if (!avatarObjectUrl.value) return
  URL.revokeObjectURL(avatarObjectUrl.value)
  avatarObjectUrl.value = ''
}

function clearAvatar(): void {
  clearAvatarObjectUrl()
  avatarPreviewUrl.value = ''
  avatarRemoteUrl.value = ''
  avatarSourceLabel.value = ''
  avatarError.value = ''
  if (avatarInput.value) avatarInput.value.value = ''
}

function setAvatarFile(file: File | null): void {
  avatarError.value = ''
  if (!file) return
  if (!file.type.startsWith('image/')) {
    avatarError.value = 'Choisissez une image valide.'
    return
  }
  if (file.size > maxAvatarSize) {
    avatarError.value = 'Image trop lourde. Limite: 5 Mo.'
    return
  }
  clearAvatarObjectUrl()
  const objectUrl = URL.createObjectURL(file)
  avatarObjectUrl.value = objectUrl
  avatarPreviewUrl.value = objectUrl
  avatarRemoteUrl.value = ''
  avatarSourceLabel.value = file.name
}

function openAvatarPicker(): void {
  avatarInput.value?.click()
}

function handleAvatarInput(event: Event): void {
  const input = event.target as HTMLInputElement
  setAvatarFile(input.files?.[0] ?? null)
}

function handleAvatarDrop(event: DragEvent): void {
  setAvatarFile(event.dataTransfer?.files?.[0] ?? null)
}

function useRemoteAvatar(): void {
  const value = avatarRemoteUrl.value.trim()
  avatarError.value = ''
  if (!value) return
  try {
    const url = new URL(value)
    if (!['http:', 'https:'].includes(url.protocol)) {
      avatarError.value = 'Utilisez une URL image en HTTPS.'
      return
    }
    clearAvatarObjectUrl()
    avatarPreviewUrl.value = url.toString()
    avatarSourceLabel.value = url.hostname
  } catch {
    avatarError.value = 'URL image invalide.'
  }
}

onBeforeUnmount(() => {
  clearAvatarObjectUrl()
})

const formValid = computed(() => {
  const fieldsValid = currentFields.value.every((field) => fieldValid(field))
  if (!fieldsValid) return false
  if (isIndividual.value) return passwordValid.value && passwordConfirmationValid.value
  if (!authorized.value) return false
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

const individualProgressSteps = computed(() => [
  { key: 'lastName', label: 'Nom', complete: isFieldComplete('lastName') },
  { key: 'firstName', label: 'Prénom', complete: isFieldComplete('firstName') },
  { key: 'email', label: 'Email', complete: isFieldComplete('email') },
  { key: 'phone', label: 'Téléphone', complete: isFieldComplete('phone') },
  { key: 'password', label: 'Mot de passe', complete: passwordValid.value },
  { key: 'passwordConfirmation', label: 'Confirmation', complete: passwordConfirmationValid.value },
  { key: 'role', label: 'Usage prévu', complete: isFieldComplete('role') }
])

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
    const trimmedFirstName = normalizeText('firstName', firstName.value)
    const trimmedLastName = normalizeText('lastName', lastName.value)
    const trimmedName = normalizeText('organizationName', organizationName.value)
    const trimmedIndividualName = [trimmedFirstName, trimmedLastName].filter(Boolean).join(' ')
    const trimmedEmail = normalizeText('email', email.value)
    const trimmedPhone = normalizeText('phone', phone.value)
    const trimmedRole = normalizeText('role', role.value)
    const messageRedacted = isIndividual.value
      ? [
          'Contexte: creation compte individuel',
          `Prenom: ${trimmedFirstName}`,
          `Nom: ${trimmedLastName}`,
          `Telephone: ${trimmedPhone}`,
          `Usage prevu: ${trimmedRole}`,
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
        organizationHint: isIndividual.value ? trimmedIndividualName : trimmedName,
        requestedRole: isIndividual.value ? 'viewer' : 'admin',
        messageRedacted
      }
    })

    successMessage.value = isIndividual.value
      ? `Demande préparée pour ${data.requestAccess.emailRedacted}. L’activation nécessitera une validation.`
      : `Demande préparée pour ${data.requestAccess.emailRedacted}. Aucun justificatif n’a été téléversé.`
    organizationName.value = ''
    firstName.value = ''
    lastName.value = ''
    legalIdentifier.value = ''
    officialWebsite.value = ''
    contactName.value = ''
    email.value = ''
    phone.value = ''
    role.value = ''
    password.value = ''
    passwordConfirmation.value = ''
    clearAvatar()
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
                <label class="block text-sm font-semibold transition" :class="isFieldComplete('lastName') ? 'text-emerald-700' : 'text-slate-700'">
                  <span class="inline-flex items-center gap-1">Nom <span v-if="isFieldComplete('lastName')" aria-hidden="true">✓</span></span>
                  <span class="relative mt-2 block">
                    <span class="pointer-events-none absolute inset-y-0 left-3 flex items-center text-slate-400" aria-hidden="true">◎</span>
                    <input
                      v-model="lastName"
                      :maxlength="maxLengths.lastName"
                      :aria-invalid="shouldShowFieldIssue('lastName')"
                      class="h-12 w-full rounded-lg bg-slate-50 py-2 pl-10 pr-10 text-sm outline-none ring-1 ring-slate-200 transition focus:bg-white focus:ring-2 focus:ring-cyan-700"
                      :class="shouldShowFieldIssue('lastName') ? 'ring-red-300 focus:ring-red-500' : fieldValid('lastName') && lastName.trim() ? 'ring-emerald-200' : ''"
                      type="text"
                      autocomplete="family-name"
                      placeholder="Ex. Catteau"
                      @blur="markTouched('lastName')"
                    >
                    <span v-if="fieldValid('lastName') && lastName.trim()" class="pointer-events-none absolute inset-y-0 right-3 flex items-center text-emerald-600" aria-hidden="true">✓</span>
                  </span>
                  <span v-if="shouldShowFieldIssue('lastName')" class="mt-2 block animate-[fadeIn_.18s_ease-out] text-xs font-medium text-red-700">{{ fieldIssue('lastName') }}</span>
                </label>

                <label class="block text-sm font-semibold transition" :class="isFieldComplete('firstName') ? 'text-emerald-700' : 'text-slate-700'">
                  <span class="inline-flex items-center gap-1">Prénom <span v-if="isFieldComplete('firstName')" aria-hidden="true">✓</span></span>
                  <span class="relative mt-2 block">
                    <span class="pointer-events-none absolute inset-y-0 left-3 flex items-center text-slate-400" aria-hidden="true">◎</span>
                    <input
                      v-model="firstName"
                      :maxlength="maxLengths.firstName"
                      :aria-invalid="shouldShowFieldIssue('firstName')"
                      class="h-12 w-full rounded-lg bg-slate-50 py-2 pl-10 pr-10 text-sm outline-none ring-1 ring-slate-200 transition focus:bg-white focus:ring-2 focus:ring-cyan-700"
                      :class="shouldShowFieldIssue('firstName') ? 'ring-red-300 focus:ring-red-500' : fieldValid('firstName') && firstName.trim() ? 'ring-emerald-200' : ''"
                      type="text"
                      autocomplete="given-name"
                      placeholder="Ex. Grégory"
                      @blur="markTouched('firstName')"
                    >
                    <span v-if="fieldValid('firstName') && firstName.trim()" class="pointer-events-none absolute inset-y-0 right-3 flex items-center text-emerald-600" aria-hidden="true">✓</span>
                  </span>
                  <span v-if="shouldShowFieldIssue('firstName')" class="mt-2 block animate-[fadeIn_.18s_ease-out] text-xs font-medium text-red-700">{{ fieldIssue('firstName') }}</span>
                </label>

                <label class="block text-sm font-semibold transition" :class="isFieldComplete('email') ? 'text-emerald-700' : 'text-slate-700'">
                  <span class="inline-flex items-center gap-1">Email <span v-if="isFieldComplete('email')" aria-hidden="true">✓</span></span>
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

                <label class="block text-sm font-semibold transition" :class="isFieldComplete('phone') ? 'text-emerald-700' : 'text-slate-700'">
                  <span class="inline-flex items-center gap-1">Téléphone <span v-if="isFieldComplete('phone')" aria-hidden="true">✓</span></span>
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
                <label class="block text-sm font-semibold transition" :class="passwordValid ? 'text-emerald-700' : 'text-slate-700'">
                  <span class="inline-flex items-center gap-1">Mot de passe <span v-if="passwordValid" aria-hidden="true">✓</span></span>
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

                <label class="block text-sm font-semibold transition" :class="passwordConfirmationValid ? 'text-emerald-700' : 'text-slate-700'">
                  <span class="inline-flex items-center gap-1">Confirmer le mot de passe <span v-if="passwordConfirmationValid" aria-hidden="true">✓</span></span>
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
              <div
                class="mt-4 rounded-lg bg-slate-50 p-4 ring-1 ring-slate-200"
                @dragover.prevent
                @drop.prevent="handleAvatarDrop"
              >
                <div class="flex flex-col items-center gap-4 sm:flex-row sm:items-start">
                  <div class="flex h-24 w-24 shrink-0 items-center justify-center overflow-hidden rounded-full bg-cyan-950 text-xl font-semibold text-white shadow-sm ring-4 ring-white">
                    <img v-if="hasAvatarPreview" class="h-full w-full object-cover" :src="avatarPreviewUrl" alt="Aperçu de la photo de profil">
                    <span v-else>{{ avatarInitials }}</span>
                  </div>
                  <div class="min-w-0 flex-1 text-center sm:text-left">
                    <div class="rounded-lg border border-dashed border-slate-300 bg-white p-4">
                      <p class="text-sm font-semibold text-slate-900">Ajoutez une image</p>
                      <p class="mt-1 text-sm leading-6 text-slate-600">Glissez une image ici, explorez ce PC, ou collez une URL d’image.</p>
                      <div class="mt-4 flex flex-col gap-2 sm:flex-row">
                        <button class="inline-flex min-h-10 items-center justify-center rounded-lg bg-cyan-950 px-4 py-2 text-sm font-semibold text-white transition hover:bg-cyan-900" type="button" @click="openAvatarPicker">
                          Explorer ce PC
                        </button>
                        <button v-if="hasAvatarPreview" class="inline-flex min-h-10 items-center justify-center rounded-lg bg-white px-4 py-2 text-sm font-semibold text-slate-700 ring-1 ring-slate-300 transition hover:bg-slate-50" type="button" @click="clearAvatar">
                          Retirer l’image
                        </button>
                      </div>
                      <input ref="avatarInput" class="sr-only" type="file" accept="image/png,image/jpeg,image/webp,image/gif,image/svg+xml" @change="handleAvatarInput">
                    </div>

                    <div class="mt-3 grid gap-2 sm:grid-cols-[minmax(0,1fr)_auto]">
                      <input
                        v-model="avatarRemoteUrl"
                        class="h-11 w-full rounded-lg bg-white px-3 text-sm outline-none ring-1 ring-slate-200 transition focus:ring-2 focus:ring-cyan-700"
                        type="url"
                        placeholder="https://exemple.fr/photo.jpg"
                        @keydown.enter.prevent="useRemoteAvatar"
                      >
                      <button class="inline-flex min-h-11 items-center justify-center rounded-lg bg-slate-900 px-4 py-2 text-sm font-semibold text-white transition hover:bg-slate-800" type="button" @click="useRemoteAvatar">
                        Utiliser l’URL
                      </button>
                    </div>

                    <div class="mt-3 flex flex-col gap-2 text-sm sm:flex-row sm:items-center sm:justify-between">
                      <p class="text-slate-600">PNG, JPG, WebP, GIF ou SVG. 5 Mo maximum.</p>
                      <p v-if="avatarSourceLabel" class="font-medium text-emerald-700">Image prête: {{ avatarSourceLabel }}</p>
                    </div>
                    <p v-if="avatarError" class="mt-2 animate-[fadeIn_.18s_ease-out] text-sm font-medium text-red-700">{{ avatarError }}</p>
                    <p class="mt-2 text-sm leading-6 text-slate-500">Aucun envoi backend dans cette étape: l’image sert à préparer l’aperçu du profil.</p>
                  </div>
                </div>
              </div>
            </section>

            <section>
              <h2 class="text-lg font-semibold text-slate-950">Usage prévu</h2>
              <label class="mt-4 block text-sm font-semibold transition" :class="isFieldComplete('role') ? 'text-emerald-700' : 'text-slate-700'">
                <span class="inline-flex items-center gap-1">Décrivez en une phrase pourquoi vous ouvrez un accès. <span v-if="isFieldComplete('role')" aria-hidden="true">✓</span></span>
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

          <label v-if="!isIndividual" class="mt-8 flex gap-3 rounded-lg bg-slate-50 p-4 text-sm leading-6 text-slate-700 ring-1 ring-slate-200">
            <input v-model="authorized" class="mt-1 h-4 w-4 rounded border-slate-300 text-cyan-800 focus:ring-cyan-700" type="checkbox">
            <span>Je suis autorisé à demander l’ouverture d’un espace Relinium pour cette organisation.</span>
          </label>
        </div>

        <aside class="space-y-5 lg:pt-0">
          <section class="rounded-lg bg-white p-5 shadow-sm ring-1 ring-slate-200/70">
            <h2 class="text-base font-semibold text-slate-950">{{ isIndividual ? 'Champs validés' : 'Vérifications prévues' }}</h2>
            <ul v-if="isIndividual" class="mt-4 space-y-3 text-sm">
              <li v-for="step in individualProgressSteps" :key="step.key" class="flex items-center gap-3">
                <span
                  class="flex h-6 w-6 shrink-0 items-center justify-center rounded-full text-xs font-semibold transition"
                  :class="step.complete ? 'bg-emerald-50 text-emerald-700 ring-1 ring-emerald-100' : 'bg-slate-100 text-slate-400 ring-1 ring-slate-200'"
                  aria-hidden="true"
                >
                  {{ step.complete ? '✓' : '' }}
                </span>
                <span class="transition" :class="step.complete ? 'font-semibold text-emerald-700' : 'text-slate-600'">{{ step.label }}</span>
              </li>
            </ul>
            <ul v-else class="mt-4 space-y-3 text-sm text-slate-700">
              <li v-for="step in verificationSteps" :key="step" class="flex items-center gap-3">
                <span class="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-cyan-50 text-xs font-semibold text-cyan-800 ring-1 ring-cyan-100">✓</span>
                <span>{{ step }}</span>
              </li>
            </ul>
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
