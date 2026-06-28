<script setup lang="ts">
const { graphql } = useGraphqlRequest()
const route = useRoute()
const email = ref('')
const organizationHint = ref('')
const requestedRole = ref(typeof route.query.role === 'string' ? route.query.role : 'viewer')
const initialContext = route.query.type === 'individual' ? 'individuel' : typeof route.query.contexte === 'string' ? route.query.contexte : 'utilisateur'
const context = ref(initialContext)
const phone = ref('')
const messageRedacted = ref('')
const erreur = ref('')
const succes = ref('')
const chargement = ref(false)

async function envoyer(): Promise<void> {
  chargement.value = true
  erreur.value = ''
  succes.value = ''
  try {
    const data = await graphql<{ requestAccess: { emailRedacted: string, status: string } }>(`
      mutation RequestAccess($input: RequestAccessInput!) {
        requestAccess(input: $input) { id emailRedacted status }
      }
    `, {
      input: {
        email: email.value,
        organizationHint: organizationHint.value,
        requestedRole: requestedRole.value,
        messageRedacted: [
          `Contexte: ${context.value}`,
          `Telephone professionnel: ${phone.value || 'non renseigne'}`,
          `Motif: ${messageRedacted.value || 'non renseigne'}`
        ].join('\n')
      }
    })
    succes.value = `Demande enregistrée pour ${data.requestAccess.emailRedacted}.`
    email.value = ''
    organizationHint.value = ''
    messageRedacted.value = ''
    phone.value = ''
    context.value = 'utilisateur'
    requestedRole.value = 'viewer'
  } catch (error) {
    erreur.value = error instanceof Error ? error.message : 'Demande impossible.'
  } finally {
    chargement.value = false
  }
}
</script>

<template>
  <section class="w-full bg-slate-50 px-4 py-8 sm:px-6 lg:px-8">
    <div class="mx-auto max-w-3xl">
      <h1 class="text-3xl font-semibold text-slate-950">Demande d’accès</h1>
      <p class="mt-3 text-slate-700">
        Préparez une demande d’accès sans mot de passe. Un responsable devra valider l’organisation et les droits avant activation.
      </p>
      <form class="mt-6 space-y-4 rounded-lg border border-slate-200 bg-white p-5" @submit.prevent="envoyer">
        <p class="rounded-md bg-amber-50 p-3 text-sm text-amber-900 ring-1 ring-amber-200">
          Ne saisissez aucun mot de passe, token, clé API ou information bancaire.
        </p>
        <label class="block text-sm font-semibold text-slate-700">Contexte
          <select v-model="context" class="mt-1 h-10 w-full rounded-md border border-slate-300 px-3 text-sm">
            <option value="utilisateur">Utilisateur</option>
            <option value="individuel">Compte individuel</option>
            <option value="administrateur">Administrateur</option>
            <option value="creation-organisation">Création organisation</option>
          </select>
        </label>
        <label class="block text-sm font-semibold text-slate-700">Email professionnel
          <input v-model="email" class="mt-1 h-10 w-full rounded-md border border-slate-300 px-3 text-sm" type="email" required>
        </label>
        <label class="block text-sm font-semibold text-slate-700">Organisation
          <input v-model="organizationHint" class="mt-1 h-10 w-full rounded-md border border-slate-300 px-3 text-sm" type="text">
        </label>
        <label class="block text-sm font-semibold text-slate-700">Rôle demandé
          <select v-model="requestedRole" class="mt-1 h-10 w-full rounded-md border border-slate-300 px-3 text-sm">
            <option value="viewer">Lecteur</option>
            <option value="operator">Opérateur</option>
            <option value="analyst">Analyste</option>
            <option value="admin">Administrateur</option>
          </select>
        </label>
        <label class="block text-sm font-semibold text-slate-700">Téléphone professionnel optionnel
          <input v-model="phone" class="mt-1 h-10 w-full rounded-md border border-slate-300 px-3 text-sm" type="tel">
        </label>
        <label class="block text-sm font-semibold text-slate-700">Motif
          <textarea v-model="messageRedacted" class="mt-1 min-h-28 w-full rounded-md border border-slate-300 px-3 py-2 text-sm" placeholder="Expliquez le besoin d’accès, sans secret." />
        </label>
        <p v-if="erreur" class="rounded-md bg-red-50 p-3 text-sm text-red-800 ring-1 ring-red-200">{{ erreur }}</p>
        <p v-if="succes" class="rounded-md bg-emerald-50 p-3 text-sm text-emerald-800 ring-1 ring-emerald-200">{{ succes }}</p>
        <button class="inline-flex h-10 items-center justify-center rounded-md bg-cyan-950 px-4 text-sm font-semibold text-white disabled:opacity-60" type="submit" :disabled="chargement">
          Envoyer la demande
        </button>
      </form>
    </div>
  </section>
</template>
