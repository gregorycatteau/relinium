<script setup lang="ts">
type AuthStatus = {
  authenticated: boolean
  mode: string
  mfaRequired: boolean
  mfaEnrolled: boolean
  oidcConfigured: boolean
  providerConfigured: boolean
  mfaProviderStatus: string
}

const { graphql } = useGraphqlRequest()
const req = useAsyncData('security-page', async () => {
  const response = await graphql<{ authStatus: AuthStatus }>('query SecurityPage { authStatus { authenticated mode mfaRequired mfaEnrolled oidcConfigured providerConfigured mfaProviderStatus } }')
  return response.authStatus
})
</script>

<template>
  <section class="w-full bg-slate-50 px-4 py-8 sm:px-6 lg:px-8">
    <div class="mx-auto max-w-3xl">
      <h1 class="text-3xl font-semibold text-slate-950">Sécurité</h1>
      <div class="mt-6 space-y-4 rounded-lg border border-slate-200 bg-white p-5">
        <p v-if="!req.data.value?.authenticated" class="text-slate-700">Aucune session active.</p>
        <template v-else>
          <div>
            <h2 class="text-lg font-semibold text-slate-950">Identité organisationnelle</h2>
            <p class="mt-1 text-sm text-slate-600">Mode actuel: {{ req.data.value.mode }}. Les mots de passe professionnels ne sont pas stockés dans Relinium.</p>
          </div>
          <div>
            <h2 class="text-lg font-semibold text-slate-950">MFA</h2>
            <p class="mt-1 text-sm text-slate-600">Requis: {{ req.data.value.mfaRequired ? 'oui' : 'non' }} · Enrôlé: {{ req.data.value.mfaEnrolled ? 'oui' : 'non' }}</p>
            <p class="mt-1 text-sm text-slate-600">Provider MFA: {{ req.data.value.mfaProviderStatus === 'planned' ? 'prévu' : req.data.value.mfaProviderStatus }}</p>
            <p class="mt-2 rounded-md bg-amber-50 p-3 text-sm text-amber-900 ring-1 ring-amber-200">
              TOTP sera ajouté avec une librairie éprouvée. Aucun pseudo-MFA maison n’est actif dans cette phase.
            </p>
          </div>
        </template>
      </div>
    </div>
  </section>
</template>
