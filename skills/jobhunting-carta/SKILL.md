---
name: jobhunting-carta
description: Escreve a carta de apresentação no modelo do JobHunting (cabeçalho igual ao currículo, 4 parágrafos: interesse, trajetória, resultado e contribuição), em PDF e DOCX, com os dados da pessoa e adaptada à vaga ou à trilha. Use quando o usuário pedir carta de apresentação, cover letter ou "carta para a vaga".
---

# JobHunting – carta de apresentação

- **Modelo:** `${CLAUDE_PLUGIN_ROOT}/templates/carta/modelo-carta.md`. Leia antes de começar.
- **Gerador:** `${CLAUDE_PLUGIN_ROOT}/scripts/gerador_carta.py`.
- **Perfil:** `${JOBHUNTING_HOME:-~/.jobhunting}/profile.json`. Use os blocos `pessoal`, `curriculo` (resumo, trajetoria, resultado_destaque, experiencias) e `mensagens`.

## Passos
1. **Alvo:** pegue empresa, cargo, nome de quem recruta (se houver) e trilha. Se houver vaga, leia a descrição e escolha **um desafio específico** para citar no §4.
2. **Os 4 parágrafos** (de 250 a 400 palavras no total), só com fatos do perfil:
   - **§1 Interesse e quem é:** vaga e empresa, identidade profissional, anos de experiência, domínios, cargo e empresa atual e foco.
   - **§2 Trajetória:** onde começou, os marcos com empresa e cargo, o que faz hoje e o que essa combinação permite.
   - **§3 Resultado:** "Um dos resultados de que mais me orgulho é..." com o número, as 2 ou 3 ações que levaram a ele e outras entregas.
   - **§4 Contribuição:** o desafio da vaga, 2 ou 3 forças, disponibilidade e agradecimento.
   - **Ajuste à trilha:**
     - **Produto:** visão, discovery, roadmap e métricas.
     - **Liderança:** equipes, governança, riscos, custos e entrega.
   - Use o artigo certo para a empresa (na Amazon, no Nubank).
3. Grave `carta.json` com `{empresa, cargo, recrutador, trilha, paragrafos:[4]}` e gere a carta:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/gerador_carta.py" carta.json
   ```
4. Mostre o texto à pessoa e aplique os ajustes que ela pedir. Entregue os caminhos do PDF e do DOCX.

Não invente fatos. Se não houver vaga, mantenha `[desafio ou área específica da vaga]` para a pessoa completar.
