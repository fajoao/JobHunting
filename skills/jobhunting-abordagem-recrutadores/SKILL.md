---
name: jobhunting-abordagem-recrutadores
description: "Gera para a pessoa o guia \"Textos para recrutadores e vagas ocultas\" (PDF e DOCX), com os 4 textos de abordagem (convite, depois de conectar, depois de se candidatar e follow-up) escritos com os dados dela, a busca booleana dos cargos-alvo e as 8 formas de achar vagas ocultas com exemplos personalizados. Use quando o usuário pedir mensagens para recrutadores, textos de abordagem, como falar com recrutador ou guia de vagas ocultas."
model: claude-haiku-5-5
---

# JobHunting – guia de abordagem a recrutadores

- **Modelo:** `${CLAUDE_PLUGIN_ROOT}/templates/linkedin/abordagem-recrutadores.md`. Leia antes de começar.
- **Gerador:** `${CLAUDE_PLUGIN_ROOT}/scripts/gerador_guia_recrutadores.py`.
- **Perfil:** `${JOBHUNTING_HOME:-~/.jobhunting}/profile.json`. Use os blocos `mensagens`, `busca` e `curriculo`.

## Passos
1. Leia o perfil.
   - Se `mensagens.foco_cargo`, `foco` ou `conquista_principal` estiverem vazios ou com o texto do exemplo, pergunte à pessoa e grave no perfil.
   - A conquista precisa ter um número real.
2. Escreva o `guia.json`:
   - **`textos.t1` a `t4`:** siga o modelo e deixe `[Nome]`, `[Empresa]` e `[cargo]` para preencher a cada envio.
     - O t1 tem no máximo 300 caracteres. Confira contando.
   - **`textos_en`:** só se a pessoa quiser falar com recrutadores de fora.
   - **`busca_booleana`:** junte os títulos das trilhas com os temas de `busca.palavras_chave`.
   - **`termos_alerta` e `cargos_lideres`.**
   - **3 exemplos** (comentário em post, mensagem para a rede, mensagem sobre uma dor da empresa), com experiências reais da pessoa.
3. Gere o guia:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/gerador_guia_recrutadores.py" guia.json
   ```
4. Entregue o PDF e o DOCX. Lembre:
   - o envio é feito pela própria pessoa, porque o LinkedIn proíbe automação;
   - cada contato deve ser registrado em `~/.jobhunting/contatos.csv`;
   - para usar os textos no dia a dia (buscar recrutadores, conferir quem aceitou, follow-up), a skill é `jobhunting-linkedin`.
