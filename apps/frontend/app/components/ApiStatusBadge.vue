<script setup lang="ts">
const { apiBase, status } = useApiStatus()

const label = computed(() => {
  if (status.value === 'connected') return 'API connectée'
  if (status.value === 'checking') return 'API…'
  return 'API indisponible'
})

const classes = computed(() => {
  if (status.value === 'connected') return 'bg-emerald-50 text-emerald-800 ring-emerald-200'
  if (status.value === 'checking') return 'bg-sky-50 text-sky-800 ring-sky-200'
  return 'bg-red-50 text-red-800 ring-red-200'
})
</script>

<template>
  <span
    class="inline-flex max-w-full items-center rounded-full px-2.5 py-1 text-xs font-semibold ring-1"
    :class="classes"
    :title="apiBase"
  >
    {{ label }}
  </span>
</template>
