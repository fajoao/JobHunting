---
name: jobhunting-rotinas
description: Cria as rotinas agendadas do JobHunting a partir dos modelos (busca por trilha 2x ao dia, resumo diário, verificador do botão Buscar agora e Texto 2 no LinkedIn), preenchendo os dados do usuário. Use quando o usuário pedir para automatizar, agendar, "rodar todo dia" ou criar as rotinas do JobHunting.
---

# JobHunting – rotinas agendadas

Os modelos ficam em `${CLAUDE_PLUGIN_ROOT}/templates/rotinas/`. Cada um tem, no topo, o agendamento sugerido e o tipo:
- **nuvem:** Claude Code routine, criada com a ferramenta RemoteTrigger;
- **local:** tarefa agendada do app Claude, criada com `create_scheduled_task`.

| Modelo | Tipo | Precisa de |
|---|---|---|
| `busca-trilha.md` | nuvem, uma por trilha | dashboard criado (`jobhunting-dashboard`) |
| `resumo-diario.md` | nuvem | dashboard |
| `buscar-agora-verificador.md` | nuvem, duas cópias (:00 e :30) | dashboard e conector Claude_Code_Remote |
| `linkedin-texto2.md` | local | Chrome com Claude in Chrome e LinkedIn logado |

## Passos
1. Confirme com o usuário quais rotinas ele quer e os horários. Mostre a tabela acima.
2. Para cada uma, troque os `{{...}}` pelos valores do usuário:
   - `PRIMEIRO_NOME`, `DASHBOARD_URL`, `TRILHA`, `TRILHA_ID` (slug), `JOBHUNTING_HOME`, `PLUGIN_ROOT`;
   - `TRIGGERS_POR_TRILHA`: os ids das rotinas de busca já criadas.
3. **Nunca cole no texto da rotina** dados pessoais (CPF, salário, autoidentificação, telefone).
   - As rotinas de nuvem leem o perfil do dashboard, em `data/users/me/perfil`.
   - A rotina local lê `~/.jobhunting/profile.json`.
4. Crie as rotinas de nuvem com `RemoteTrigger action=create`. Use o mesmo `environment_id` das rotinas que já existirem e limite `mcp_connections` ao necessário.
   - O intervalo mínimo entre execuções de uma rotina é 1 hora.
   - Mostre ao usuário o link e o próximo horário de cada rotina.
5. Crie a rotina local com `create_scheduled_task`. Avise que ela só roda com o app aberto.
6. Ofereça um teste: `RemoteTrigger action=run` numa rotina, depois `get_run_log` para conferir.

As rotinas gastam o uso do plano Claude do usuário. Avise antes de criar o verificador do "Buscar agora", que roda 32 vezes por dia.
