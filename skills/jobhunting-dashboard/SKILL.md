---
name: jobhunting-dashboard
description: "Cria ou atualiza o painel web do JobHunting (dashboard em React com KPIs, funil, gráficos, lista de vagas com Excluir e Marcar como aplicada, botão Buscar agora e progresso das buscas) como um Artifact do Claude, e guarda o perfil de forma privada nele para as rotinas. Use quando o usuário pedir dashboard, painel, \"ver minhas vagas\" ou publicar o JobHunting."
model: claude-haiku-5-5
---

# JobHunting – dashboard

**Código:** `${CLAUDE_PLUGIN_ROOT}/app` (React + TypeScript + Vite).

**Por que dois arquivos:** o tipo Dashboard dos Artifacts só aceita scripts comuns, sem módulos, e no máximo 256 KB por arquivo. Por isso o build gera `dist/vendor.js` (React) e `dist/app.js` (o app).

## Criar
1. Gere o build:
   ```bash
   cd "${CLAUDE_PLUGIN_ROOT}/app" && npm ci && npm run build
   ```
   Para ver localmente com dados de exemplo, use `npm run dev`.
2. Crie um Artifact do tipo **Dashboard**: `Artifact` com `action: "quickstart"`, `intent: "other"`, e depois o `type_url` do Dashboard. Siga as instruções que o tipo devolver.
3. Grave com `ArtifactData` (batch), num único lote:
   - `dash/meta`: `{title: "JobHunting", lang: "pt-BR"}`
   - datasets do tipo "store" com estes caminhos:
     - `vagas` → `data/radar/vagas`
     - `execucoes` → `data/radar/execucoes`
     - `pedidos` → `data/radar/pedidos`
     - `progresso` → `data/radar/progresso`
     - `perfil` → `data/radar/perfil`
   - `data/radar/perfil`, `doc_id` `perfil`: `{nome, trilhas}`, sem nenhum outro dado pessoal.
     - `nome`: o primeiro nome, que aparece no topo do painel.
     - `trilhas`: uma entrada `{id, nome}` para cada trilha de `busca.trilhas`, na ordem do perfil. `id` é o slug do nome (ex.: `product-manager`) e deve ser o mesmo `TRILHA_ID` das rotinas.
     - Se `busca.todas_as_vagas` não estiver vazio, acrescente `{id: "outras", nome: "Outras vagas"}`.
     - Grave também `trilhas_ordem`: os mesmos nomes separados por `|` (ex.: `"Product Manager|Liderança|Outras vagas"`). O painel usa esse texto quando o armazenamento achata listas.
     - O caminho precisa ter um número ímpar de partes (coleção/documento/coleção), por isso é `data/radar/perfil` e não `data/perfil`.
     - Essas trilhas viram os filtros do painel. Quando a pessoa mudar as trilhas no perfil (`jobhunting-setup`), regrave este documento.
   - `files/vendor.js` e `files/app.js`: o conteúdo de `dist/`, no formato `{text}`
   - `files/index.html`:
     ```html
     <meta name="dash-one-writer">
     <div id="job-hunting" data-draw="app" data-source="vagas execucoes pedidos progresso perfil">—</div>
     <script src="vendor.js"></script>
     <script src="app.js"></script>
     ```
   - `automacao/coletor`: `{text: <conteúdo de scripts/coletor.py>}`
   - `automacao/gerador_cv`: `{text: <conteúdo de scripts/gerador_cv.py>}`
4. **Perfil privado para as rotinas:** grave em `data/users/me`, `doc_id` `perfil`, `{json: <conteúdo do profile.json>}`.
   - O subcaminho `data/users/<você>` só é legível por você.
   - **Nunca** grave o perfil em caminhos públicos do dashboard.
5. Leia `data/users/me` `check` e `runs` para confirmar que o painel carregou. Entregue o link.

## Atualizar
Depois de mudar o código, rode `npm run build` e regrave **só** `files/app.js` com `if_version`. `vendor.js` só muda quando a versão do React muda.

## Privacidade
- Quem abrir o link do dashboard vê as vagas, as notas e os currículos enviados como asset.
- Não grave nesse dashboard salário, autoidentificação, contato pessoal nem dados do bloco `candidatura`.
