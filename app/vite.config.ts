import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// The dashboard loads plain (non-module) scripts and caps each file at 256 KB, so the build is two
// IIFE files: dist/vendor.js (React, as globals) and dist/app.js (this app). Run `npm run build`.
const globals = {
  react: 'React',
  'react-dom': 'ReactDOM',
  'react-dom/client': 'ReactDOMClient',
  'react/jsx-runtime': 'ReactJSX',
}
const part = process.env.PART === 'vendor' ? 'vendor' : 'app'

export default defineConfig(({ command }) => ({
  plugins: [react()],
  define: command === 'build' ? { 'process.env.NODE_ENV': JSON.stringify('production') } : {},
  build: {
    target: 'es2020',
    emptyOutDir: part === 'vendor',
    copyPublicDir: false,
    lib: {
      entry: part === 'vendor' ? 'src/vendor.ts' : 'src/main.tsx',
      formats: ['iife'],
      name: part === 'vendor' ? 'JobHuntingVendor' : 'JobHunting',
      fileName: () => `${part}.js`,
    },
    rollupOptions: part === 'app' ? { external: Object.keys(globals), output: { globals } } : {},
    minify: 'esbuild',
  },
}))
