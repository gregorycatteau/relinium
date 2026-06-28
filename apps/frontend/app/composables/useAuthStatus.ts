type AuthOrganization = {
  id: string
  slug: string
  name: string
  mfaPolicy?: string
}

type AuthUser = {
  displayName: string
  avatarInitials: string
  emailRedacted?: string
  selectedOrganization?: AuthOrganization | null
}

type AuthMembership = {
  role: string
  status: string
  organization: AuthOrganization
}

type AuthStatusPayload = {
  authenticated: boolean
  mode: string
  oidcConfigured: boolean
  providerConfigured: boolean
  providerName: string
  devAuthEnabled: boolean
  mfaRequired: boolean
  mfaEnrolled: boolean
  mfaProviderStatus: string
  user?: AuthUser | null
  currentOrganization?: AuthOrganization | null
}

type AuthStatusData = {
  authStatus: AuthStatusPayload
  currentUser?: AuthUser | null
  myMemberships: AuthMembership[]
}

const anonymousAuthData = (): AuthStatusData => ({
  authStatus: {
    authenticated: false,
    mode: 'disabled',
    oidcConfigured: false,
    providerConfigured: false,
    providerName: '',
    devAuthEnabled: false,
    mfaRequired: false,
    mfaEnrolled: false,
    mfaProviderStatus: 'planned',
    user: null,
    currentOrganization: null
  },
  currentUser: null,
  myMemberships: []
})

export function useAuthStatus() {
  const { graphql } = useGraphqlRequest()

  const req = useAsyncData<AuthStatusData>(
    'relinium-auth-status',
    () => graphql<AuthStatusData>(`
      query ReliniumAuthStatus {
        authStatus {
          authenticated
          mode
          oidcConfigured
          providerConfigured
          providerName
          devAuthEnabled
          mfaRequired
          mfaEnrolled
          mfaProviderStatus
          user { displayName avatarInitials emailRedacted selectedOrganization { id slug name mfaPolicy } }
          currentOrganization { id slug name mfaPolicy }
        }
        currentUser { displayName avatarInitials emailRedacted selectedOrganization { id slug name mfaPolicy } }
        myMemberships { role status organization { id slug name mfaPolicy } }
      }
    `),
    { default: anonymousAuthData }
  )

  const data = computed(() => req.data.value || anonymousAuthData())
  const status = computed(() => data.value.authStatus)
  const isAuthenticated = computed(() => Boolean(status.value.authenticated))
  const user = computed(() => isAuthenticated.value ? (status.value.user || data.value.currentUser || null) : null)
  const displayName = computed(() => user.value?.displayName || '')
  const initials = computed(() => user.value?.avatarInitials || displayName.value.slice(0, 2).toUpperCase())
  const currentOrganization = computed(() => status.value.currentOrganization || user.value?.selectedOrganization || null)
  const memberships = computed(() => isAuthenticated.value ? data.value.myMemberships : [])

  return {
    pending: req.pending,
    error: req.error,
    refresh: req.refresh,
    status,
    isAuthenticated,
    displayName,
    initials,
    mode: computed(() => status.value.mode),
    providerConfigured: computed(() => Boolean(status.value.providerConfigured)),
    providerName: computed(() => status.value.providerName),
    devAuthEnabled: computed(() => Boolean(status.value.devAuthEnabled)),
    currentOrganization,
    memberships,
    mfaRequired: computed(() => Boolean(status.value.mfaRequired)),
    mfaEnrolled: computed(() => Boolean(status.value.mfaEnrolled))
  }
}
