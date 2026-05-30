<script setup lang="ts">
// "Decentralized Network In Mind" — the four cyan initials fly straight into MIND.
// CSS-only motion (animation runs on mount); the same look ships to the site as an
// inline HTML block + styles.css. Positions are computed in ch units so it scales
// with font-size. The four capitals are detected automatically.
const props = withDefaults(defineProps<{
  phrase?: string
  hold?: string      // how long the sentence shows before collapsing
  move?: string      // duration of the fly-together
  scale?: number     // how large the surviving letters grow
}>(), {
  phrase: 'Decentralized Network In Mind',
  hold: '1.9s',
  move: '1.05s',
  scale: 2.55,
})

const GS = 4.0                                   // spacing (ch) between the final letters
const TARGET: Record<string, number> = { M: 0, I: 1, N: 2, D: 3 }  // caps fly straight into MIND order
const center = props.phrase.length / 2

const letters = [...props.phrase].map((ch, i) => {
  const isCap = ch >= 'A' && ch <= 'Z'
  const dx = isCap ? (center + (TARGET[ch] - 1.5) * GS) - (i + 0.5) : 0
  return { ch: ch === ' ' ? ' ' : ch, isCap, dx }
})
</script>

<template>
  <div class="mind-mark" :style="{ '--hold': hold, '--move': move, '--scale': String(scale) }">
    <div class="ln">
      <span v-for="(l, i) in letters" :key="i" class="ch" :class="l.isCap ? 'c' : 'l'"
            :style="l.isCap ? { '--dx': l.dx + 'ch' } : undefined">
        <span class="g">{{ l.ch }}</span>
      </span>
    </div>
  </div>
</template>

<!-- Visuals come from shared/brand.css (.mind-mark) — the single source of truth,
     imported in slides/styles/index.css. Edit the look there, not here. -->

