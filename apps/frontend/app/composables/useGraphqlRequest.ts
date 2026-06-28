type GraphqlResponse<T> = {
  data?: T
  errors?: Array<{ message: string }>
}

export function useGraphqlRequest() {
  const config = useRuntimeConfig()
  const apiBase = computed(() => String(config.public.apiBase || 'http://127.0.0.1:8000'))

  async function csrfHeaders(): Promise<Record<string, string>> {
    const response = await $fetch.raw<{ csrfToken: string }>(`${apiBase.value}/api/csrf`, {
      credentials: 'include'
    })
    const token = response._data?.csrfToken || ''
    const headers: Record<string, string> = { 'X-CSRFToken': token }
    if (import.meta.server) {
      const setCookie = response.headers.get('set-cookie')
      if (setCookie) headers.Cookie = setCookie.split(';', 1)[0]
    }
    return headers
  }

  async function graphql<T>(query: string, variables: Record<string, unknown> = {}): Promise<T> {
    const headers = await csrfHeaders()
    const response = await $fetch<GraphqlResponse<T>>(`${apiBase.value}/graphql`, {
      method: 'POST',
      credentials: 'include',
      headers,
      body: { query, variables }
    })
    if (response.errors?.length) {
      throw new Error(response.errors.map((item) => item.message).join(' '))
    }
    if (!response.data) throw new Error('Réponse GraphQL vide.')
    return response.data
  }

  return { apiBase, graphql }
}
