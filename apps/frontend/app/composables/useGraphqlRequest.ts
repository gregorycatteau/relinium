type GraphqlResponse<T> = {
  data?: T
  errors?: Array<{ message: string }>
}

export function useGraphqlRequest() {
  const config = useRuntimeConfig()
  const apiBase = computed(() => String(config.public.apiBase || 'http://127.0.0.1:8000'))

  async function csrfToken(): Promise<string> {
    const response = await $fetch<{ csrfToken: string }>(`${apiBase.value}/api/csrf`, {
      credentials: 'include'
    })
    return response.csrfToken
  }

  async function graphql<T>(query: string, variables: Record<string, unknown> = {}): Promise<T> {
    const token = await csrfToken()
    const response = await $fetch<GraphqlResponse<T>>(`${apiBase.value}/graphql`, {
      method: 'POST',
      credentials: 'include',
      headers: { 'X-CSRFToken': token },
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
