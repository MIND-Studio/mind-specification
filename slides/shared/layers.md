<!-- Shared partial · distilled from src/architecture.md "How Mind is shaped" -->

# Four layers, one source of truth

<LayerStack compact class="mt-2" />

<div class="mt-2 text-xs op75">
Apps & Workers both read and write the <strong>Pod</strong> — they never call each other; they meet at it. The <strong>WebID</strong> names your pod across the web.
</div>

<style scoped>
.slidev-layout h1 { font-size: 1.7em; margin-bottom: 0.2em; }
</style>
