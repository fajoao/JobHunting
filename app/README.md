# JobHunting – painel web

React + TypeScript + Vite. Roda como Artifact do tipo Dashboard do Claude (veja a skill `jobhunting-dashboard`).

```bash
npm ci
npm run dev     # local, com dados de exemplo (src/mock.ts)
npm run build   # gera dist/vendor.js (React) e dist/app.js (o app), cada um com menos de 256 KB
```

`src/runtime.ts` liga o app aos datasets do dashboard (`vagas`, `execucoes`, `pedidos`, `progresso`, `perfil`) ou ao mock local.
