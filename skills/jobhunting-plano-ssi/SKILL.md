---
name: jobhunting-plano-ssi
description: "Gera para a pessoa o \"Material de crescimento do SSI no LinkedIn\", um plano de 30 dias com pilares do SSI, como e quando postar, como comentar, rotina diária, vagas ocultas por empresa, calendário com datas e 13 posts escritos a partir do perfil dela (PDF e DOCX). Use quando o usuário pedir plano de LinkedIn, SSI, Social Selling Index, crescer no LinkedIn, calendário de posts ou ideias de publicação."
model: claude-sonnet-5-5
---

# JobHunting – plano de crescimento do SSI no LinkedIn

- **Modelo e arquétipos dos posts:** `${CLAUDE_PLUGIN_ROOT}/templates/linkedin/plano-ssi.md`. Leia antes de começar.
- **Gerador:** `${CLAUDE_PLUGIN_ROOT}/scripts/gerador_plano_ssi.py`.
- **Perfil:** `${JOBHUNTING_HOME:-~/.jobhunting}/profile.json`.

## Passos
1. Leia o perfil: trajetória, resultado de destaque, experiências, trilhas, palavras-chave e mensagens.
2. Pergunte (com AskUserQuestion, se fizer sentido):
   - **Data de início:** padrão é a próxima segunda-feira.
   - **SSI atual, se souber:** usado só para dar contexto.
   - **Temas que quer evitar:** por exemplo, o empregador atual.
3. Escreva o `plano.json`:
   - `area`, `hashtags_exemplo` e `lideres_exemplo`, a partir da área da pessoa.
   - **2 `comentarios_exemplo`:** reconhecem o ponto do autor, trazem uma experiência real da pessoa e fecham com uma pergunta.
   - **`mensagem_recrutador`:** segue o modelo do Passo 3, com `foco_cargo` e `conquista_principal`.
   - **13 `posts` com os arquétipos do modelo:**
     - de 80 a 150 palavras;
     - primeira linha forte e quebra de linha a cada 1 ou 2 frases;
     - pergunta no fim e de 3 a 5 hashtags;
     - **só números e fatos do perfil**, no tom da pessoa, sem clichês.
4. Gere o material:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/gerador_plano_ssi.py" plano.json
   ```
5. Entregue o PDF e o DOCX e explique em 3 linhas como usar:
   - publicar na terça, quinta e sábado;
   - engajar nos outros dias;
   - registrar o SSI toda semana.

   Lembre que a pessoa deve revisar cada post com as próprias palavras antes de publicar.

**Não publique** no LinkedIn por ela. O plano é para ela executar.
