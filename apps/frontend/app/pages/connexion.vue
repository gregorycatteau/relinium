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
  if (pending.value) return 'Vérification de la connexion organisation.'
  if (error.value) return 'La connexion organisation n’est pas encore disponible depuis cet environnement.'
  if (providerConfigured.value) return `Connexion organisation prête${providerName.value ? ` avec ${providerName.value}` : ''}.`
  return 'Connexion organisation à configurer.'
})

const loginReadyMessage = ref('')

function prepareOrganizationLogin(): void {
  loginReadyMessage.value = 'La redirection vers le fournisseur d’identité sera raccordée lors de l’activation OIDC.'
}
</script>

<template>
  <section class="w-full bg-slate-50 px-4 py-8 sm:px-6 lg:px-8">
    <div class="mx-auto max-w-6xl">
      <div class="max-w-3xl">
        <p v-if="isAuthenticated" class="mb-3 text-sm font-semibold text-emerald-800">
          Session active pour {{ displayName }} · {{ currentOrganization?.name || 'Organisation non sélectionnée' }}
        </p>
        <h1 class="text-3xl font-semibold text-slate-950">Accéder à Relinium</h1>
        <p class="mt-3 max-w-2xl text-slate-700">
          Connectez-vous avec votre organisation, créez un accès entreprise ou préparez une demande de validation.
        </p>
      </div>

      <div class="mt-7 grid gap-4 lg:grid-cols-3">
        <article class="flex min-h-[260px] min-w-0 flex-col rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
          <div>
            <p class="text-xs font-semibold uppercase tracking-normal text-cyan-800">Utilisateur existant</p>
            <h2 class="mt-2 text-xl font-semibold text-slate-950">J’ai déjà un compte</h2>
            <p class="mt-3 break-words text-sm leading-6 text-slate-700">
              Utilisez l’identité de votre organisation pour accéder à votre espace Relinium.
            </p>
          </div>

          <div class="mt-auto pt-5">
            <button
              class="inline-flex h-10 w-full items-center justify-center rounded-md bg-cyan-950 px-4 text-sm font-semibold text-white transition hover:bg-cyan-900 disabled:cursor-not-allowed disabled:bg-slate-200 disabled:text-slate-500"
              type="button"
              :disabled="!providerConfigured"
              @click="prepareOrganizationLogin"
            >
              Se connecter
            </button>
            <p class="mt-3 text-sm text-slate-600">{{ loginNote }}</p>
            <p v-if="loginReadyMessage" class="mt-2 text-sm text-slate-600">{{ loginReadyMessage }}</p>
            <NuxtLink class="mt-4 inline-flex text-sm font-semibold text-slate-600 hover:text-slate-950" to="/">Retour au tableau de bord</NuxtLink>
          </div>
        </article>

        <article class="flex min-h-[260px] min-w-0 flex-col rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
          <div>
            <p class="text-xs font-semibold uppercase tracking-normal text-cyan-800">Organisation</p>
            <h2 class="mt-2 text-xl font-semibold text-slate-950">Créer un compte entreprise</h2>
            <p class="mt-3 break-words text-sm leading-6 text-slate-700">
              Déclarez votre organisation et préparez les informations nécessaires à la vérification.
            </p>
          </div>

          <div class="mt-auto pt-5">
            <NuxtLink
              class="inline-flex h-10 w-full items-center justify-center rounded-md bg-white px-4 text-sm font-semibold text-slate-800 ring-1 ring-slate-200 transition hover:bg-slate-50"
              to="/creation-compte"
            >
              Créer mon espace
            </NuxtLink>
            <p class="mt-3 text-sm text-slate-600">Un administrateur devra valider votre organisation avant activation.</p>
          </div>
        </article>

        <article class="flex min-h-[260px] min-w-0 flex-col rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
          <div>
            <p class="text-xs font-semibold uppercase tracking-normal text-cyan-800">Responsable</p>
            <h2 class="mt-2 text-xl font-semibold text-slate-950">Accès administrateur</h2>
            <p class="mt-3 break-words text-sm leading-6 text-slate-700">
              Réservé aux responsables autorisés à inviter des collaborateurs et gérer les droits.
            </p>
          </div>

          <div class="mt-auto pt-5">
            <NuxtLink
              class="inline-flex h-10 w-full items-center justify-center rounded-md bg-white px-4 text-sm font-semibold text-slate-800 ring-1 ring-slate-200 transition hover:bg-slate-50"
              to="/admin-acces"
            >
              Accès admin
            </NuxtLink>
            <p class="mt-3 text-sm text-slate-600">La validation renforcée est requise avant tout privilège administrateur.</p>
          </div>
        </article>
      </div>

      <p class="mt-6 rounded-lg border border-slate-200 bg-white px-4 py-3 text-sm leading-6 text-slate-700">
        Relinium ne stocke pas vos mots de passe professionnels. L’accès définitif passe par une validation de l’organisation et des droits.
      </p>
    </div>
  </section>
</template>
