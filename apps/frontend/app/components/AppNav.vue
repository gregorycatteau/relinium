<script setup lang="ts">
type NavItem = {
  label: string
  to?: string
  soon?: boolean
}

const route = useRoute()

const items: NavItem[] = [
  { label: 'Tableau de bord', to: '/' },
  { label: 'Anti-Scam', to: '/anti-scam' },
  { label: 'Cartographie documentaire', soon: true },
  { label: 'Détecteur de mouvement', soon: true },
  { label: 'Rapports', soon: true },
  { label: 'Administration', soon: true }
]

function isActive(item: NavItem): boolean {
  if (!item.to) return false
  return item.to === '/' ? route.path === '/' : route.path.startsWith(item.to)
}
</script>

<template>
  <nav aria-label="Navigation applicative" class="min-w-0">
    <div class="flex gap-1.5 overflow-x-auto pb-1 md:flex-wrap md:overflow-visible md:pb-0">
      <component
        :is="item.to ? 'NuxtLink' : 'button'"
        v-for="item in items"
        :key="item.label"
        :to="item.to"
        :disabled="item.soon || undefined"
        class="group inline-flex min-h-10 shrink-0 items-center gap-2 rounded-full px-3 py-2 text-sm font-semibold transition"
        :class="[
          isActive(item)
            ? 'bg-cyan-950 text-white shadow-sm ring-1 ring-cyan-950'
            : item.soon
              ? 'cursor-not-allowed bg-slate-50 text-slate-400 ring-1 ring-slate-200'
              : 'bg-white text-slate-700 ring-1 ring-slate-200 hover:bg-slate-50',
        ]"
        type="button"
      >
        <span>{{ item.label }}</span>
        <span
          v-if="item.soon"
          class="rounded-full bg-white px-1.5 py-0.5 text-[0.68rem] font-semibold text-slate-500 ring-1 ring-slate-200"
        >
          Bientôt
        </span>
        <span v-if="isActive(item)" class="h-1.5 w-1.5 rounded-full bg-cyan-200" aria-hidden="true" />
      </component>
    </div>
  </nav>
</template>
