<script setup lang="ts">
type OrganizationData = {
  currentOrganization?: { id: string, name: string, slug: string, mfaPolicy: string } | null
  myMemberships: Array<{ role: string, status: string, organization: { id: string, name: string, slug: string } }>
  myPermissions: { permissions: string[] }
}

const { graphql } = useGraphqlRequest()
const erreur = ref('')

const req = useAsyncData('organization-page', () => graphql<OrganizationData>(`
  query OrganizationPage {
    currentOrganization { id name slug mfaPolicy }
    myMemberships { role status organization { id name slug } }
    myPermissions { permissions }
  }
`))

const peutAdministrer = computed(() => req.data.value?.myPermissions.permissions.includes('admin:manage_members') || false)

async function selectionner(id: string): Promise<void> {
  erreur.value = ''
  try {
    await graphql('mutation SelectOrganization($organizationId: String!) { selectOrganization(organizationId: $organizationId) { id name } }', { organizationId: id })
    await req.refresh()
  } catch (error) {
    erreur.value = error instanceof Error ? error.message : 'Sélection impossible.'
  }
}
</script>

<template>
  <section class="w-full bg-slate-50 px-4 py-8 sm:px-6 lg:px-8">
    <div class="mx-auto max-w-4xl">
      <h1 class="text-3xl font-semibold text-slate-950">Organisation</h1>
      <div class="mt-6 grid gap-4 lg:grid-cols-[1fr_1fr]">
        <section class="rounded-lg border border-slate-200 bg-white p-5">
          <h2 class="text-lg font-semibold text-slate-950">Organisation active</h2>
          <p class="mt-2 text-sm text-slate-600">{{ req.data.value?.currentOrganization?.name || 'Aucune organisation sélectionnée' }}</p>
          <p v-if="req.data.value?.currentOrganization" class="mt-1 text-xs text-slate-500">MFA: {{ req.data.value.currentOrganization.mfaPolicy }}</p>
        </section>
        <section class="rounded-lg border border-slate-200 bg-white p-5">
          <h2 class="text-lg font-semibold text-slate-950">Administration</h2>
          <p class="mt-2 text-sm" :class="peutAdministrer ? 'text-emerald-800' : 'text-slate-600'">
            {{ peutAdministrer ? 'Vous pouvez gérer les membres.' : 'La gestion des membres est réservée aux administrateurs.' }}
          </p>
        </section>
      </div>
      <section class="mt-4 rounded-lg border border-slate-200 bg-white p-5">
        <h2 class="text-lg font-semibold text-slate-950">Mes accès</h2>
        <div class="mt-3 divide-y divide-slate-100">
          <div v-for="membership in req.data.value?.myMemberships || []" :key="membership.organization.id" class="flex items-center justify-between gap-3 py-3">
            <div>
              <p class="font-semibold text-slate-900">{{ membership.organization.name }}</p>
              <p class="text-sm text-slate-500">{{ membership.role }} · {{ membership.status }}</p>
            </div>
            <button class="h-9 rounded-md bg-white px-3 text-sm font-semibold text-slate-700 ring-1 ring-slate-200" type="button" @click="selectionner(membership.organization.id)">Sélectionner</button>
          </div>
        </div>
        <p v-if="erreur" class="mt-3 rounded-md bg-red-50 p-3 text-sm text-red-800 ring-1 ring-red-200">{{ erreur }}</p>
      </section>
      <section class="mt-4 rounded-lg border border-slate-200 bg-white p-5">
        <h2 class="text-lg font-semibold text-slate-950">Permissions</h2>
        <div class="mt-3 flex flex-wrap gap-2">
          <span v-for="permission in req.data.value?.myPermissions.permissions || []" :key="permission" class="rounded-md bg-slate-50 px-2 py-1 text-xs font-semibold text-slate-700 ring-1 ring-slate-200">{{ permission }}</span>
        </div>
      </section>
    </div>
  </section>
</template>
