<template>
  <div class="slidev-layout mind-cover">
    <div class="mind-cover-bracket tl" />
    <div class="mind-cover-bracket br" />
    <div class="mind-cover-inner">
      <slot />
    </div>
  </div>
</template>

<style scoped>
.mind-cover {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  padding: 0 4rem;
  position: relative;
}
.mind-cover-inner {
  max-width: 80%;
}
.mind-cover-bracket {
  position: absolute;
  width: 36px;
  height: 36px;
  border: 1.5px solid rgba(34, 211, 238, 0.5);
  pointer-events: none;
}
.mind-cover-bracket.tl { top: 24px; left: 24px; border-right: 0; border-bottom: 0; }
.mind-cover-bracket.br { bottom: 24px; right: 24px; border-left: 0; border-top: 0; }

.mind-cover :deep(h1) {
  font-size: 3.4em;
  line-height: 1.05;
  margin-bottom: 0.3em;
  background: linear-gradient(180deg, #f5f5f5 0%, #a5f3fc 140%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}
.mind-cover :deep(p) {
  font-size: 1.25em;
  color: var(--mind-muted);
  max-width: 40ch;
}
.mind-cover :deep(.mind-kicker) {
  font-family: var(--mind-font-mono);
  font-size: 0.8em;
  letter-spacing: 0.3em;
  text-transform: uppercase;
  color: var(--mind-accent-bright);
  margin-bottom: 1.2em;
}
</style>
