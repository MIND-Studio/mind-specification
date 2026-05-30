<script setup lang="ts">
// Phase ladder — ported from .diagram-roadmap-ladder in site/styles.css.
// Slide-sized condensation of src/roadmap.md (full 12-step list lives in the docs).
type Status = 'planned' | 'building' | 'concept'
interface Step { n: string; name: string; tag: string; status: Status; tone: 'foundation' | 'now' | 'next' | 'later' }
interface Phase { num: string; title: string; sub: string; steps: Step[] }

const phases: Phase[] = [
  {
    num: 'PHASE I', title: 'The Wedge', sub: 'Ship to the first hundred users.',
    steps: [
      { n: '0', name: 'Pods.mind', tag: 'Hosted pods — the foundation everything stands on.', status: 'planned', tone: 'foundation' },
      { n: '1', name: 'Agents + Compass', tag: 'Your AI’s memory belongs to you. No incumbent.', status: 'building', tone: 'now' },
      { n: '2', name: 'Codespaces', tag: 'Developer wedge — already production-alpha.', status: 'building', tone: 'now' },
    ],
  },
  {
    num: 'PHASE II', title: 'Make it Daily', sub: 'Surround the wedge with daily surfaces.',
    steps: [
      { n: '3–5', name: 'Drive · Todo · Dock', tag: 'Files, the “hello world,” and the shell to launch it all.', status: 'building', tone: 'next' },
      { n: '6–8', name: 'Calendar · Docs · Flow', tag: 'Shared-domain basics + rich content + the work board.', status: 'concept', tone: 'next' },
    ],
  },
  {
    num: 'PHASE III', title: 'Fill Out the Family', sub: 'Network-effect & niche apps — once there are users.',
    steps: [
      { n: '9–11', name: 'Video · Chat · Social · Health', tag: 'Need differentiation or other people first.', status: 'concept', tone: 'later' },
    ],
  },
]
const statusLabel: Record<Status, string> = { planned: 'PRE-PRODUCT', building: 'BUILDING', concept: 'CONCEPT' }
</script>

<template>
  <div class="mind-ladder">
    <template v-for="p in phases" :key="p.num">
      <div class="phase-header">
        <span class="phase-num">{{ p.num }}</span>
        <div class="phase-titles">
          <div class="phase-title">{{ p.title }}</div>
          <div class="phase-sub">{{ p.sub }}</div>
        </div>
      </div>
      <div v-for="s in p.steps" :key="s.n" class="step" :class="`step-${s.tone}`">
        <div class="step-num">{{ s.n }}</div>
        <div class="step-body">
          <div class="step-name">{{ s.name }}</div>
          <div class="step-tag">{{ s.tag }}</div>
        </div>
        <div class="step-status">
          <span class="pill" :class="`status-${s.status}`">{{ statusLabel[s.status] }}</span>
        </div>
      </div>
    </template>
  </div>
</template>

<style scoped>
.mind-ladder {
  background: linear-gradient(180deg, rgba(11, 13, 18, 0.98), rgba(7, 8, 11, 0.98));
  border: 1px solid rgba(34, 211, 238, 0.18);
  border-radius: 8px;
  color: #e2e8f0;
  overflow: hidden;
  font-family: var(--mind-font-sans);
}
.phase-header {
  display: flex; align-items: center; gap: 14px; padding: 6px 22px 5px;
  background: linear-gradient(90deg, rgba(34, 211, 238, 0.06), transparent 60%);
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
}
.phase-header + .step, .step + .step { border-top: 1px solid rgba(148, 163, 184, 0.08); }
.phase-header:not(:first-child) { border-top: 1px dashed rgba(148, 163, 184, 0.2); }
.phase-num {
  font-family: var(--mind-font-mono); font-size: 10px; font-weight: 700; letter-spacing: 0.22em;
  text-transform: uppercase; color: #67e8f9; padding: 3px 9px;
  border: 1px solid rgba(34, 211, 238, 0.4); border-radius: 999px; white-space: nowrap;
}
.phase-titles { display: flex; flex-direction: column; gap: 1px; }
.phase-title { font-size: 15px; font-weight: 700; color: #f1f5f9; }
.phase-sub { font-size: 11px; color: rgba(148, 163, 184, 0.85); }

.step { display: flex; align-items: center; gap: 14px; padding: 4px 22px; position: relative; }
.step::before {
  content: ""; position: absolute; left: 40px; top: 0; bottom: 0; width: 2px; margin-left: -1px; z-index: 0;
}
.step-foundation::before { background: linear-gradient(180deg, rgba(251, 191, 36, 0.55), rgba(251, 191, 36, 0.25)); }
.step-now::before { background: linear-gradient(180deg, rgba(34, 211, 238, 0.55), rgba(34, 211, 238, 0.35)); }
.step-next::before { background: linear-gradient(180deg, rgba(34, 211, 238, 0.3), rgba(148, 163, 184, 0.2)); }
.step-later::before { background: rgba(148, 163, 184, 0.18); }

.step-num {
  position: relative; z-index: 1; flex: 0 0 auto; min-width: 32px; height: 32px; padding: 0 7px;
  border-radius: 999px; display: flex; align-items: center; justify-content: center;
  font-family: var(--mind-font-mono); font-size: 12px; font-weight: 800;
  background: #0b0d12; border: 2px solid rgba(148, 163, 184, 0.45); color: rgba(226, 232, 240, 0.95);
}
.step-foundation .step-num { border-color: #fbbf24; color: #fbbf24; box-shadow: 0 0 0 4px #0b0d12, 0 0 14px rgba(251, 191, 36, 0.35); }
.step-now .step-num { border-color: #22d3ee; color: #67e8f9; box-shadow: 0 0 0 4px #0b0d12, 0 0 14px rgba(34, 211, 238, 0.4); }
.step-next .step-num { border-color: rgba(34, 211, 238, 0.55); color: #a5f3fc; box-shadow: 0 0 0 4px #0b0d12; }
.step-later .step-num { border-color: rgba(148, 163, 184, 0.35); color: rgba(148, 163, 184, 0.85); box-shadow: 0 0 0 4px #0b0d12; }

.step-body { flex: 1 1 auto; min-width: 0; display: flex; flex-direction: column; gap: 2px; }
.step-name { font-size: 14px; font-weight: 700; color: #f1f5f9; }
.step-tag { font-size: 12px; line-height: 1.4; color: rgba(203, 213, 225, 0.78); }
.step-later .step-name { color: rgba(226, 232, 240, 0.78); }
.step-later .step-tag { color: rgba(203, 213, 225, 0.55); }

.step-status { flex: 0 0 auto; }
.pill {
  font-family: var(--mind-font-mono); font-size: 9px; letter-spacing: 1.5px; font-weight: 700;
  padding: 3px 8px; border-radius: 2px; white-space: nowrap; border: 1px solid;
}
.status-building { background: rgba(8, 32, 52, 0.7); border-color: rgba(34, 211, 238, 0.5); color: #67e8f9; box-shadow: 0 0 8px rgba(34, 211, 238, 0.18); }
.status-concept { background: rgba(30, 30, 35, 0.7); border-color: rgba(148, 163, 184, 0.4); color: rgba(203, 213, 225, 0.7); }
.status-planned { background: rgba(40, 35, 20, 0.7); border-color: rgba(180, 140, 80, 0.4); color: rgba(252, 211, 77, 0.85); }
</style>
