<script setup lang="ts">
const {
  pending,
  error,
  isAuthenticated,
  displayName,
  providerConfigured,
  providerName,
  currentOrganization
} = useAuthStatus()

const loginNote = computed(() => {
  if (pending.value) return 'Vérification en cours.'
  if (error.value || !providerConfigured.value) return 'Connexion organisation à configurer.'
  return providerName.value ? `Prêt avec ${providerName.value}.` : 'Connexion organisation prête.'
})

const loginReadyMessage = ref('')

function prepareOrganizationLogin(): void {
  loginReadyMessage.value = 'La redirection OIDC sera activée avec le fournisseur d’identité.'
}
</script>

<template>
  <section class="w-full bg-slate-100 px-3 py-8 sm:px-6 lg:px-8">
    <div class="mx-auto max-w-6xl">
      <div class="flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
        <div class="max-w-2xl">
          <p v-if="isAuthenticated" class="mb-2 text-sm font-semibold text-emerald-800">
            Session active pour {{ displayName }} · {{ currentOrganization?.name || 'Organisation non sélectionnée' }}
          </p>
          <h1 class="text-3xl font-semibold text-slate-950">Accéder à Relinium</h1>
          <p class="mt-3 text-slate-700">
            Créez un accès, connectez-vous ou demandez des droits administrateur.
          </p>
        </div>
        <p class="max-w-sm text-sm text-slate-500">
          Vos mots de passe professionnels ne sont pas stockés dans Relinium.
        </p>
      </div>

      <div class="mt-7 grid gap-5 lg:grid-cols-2">
        <section class="rounded-xl bg-cyan-50/80 p-2 ring-1 ring-cyan-100 sm:p-4">
          <div class="mb-3 flex items-center justify-between gap-3 px-1">
            <h2 class="text-sm font-semibold uppercase tracking-normal text-cyan-950">Créer un accès</h2>
            <span class="h-px flex-1 bg-cyan-200/70" aria-hidden="true" />
          </div>

          <div class="grid gap-3 sm:grid-cols-2">
            <article class="flex min-h-[220px] min-w-0 flex-col rounded-lg bg-white p-4 shadow-sm ring-1 ring-cyan-100/80">
              <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-cyan-100 text-cyan-900" aria-hidden="true">
                <svg class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="8" r="4" />
                  <path d="M5 21a7 7 0 0 1 14 0" />
                </svg>
              </div>
              <h3 class="mt-4 text-lg font-semibold text-slate-950">Compte individuel</h3>
              <p class="mt-2 break-words text-sm leading-6 text-slate-600">Pour intervenir seul ou préparer un dossier personnel.</p>
              <div class="mt-auto pt-5">
                <NuxtLink class="inline-flex min-h-10 w-full min-w-0 items-center justify-center rounded-md bg-cyan-950 px-3 py-2 text-center text-sm font-semibold leading-tight text-white transition hover:bg-cyan-900" to="/creation-compte?type=individual">
                  Créer mon compte
                </NuxtLink>
                <p class="mt-3 text-xs font-semibold text-cyan-900">Validation avant activation.</p>
              </div>
            </article>

            <article class="flex min-h-[220px] min-w-0 flex-col rounded-lg bg-white p-4 shadow-sm ring-1 ring-cyan-100/80">
              <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-cyan-100 text-cyan-900" aria-hidden="true">
                <svg class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M4 21h16" />
                  <path d="M6 21V7l6-4 6 4v14" />
                  <path d="M9 10h.01M12 10h.01M15 10h.01M9 14h.01M12 14h.01M15 14h.01" />
                </svg>
              </div>
              <h3 class="mt-4 text-lg font-semibold text-cyan-950">Compte entreprise</h3>
              <p class="mt-2 break-words text-sm leading-6 text-slate-600">Pour déclarer une organisation et gérer ses sources.</p>
              <div class="mt-auto pt-5">
                <NuxtLink class="inline-flex min-h-10 w-full min-w-0 items-center justify-center rounded-md bg-cyan-800 px-3 py-2 text-center text-sm font-semibold leading-tight text-white transition hover:bg-cyan-700" to="/creation-compte?type=company">
                  Créer l’espace entreprise
                </NuxtLink>
                <p class="mt-3 text-xs font-semibold text-cyan-900">KYC organisation requis.</p>
              </div>
            </article>
          </div>
        </section>

        <section class="rounded-xl bg-slate-200/55 p-2 ring-1 ring-slate-200 sm:p-4">
          <div class="mb-3 flex items-center justify-between gap-3 px-1">
            <h2 class="text-sm font-semibold uppercase tracking-normal text-slate-800">Accéder à Relinium</h2>
            <span class="h-px flex-1 bg-slate-300" aria-hidden="true" />
          </div>

          <div class="grid gap-3 sm:grid-cols-2">
            <article class="flex min-h-[220px] min-w-0 flex-col rounded-lg bg-white p-4 shadow-sm ring-1 ring-slate-200">
              <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-slate-100 text-slate-800" aria-hidden="true">
                <svg class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="8" cy="15" r="4" />
                  <path d="M12 15h8M17 15v-3M20 15v-3" />
                </svg>
              </div>
              <h3 class="mt-4 text-lg font-semibold text-slate-950">Déjà inscrit</h3>
              <p class="mt-2 break-words text-sm leading-6 text-slate-600">Connectez-vous avec l’identité de votre organisation.</p>
              <div class="mt-auto pt-5">
                <button
                  class="inline-flex min-h-10 w-full min-w-0 items-center justify-center rounded-md bg-slate-950 px-3 py-2 text-center text-sm font-semibold leading-tight text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:bg-slate-200 disabled:text-slate-500"
                  type="button"
                  :disabled="!providerConfigured"
                  @click="prepareOrganizationLogin"
                >
                  Se connecter
                </button>
                <p class="mt-3 text-xs font-semibold text-slate-600">{{ loginNote }}</p>
                <p v-if="loginReadyMessage" class="mt-2 text-xs text-slate-500">{{ loginReadyMessage }}</p>
              </div>
            </article>

            <article class="flex min-h-[220px] min-w-0 flex-col rounded-lg bg-white p-4 shadow-sm ring-1 ring-slate-200">
              <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-indigo-50 text-indigo-900" aria-hidden="true">
                <svg class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M12 3 19 6v5c0 5-3 8-7 10-4-2-7-5-7-10V6l7-3Z" />
                  <path d="m9.5 12 1.7 1.7L15 10" />
                </svg>
              </div>
              <h3 class="mt-4 text-lg font-semibold text-slate-950">Accès administrateur</h3>
              <p class="mt-2 break-words text-sm leading-6 text-slate-600">Pour inviter des collaborateurs et gérer les droits.</p>
              <div class="mt-auto pt-5">
                <NuxtLink class="inline-flex min-h-10 w-full min-w-0 items-center justify-center rounded-md bg-white px-3 py-2 text-center text-sm font-semibold leading-tight text-slate-800 ring-1 ring-slate-300 transition hover:bg-slate-50" to="/admin-acces">
                  Demander les droits admin
                </NuxtLink>
                <p class="mt-3 text-xs font-semibold text-indigo-900">Vérification renforcée.</p>
              </div>
            </article>
          </div>
        </section>
      </div>
    </div>
  </section>
</template>
