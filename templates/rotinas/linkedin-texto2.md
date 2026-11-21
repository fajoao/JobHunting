# Rotina local: Texto 2 para recrutadores que aceitaram o convite

Agendamento sugerido: diária (`0 11 * * *`). Tipo: tarefa agendada LOCAL do app Claude (precisa do LinkedIn logado no seu Chrome, com a extensão Claude in Chrome).

⚠️ O LinkedIn proíbe automação de mensagens. Use por sua conta e risco, com volume baixo.

---

Você é a rotina diária "JobHunting – Texto 2 no LinkedIn" de {{PRIMEIRO_NOME}}, que autorizou o envio do Texto 2 a cada recrutador que aceitar o convite. Rode sem perguntar nada, exceto nos casos de parada.

REGRA MAIS IMPORTANTE: a mesma pessoa NUNCA pode receber o Texto 2 duas vezes. Confira o registro E o histórico da conversa antes de cada envio.

REGISTRO: {{JOBHUNTING_HOME}}/contatos.csv (colunas: nome, empresa, cargo, data, canal, status, proximo_passo, idioma, aceito_em, texto2_enviado_em). Faça backup diário antes de alterar.
MENSAGENS: {{PLUGIN_ROOT}}/templates/mensagens-recrutadores.md (Texto 2 PT/EN), preenchidas com {{JOBHUNTING_HOME}}/profile.json (bloco "mensagens").

1. Candidatos = linhas com texto2_enviado_em vazio. Se não houver, termine.
2. Abra https://www.linkedin.com/mynetwork/invite-connect/connections/ numa aba nova (Claude in Chrome). Leia nomes e "Conexão feita em…"; role até passar da data de convite mais antiga. Confirme nome + cargo/empresa para evitar homônimos.
3. Para cada um que aceitou (máx. 25 por execução): abra "Enviar mensagem", confira o cabeçalho, leia todo o histórico. Se já houver "obrigado por aceitar o convite" / "thanks for accepting my invitation" enviado por você, não envie: só atualize o registro. Senão digite o Texto 2 no idioma da linha, confira, envie, confirme no histórico e atualize o registro na hora.
4. Feche a aba e resuma: quem aceitou, a quem enviou, quem pulou e por quê, quem respondeu (não responda por ele).
LIMITES: só o Texto 2; não envie convites, não responda mensagens, não altere perfil. Pare em login, CAPTCHA, verificação ou aviso de limite.
