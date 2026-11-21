---
name: jobhunting-linkedin
description: "LinkedIn no JobHunting. Monta e abre a busca booleana de vagas a partir das trilhas do perfil, prepara os 4 textos para recrutadores (conexão, vagas não divulgadas, pós-candidatura e follow-up) e mantém o registro de contatos sem repetir mensagens. Use quando o usuário pedir busca booleana, vagas no LinkedIn, mensagem para recrutador, convites, follow-up ou vagas ocultas."
---

# JobHunting – LinkedIn

Guia completo e textos: `${CLAUDE_PLUGIN_ROOT}/templates/mensagens-recrutadores.md`.
Perfil: `${JOBHUNTING_HOME:-~/.jobhunting}/profile.json` (blocos `busca.trilhas` e `mensagens`).
Registro de contatos: `${JOBHUNTING_HOME:-~/.jobhunting}/contatos.csv`. O cabeçalho está em `${CLAUDE_PLUGIN_ROOT}/templates/contatos.example.csv`.

## Antes de agir: limites
- O LinkedIn **proíbe automação** de convites e mensagens e não tem API pública de vagas. Avise o usuário uma vez.
- O padrão é **preparar** os textos para ele enviar.
- Só envie pelo navegador (Claude in Chrome) se ele pedir explicitamente, em lotes de até 15 a 20 por dia, e revise cada tela antes de clicar em enviar.
- Contas sem Premium têm poucos convites com nota por mês.
- **Nunca** mande a mesma mensagem duas vezes para a mesma pessoa. Confira o registro **e** o histórico da conversa antes.

## 1. Busca booleana de vagas
1. Gere a busca a partir das trilhas: `python3 -I "${CLAUDE_PLUGIN_ROOT}/scripts/coletor.py" busca.json --sites linkedin`. O campo `linkedin` traz, por trilha, `("título 1" OR "título 2" ...) AND (<busca.linkedin.temas>)` e o link pronto.
2. Se preferir montar à mão, codifique a busca para URL e abra `https://www.linkedin.com/jobs/search-results/?keywords=<busca>&geoId=106057199` (Brasil).
   - Use `/jobs/search-results/`; o endereço antigo `/jobs/search/` não abre mais.
3. Se ele pedir, leia as páginas de resultados só para **listar** título, empresa, local e link. Não se candidate.
4. Salve a lista em `${JOBHUNTING_HOME:-~/.jobhunting}/buscas/` e deixe a aba aberta se ele quiser.

Observação: o LinkedIn interpreta a busca com IA e não segue o booleano à risca. Na busca de **pessoas**, expressões longas e com acento costumam voltar vazias. Encurte e tire os acentos.

## 2. Recrutadores (Textos 1 a 4)
- **Texto 1 (convite):** preencha `[Nome]` e `[Empresa]`, com o artigo correto (do/da). Use até 300 caracteres e o idioma da pessoa.
- **Texto 2:** só para quem **aceitou**. Confira em "Minha rede > Conexões", ordenado por recentes.
- **Texto 3:** depois de uma candidatura. **Texto 4:** follow-up de 7 a 10 dias depois do silêncio.
- Pule perfis que exigem o e-mail para conectar e empresas em `busca.empresas_excluidas`.
- Registre cada ação no `contatos.csv` logo depois que ela acontecer.

## 3. Rotina diária do Texto 2
Ofereça a rotina local `templates/rotinas/linkedin-texto2.md`, criada pela skill `jobhunting-rotinas`.
