<script setup lang="ts">
// Today (silos) vs With-pods (hub) — ported from .diagram-shift in site/styles.css.
// mode="both" (default) shows both panes; "before"/"after" show one.
withDefaults(defineProps<{ mode?: 'both' | 'before' | 'after' }>(), { mode: 'both' })
</script>

<template>
  <div class="mind-shift" :class="mode">
    <div v-if="mode !== 'after'" class="shift-pane shift-before">
      <div class="shift-tag">TODAY</div>
      <div class="shift-headline">Apps own your data</div>
      <div class="shift-viz">
        <div class="silo" v-for="s in [['Gmail', `Google's DB`], ['Notion', `Notion's DB`], ['Strava', `Strava's DB`]]" :key="s[0]">
          <div class="silo-cell user">you</div>
          <div class="silo-arrow">↓</div>
          <div class="silo-cell app">{{ s[0] }}</div>
          <div class="silo-arrow">↓</div>
          <div class="silo-cell db">{{ s[1] }}</div>
        </div>
      </div>
      <div class="shift-note">Three copies of "you". Three locked databases.</div>
    </div>

    <div v-if="mode !== 'before'" class="shift-pane shift-after">
      <div class="shift-tag">WITH PODS</div>
      <div class="shift-headline">You own your data</div>
      <div class="shift-viz">
        <div class="hub">
          <div class="hub-cell user">you</div>
          <div class="hub-arrow">↓</div>
          <div class="hub-apps">
            <div class="hub-app">Mail</div>
            <div class="hub-app">Notes</div>
            <div class="hub-app">Activity</div>
          </div>
          <div class="hub-fan">↘&nbsp;&nbsp;↓&nbsp;&nbsp;↙</div>
          <div class="hub-cell pod">Your Pod</div>
        </div>
      </div>
      <div class="shift-note">One you. One pod. Apps just visit.</div>
    </div>
  </div>
</template>

<style scoped>
.mind-shift {
  display: grid;
  grid-template-columns: 1fr 1fr;
  background:
    radial-gradient(ellipse 80% 60% at 50% 50%, rgba(34, 211, 238, 0.05) 0%, transparent 70%),
    linear-gradient(180deg, #0b0d12 0%, #07080b 100%);
  border: 1px solid #1e2939;
  border-radius: 12px;
  color: #e2e8f0;
  font-family: var(--mind-font-sans);
  overflow: hidden;
  box-shadow: 0 30px 60px -30px rgba(0, 0, 0, 0.6);
}
.mind-shift.before,
.mind-shift.after { grid-template-columns: 1fr; }

.shift-pane { padding: 26px 24px 22px; position: relative; }
.shift-before { border-right: 1px solid rgba(148, 163, 184, 0.1); }
.before .shift-before { border-right: 0; }
.shift-after { background: linear-gradient(180deg, rgba(7, 32, 52, 0.3) 0%, rgba(5, 18, 30, 0.5) 100%); }
.both .shift-after::before {
  content: "";
  position: absolute;
  left: 0; top: 14%; bottom: 14%;
  width: 1px;
  background: linear-gradient(180deg, transparent, rgba(34, 211, 238, 0.4), transparent);
}

.shift-tag {
  font-family: var(--mind-font-mono);
  font-size: 10px;
  letter-spacing: 3px;
  color: rgba(148, 163, 184, 0.5);
  margin-bottom: 4px;
}
.shift-after .shift-tag { color: rgba(103, 232, 249, 0.65); }
.shift-headline { font-size: 15px; font-weight: 700; color: #e2e8f0; margin-bottom: 22px; }
.shift-after .shift-headline { color: #cffafe; }

.shift-viz { display: flex; justify-content: center; gap: 16px; margin: 6px 0 16px; flex-wrap: wrap; }
.silo { display: flex; flex-direction: column; align-items: center; gap: 3px; }
.silo-cell {
  font-size: 11.5px; font-weight: 500; padding: 6px 12px; border-radius: 3px;
  min-width: 72px; text-align: center;
  background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(71, 85, 105, 0.5); color: #cbd5e1;
}
.silo-cell.user { background: transparent; border-style: dashed; color: rgba(203, 213, 225, 0.65); font-style: italic; }
.silo-cell.app { background: rgba(30, 41, 59, 0.7); color: #e2e8f0; }
.silo-cell.db {
  background: rgba(20, 15, 15, 0.7); border-color: rgba(120, 80, 80, 0.5);
  color: rgba(252, 165, 165, 0.85); font-family: var(--mind-font-mono); font-size: 10.5px;
}
.silo-arrow { font-size: 10px; color: rgba(148, 163, 184, 0.45); line-height: 1; }

.hub { display: flex; flex-direction: column; align-items: center; gap: 7px; }
.hub-cell {
  font-size: 11.5px; font-weight: 500; padding: 6px 14px; border-radius: 3px; text-align: center;
  background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(71, 85, 105, 0.5); color: #cbd5e1;
}
.hub-cell.user { background: transparent; border-style: dashed; color: rgba(207, 250, 254, 0.85); font-style: italic; }
.hub-cell.pod {
  background: rgba(8, 32, 52, 0.7); border-color: rgba(34, 211, 238, 0.5); color: #cffafe;
  font-weight: 700; letter-spacing: 0.5px; padding: 8px 22px;
  box-shadow: inset 0 0 14px rgba(34, 211, 238, 0.1);
}
.hub-arrow, .hub-fan { font-size: 11px; color: rgba(103, 232, 249, 0.45); letter-spacing: 4px; line-height: 1; }
.hub-apps { display: flex; gap: 8px; }
.hub-app {
  font-size: 11.5px; font-weight: 500; padding: 5px 11px; border-radius: 3px;
  background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(71, 85, 105, 0.5); color: #e2e8f0;
}
.shift-note { font-size: 11.5px; color: rgba(148, 163, 184, 0.65); text-align: center; margin-top: 14px; font-style: italic; }
</style>
