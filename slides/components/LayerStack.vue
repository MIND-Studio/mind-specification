<script setup lang="ts">
// Four-layer stack — ported from .diagram-layers in site/styles.css.
// `compact` trims padding so it fits a slide alongside a heading.
defineProps<{ compact?: boolean }>()
</script>

<template>
  <div class="mind-layers" :class="{ compact }">
    <div class="layer">
      <div class="layer-head">
        <span class="layer-num">04</span>
        <div class="layer-meta">
          <div class="layer-name">APPS</div>
          <div class="layer-tag">what you click · web + installed</div>
        </div>
      </div>
      <div class="layer-body">
        <span class="chip">Compass</span><span class="chip">Agents</span><span class="chip">Drive</span><span class="chip">Docs</span><span class="chip">Codespaces</span><span class="chip">Chat</span><span class="chip">+8</span>
      </div>
    </div>

    <div class="layer">
      <div class="layer-head">
        <span class="layer-num">03</span>
        <div class="layer-meta">
          <div class="layer-name">WORKERS</div>
          <div class="layer-tag">background work · holds your pod auth</div>
        </div>
      </div>
      <div class="layer-body">
        <span class="chip">indexers</span><span class="chip">bridges</span><span class="chip">agent runtimes</span>
      </div>
    </div>

    <div class="layer is-canonical">
      <div class="layer-head">
        <span class="layer-num">02</span>
        <div class="layer-meta">
          <div class="layer-name">POD</div>
          <div class="layer-tag">where your stuff lives · the source of truth</div>
        </div>
      </div>
      <div class="layer-body">
        <span class="chip chip-pod">Solid pod · hosted anywhere</span>
      </div>
    </div>

    <div class="layer is-external">
      <div class="layer-head">
        <span class="layer-num">01</span>
        <div class="layer-meta">
          <div class="layer-name">WEBID</div>
          <div class="layer-tag">your portable identity · standard Solid + OIDC</div>
        </div>
      </div>
      <div class="layer-body">
        <span class="chip chip-id">WebID + Solid-OIDC</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.mind-layers {
  background:
    radial-gradient(ellipse 80% 60% at 50% 50%, rgba(34, 211, 238, 0.06) 0%, transparent 70%),
    linear-gradient(180deg, #0b0d12 0%, #07080b 100%);
  border: 1px solid #1e2939;
  border-radius: 12px;
  overflow: hidden;
  font-family: var(--mind-font-sans);
  color: #e2e8f0;
  box-shadow: 0 1px 0 rgba(255, 255, 255, 0.04) inset, 0 30px 60px -30px rgba(0, 0, 0, 0.6);
  position: relative;
}
.mind-layers::before,
.mind-layers::after {
  content: "";
  position: absolute;
  width: 18px;
  height: 18px;
  border: 1px solid rgba(34, 211, 238, 0.45);
  pointer-events: none;
}
.mind-layers::before { top: 8px; left: 8px; border-right: 0; border-bottom: 0; }
.mind-layers::after { bottom: 8px; right: 8px; border-left: 0; border-top: 0; }

.layer {
  position: relative;
  padding: 22px 32px;
  border-top: 1px solid rgba(148, 163, 184, 0.08);
  background: linear-gradient(180deg, rgba(15, 23, 42, 0.35) 0%, rgba(8, 11, 18, 0.55) 100%);
}
.compact .layer { padding: 8px 26px; }
.layer:first-child { border-top: 0; }
.layer::before {
  content: "";
  position: absolute;
  left: 0; top: 0; bottom: 0;
  width: 2px;
  background: transparent;
}

.layer-head { display: flex; align-items: baseline; gap: 22px; margin-bottom: 12px; }
.compact .layer-head { margin-bottom: 4px; }
.layer-num {
  font-family: var(--mind-font-mono);
  font-size: 36px;
  font-weight: 300;
  letter-spacing: -1.5px;
  line-height: 1;
  width: 52px;
  text-align: right;
  background: linear-gradient(180deg, rgba(148, 163, 184, 0.85) 0%, rgba(71, 85, 105, 0.4) 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}
.compact .layer-num { font-size: 23px; width: 36px; }
.compact .layer-body { gap: 6px; padding-left: 58px; }
.compact .chip { padding: 3px 9px; font-size: 11px; }
.compact .layer-tag { font-size: 10.5px; }
.layer-meta { display: flex; flex-direction: column; gap: 2px; }
.layer-name { font-size: 12px; font-weight: 700; letter-spacing: 3.5px; color: #e2e8f0; }
.layer-tag { font-size: 11px; color: rgba(148, 163, 184, 0.75); }

.layer-body { display: flex; flex-wrap: wrap; gap: 7px; padding-left: 74px; }
.chip {
  display: inline-flex;
  align-items: center;
  padding: 5px 12px;
  background: rgba(15, 23, 42, 0.65);
  border: 1px solid rgba(71, 85, 105, 0.55);
  border-radius: 3px;
  font-size: 11.5px;
  font-weight: 500;
  color: #cbd5e1;
}

.layer.is-canonical {
  background: linear-gradient(180deg, rgba(8, 32, 52, 0.55) 0%, rgba(7, 18, 30, 0.75) 100%);
  border-top-color: rgba(34, 211, 238, 0.2);
}
.layer.is-canonical + .layer { border-top-color: rgba(34, 211, 238, 0.2); }
.layer.is-canonical::before {
  background: linear-gradient(180deg, transparent 0%, #22d3ee 50%, transparent 100%);
  box-shadow: 0 0 14px rgba(34, 211, 238, 0.5);
}
.layer.is-canonical .layer-num {
  background: linear-gradient(180deg, #67e8f9 0%, #22d3ee 60%, rgba(34, 211, 238, 0.4) 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}
.layer.is-canonical .layer-name { color: #cffafe; }
.layer.is-canonical .layer-tag { color: rgba(103, 232, 249, 0.7); }
.chip-pod {
  background: rgba(8, 41, 66, 0.7);
  border-color: rgba(34, 211, 238, 0.45);
  color: #cffafe;
  box-shadow: inset 0 0 14px rgba(34, 211, 238, 0.1);
}

.layer.is-external {
  background: linear-gradient(180deg, rgba(10, 10, 12, 0.6) 0%, rgba(5, 5, 7, 0.85) 100%);
}
.layer.is-external .layer-num {
  background: linear-gradient(180deg, rgba(100, 116, 139, 0.7) 0%, rgba(51, 65, 85, 0.3) 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}
.layer.is-external .layer-name { color: rgba(203, 213, 225, 0.8); }
.chip-id {
  font-family: var(--mind-font-mono);
  background: rgba(5, 5, 7, 0.7);
  border-color: rgba(51, 65, 85, 0.6);
  color: rgba(148, 163, 184, 0.85);
  font-size: 11px;
}
</style>
