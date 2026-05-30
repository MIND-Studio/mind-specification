import { defineConfig } from 'vite'

// Allow the deck to @import ../../shared/brand.css (the single source of
// truth for brand visuals, shared with the site). Vite's dev server
// otherwise blocks reads outside the project root.
export default defineConfig({
  server: {
    fs: { allow: ['..'] },
  },
})
