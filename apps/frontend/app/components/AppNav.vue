<script setup lang="ts">
type NavItem = {
  label: string
  to?: string
  disabled?: boolean
}

const route = useRoute()
const NuxtLinkComponent = resolveComponent('NuxtLink')

const items: NavItem[] = [
  { label: 'Anti-Scam', to: '/anti-scam' },
  { label: 'Cartographie', disabled: true },
  { label: 'Mouvements', disabled: true },
  { label: 'Rapports', disabled: true }
]

function isActive(item: NavItem): boolean {
  if (!item.to) return false
  return item.to === '/' ? route.path === '/' : route.path.startsWith(item.to)
}
</script>

<template>
  <nav aria-label="Navigation applicative" class="min-w-0">
    <div class="flex flex-col gap-1 md:flex-row md:items-center md:gap-1.5">
      <component
        :is="item.to ? NuxtLinkComponent : 'button'"
        v-for="item in items"
        :key="item.label"
        :to="item.to"
        :disabled="item.disabled || undefined"
        class="group inline-flex h-9 w-full items-center justify-between rounded-md px-3 text-sm font-medium transition outline-none focus-visible:ring-2 focus-visible:ring-cyan-700 focus-visible:ring-offset-2 md:h-8 md:w-[112px] md:max-w-[112px] md:justify-center md:px-2 md:text-[13px]"
        :class="[
          isActive(item)
            ? 'bg-cyan-50 text-cyan-950 ring-1 ring-cyan-100'
            : item.disabled
              ? 'cursor-not-allowed text-slate-400'
              : 'text-slate-700 hover:bg-slate-50 hover:text-slate-950',
        ]"
        type="button"
      >
        <span class="whitespace-nowrap">{{ item.label }}</span>
        <span v-if="isActive(item)" class="h-1 w-1 rounded-full bg-cyan-700 md:hidden" aria-hidden="true" />
      </component>
    </div>
  </nav>
</template>
