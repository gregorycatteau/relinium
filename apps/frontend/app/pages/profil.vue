<script setup lang="ts">
type AuthData = {
  currentUser?: {
    displayName: string
    emailRedacted: string
    locale: string
    timezone: string
    selectedOrganization?: { name: string } | null
  } | null
  myMemberships: Array<{ role: string, status: string, organization: { name: string } }>
}

const { graphql } = useGraphqlRequest()
const displayName = ref('')
const locale = ref('fr-FR')
const timezone = ref('Europe/Paris')
const erreur = ref('')
const message = ref('')

const req = useAsyncData('profile-page', () => graphql<AuthData>(`
  query ProfilePage {
    currentUser { displayName emailRedacted locale timezone selectedOrganization { name } }
    myMemberships { role status organization { name } }
  }
`))

watchEffect(() => {
  const user = req.data.value?.currentUser
  if (user) {
    displayName.value = user.displayName
    locale.value = user.locale
    timezone.value = user.timezone
  }
})

async function enregistrer(): Promise<void> {
  erreur.value = ''
  message.value = ''
  try {
    await graphql(`
      mutation UpdateProfile($input: UpdateMyProfileInput!) {
        updateMyProfile(input: $input) { displayName locale timezone }
      }
    `, { input: { displayName: displayName.value, locale: locale.value, timezone: timezone.value } })
    message.value = 'Profil mis à jour.'
    await req.refresh()
  } catch (error) {
    erreur.value = error instanceof Error ? error.message : 'Mise à jour impossible.'
  }
}
</script>

<template>
  <section class="w-full bg-slate-50 px-4 py-8 sm:px-6 lg:px-8">
    <div class="mx-auto max-w-4xl">
      <h1 class="text-3xl font-semibold text-slate-950">Profil</h1>
      <div v-if="!req.data.value?.currentUser" class="mt-6 rounded-lg border border-slate-200 bg-white p-5">
        <p class="text-slate-700">Aucune session active.</p>
        <NuxtLink class="mt-3 inline-flex h-9 items-center rounded-md bg-cyan-950 px-3 text-sm font-semibold text-white" to="/connexion">Connexion</NuxtLink>
      </div>
      <form v-else class="mt-6 space-y-4 rounded-lg border border-slate-200 bg-white p-5" @submit.prevent="enregistrer">
        <p class="text-sm text-slate-600">{{ req.data.value.currentUser.emailRedacted }} · {{ req.data.value.currentUser.selectedOrganization?.name || 'Organisation non sélectionnée' }}</p>
        <label class="block text-sm font-semibold text-slate-700">Nom affiché
          <input v-model="displayName" class="mt-1 h-10 w-full rounded-md border border-slate-300 px-3 text-sm" type="text">
        </label>
        <label class="block text-sm font-semibold text-slate-700">Langue
          <input v-model="locale" class="mt-1 h-10 w-full rounded-md border border-slate-300 px-3 text-sm" type="text">
        </label>
        <label class="block text-sm font-semibold text-slate-700">Fuseau horaire
          <input v-model="timezone" class="mt-1 h-10 w-full rounded-md border border-slate-300 px-3 text-sm" type="text">
        </label>
        <p v-if="erreur" class="rounded-md bg-red-50 p-3 text-sm text-red-800 ring-1 ring-red-200">{{ erreur }}</p>
        <p v-if="message" class="rounded-md bg-emerald-50 p-3 text-sm text-emerald-800 ring-1 ring-emerald-200">{{ message }}</p>
        <button class="inline-flex h-10 items-center rounded-md bg-cyan-950 px-4 text-sm font-semibold text-white" type="submit">Enregistrer</button>
      </form>
    </div>
  </section>
</template>
