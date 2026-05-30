<!-- Shared partial · distilled from src/apps.md "The fourteen apps" -->

# One pod. A whole family of apps.

<div class="app-grid mt-6">
  <div class="app-cell wedge"><b>Agents</b><span>AI memory you own</span></div>
  <div class="app-cell"><b>Compass</b><span>operator UI</span></div>
  <div class="app-cell"><b>Codespaces</b><span>git → your pod</span></div>
  <div class="app-cell"><b>Drive</b><span>your files</span></div>
  <div class="app-cell"><b>Docs</b><span>rich content</span></div>
  <div class="app-cell"><b>Todo</b><span>share = delegate</span></div>
  <div class="app-cell"><b>Calendar</b><span>your events</span></div>
  <div class="app-cell"><b>Contacts</b><span>your people</span></div>
  <div class="app-cell"><b>Flow</b><span>work board</span></div>
  <div class="app-cell"><b>Chat</b><span>pod-to-pod</span></div>
  <div class="app-cell"><b>Social</b><span>posts & friends</span></div>
  <div class="app-cell"><b>Marketplace</b><span>listings</span></div>
  <div class="app-cell"><b>Video</b><span>AI editor</span></div>
  <div class="app-cell"><b>Health</b><span>medical records</span></div>
</div>

<div class="mt-5 text-sm op75">
Every app reads and writes <strong>your</strong> pod — not a vendor's database. Add a new one by writing software that speaks the protocol. No app store, no platform approval.
</div>

<style scoped>
.app-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 8px; }
.app-cell {
  display: flex; flex-direction: column; gap: 2px;
  padding: 10px 12px; border-radius: 5px;
  background: rgba(15, 23, 42, 0.55); border: 1px solid rgba(71, 85, 105, 0.5);
}
.app-cell b { font-size: 13px; color: #e2e8f0; }
.app-cell span { font-size: 10.5px; color: rgba(148, 163, 184, 0.8); }
.app-cell.wedge { background: rgba(8, 32, 52, 0.7); border-color: rgba(34, 211, 238, 0.5); box-shadow: inset 0 0 14px rgba(34, 211, 238, 0.1); }
.app-cell.wedge b { color: #cffafe; }
.app-cell.wedge span { color: rgba(103, 232, 249, 0.75); }
</style>
