<script setup lang="ts">
const { apiBase, status } = useApiStatus()

const label = computed(() => {
  if (status.value === 'connected') return 'API connectée'
  if (status.value === 'checking') return 'API…'
  return 'API indisponible'
})

const pointClass = computed(() => {
  if (status.value === 'connected') return 'bg-emerald-500'
  if (status.value === 'checking') return 'bg-sky-500'
  return 'bg-red-500'
})
</script>

<template>
  <span class="relative inline-flex h-8 w-8 items-center justify-center rounded-md text-slate-600 transition hover:bg-slate-50 hover:text-slate-950" :title="`${label} - ${apiBase}`" :aria-label="label">
    <svg aria-hidden="true" class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
      <path d="M22 12h-4l-3 8-6-16-3 8H2" />
    </svg>
    <span class="absolute right-1.5 top-1.5 h-2 w-2 rounded-full ring-2 ring-white" :class="pointClass" />
  </span>
</template>
