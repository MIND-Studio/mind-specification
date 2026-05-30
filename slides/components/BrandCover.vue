<script setup lang="ts">
// Cinematic quote / statement panel — echoes .diagram-hero from site/styles.css.
defineProps<{ kicker?: string; attrib?: string }>()
</script>

<template>
  <div class="mind-hero">
    <div v-if="kicker" class="hero-kicker">{{ kicker }}</div>
    <blockquote class="hero-quote"><slot /></blockquote>
    <div v-if="attrib" class="hero-attrib">{{ attrib }}</div>
  </div>
</template>

<style scoped>
.mind-hero {
  background:
    radial-gradient(ellipse 90% 70% at 50% 0%, rgba(34, 211, 238, 0.07) 0%, transparent 60%),
    linear-gradient(180deg, #0b0d12 0%, #07080b 100%);
  border: 1px solid #1e2939;
  border-radius: 12px;
  padding: 3rem 3.2rem;
  text-align: center;
  box-shadow: 0 30px 60px -30px rgba(0, 0, 0, 0.6);
}
.hero-kicker {
  font-family: var(--mind-font-mono);
  font-size: 0.85rem;
  letter-spacing: 0.32em;
  text-transform: uppercase;
  color: var(--mind-accent-bright);
  margin-bottom: 1.6rem;
}
.hero-quote {
  font-size: 3rem;
  font-weight: 700;
  line-height: 1.12;
  color: #f5f5f5;
  border: 0;
  margin: 0;
  padding: 0;
  letter-spacing: -0.02em;
}
.hero-quote :deep(strong) { color: var(--mind-accent-bright); }
.hero-attrib {
  margin-top: 1.6rem;
  font-size: 0.95rem;
  color: var(--mind-muted);
}
</style>
