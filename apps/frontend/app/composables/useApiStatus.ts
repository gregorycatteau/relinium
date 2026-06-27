type ApiStatus = 'checking' | 'connected' | 'unavailable'

type HealthPayload = {
  status?: string
}

export function useApiStatus() {
  const config = useRuntimeConfig()
  const apiBase = computed(() => String(config.public.apiBase || 'http://127.0.0.1:8000'))

  const health = useAsyncData<HealthPayload>(
    'relinium-api-health',
    () => $fetch<HealthPayload>(`${apiBase.value}/api/health`),
    {
      default: () => ({})
    }
  )

  const status = computed<ApiStatus>(() => {
    if (health.pending.value) return 'checking'
    if (health.error.value) return 'unavailable'
    return health.data.value?.status === 'ok' ? 'connected' : 'unavailable'
  })

  return {
    apiBase,
    status,
    pending: health.pending,
    error: health.error,
    refresh: health.refresh
  }
}
