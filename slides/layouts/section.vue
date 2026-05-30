<template>
  <div class="slidev-layout mind-section">
    <div class="mind-section-rail" />
    <div class="mind-section-inner">
      <slot />
    </div>
  </div>
</template>

<style scoped>
.mind-section {
  display: flex;
  align-items: center;
  padding: 0 4rem;
  position: relative;
}
.mind-section-rail {
  position: absolute;
  left: 0;
  top: 18%;
  bottom: 18%;
  width: 3px;
  background: linear-gradient(180deg, transparent, #22d3ee 50%, transparent);
  box-shadow: 0 0 18px rgba(34, 211, 238, 0.5);
}
.mind-section-inner :deep(h1) {
  font-size: 2.8em;
  line-height: 1.1;
}
.mind-section-inner :deep(p) {
  font-size: 1.15em;
  color: var(--mind-muted);
  max-width: 46ch;
  margin-top: 0.4em;
}
</style>
