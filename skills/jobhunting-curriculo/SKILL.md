---
name: jobhunting-curriculo
description: Gera o currículo no modelo ATS do JobHunting (PDF e DOCX, uma coluna, até 2 páginas) com os dados da pessoa, adaptado a uma trilha (ex.: Product Manager ou IT Manager) ou a uma vaga específica, sem inventar fatos. Use quando o usuário pedir currículo, CV, "adaptar meu currículo", "currículo ATS" ou colar uma vaga.
---

# JobHunting – currículo ATS

**Modelo:** `${CLAUDE_PLUGIN_ROOT}/templates/curriculo/modelo-ats.md`. Leia antes de começar.
**Gerador:** `${CLAUDE_PLUGIN_ROOT}/scripts/gerador_cv.py`. Requer `pip install reportlab python-docx`.
**Perfil:** `${JOBHUNTING_HOME:-~/.jobhunting}/profile.json`, bloco `curriculo`.

## Regra de ouro
Só fatos do perfil. Você pode:
- escolher os títulos-alvo;
- reescrever o resumo com o vocabulário da trilha ou da vaga;
- reordenar e enxugar bullets.

**Nunca** crie números, cargos, empresas, ferramentas ou certificações.

## Passos
1. **Confira o perfil.** Se o bloco `curriculo` estiver vazio ou com os textos do exemplo, peça o currículo atual da pessoa (PDF, DOCX ou texto) e preencha o bloco seguindo o modelo:
   - titulos_alvo por trilha
   - resumo em 2 parágrafos
   - resultado_destaque e trajetoria
   - experiências: empresa, cidade, cargo, área, período, escopo e bullets
   - formação, formação complementar e certificações por grupo
   - idiomas

   Confirme com a pessoa os números e as datas ambíguas. Salve no perfil.
2. **Defina o alvo:**
   - **trilha:** uma versão por trilha, como a de Produto e a de Liderança;
   - **vaga:** link ou texto. Liste os 5 a 8 requisitos e o que no perfil comprova cada um. Mostre também as lacunas.
3. Escreva `ajustes.json` com o que muda:
   - `titulos`, se for diferente de `titulos_alvo[trilha]`;
   - `resumo`;
   - `experiencias` com os bullets reordenados, priorizando os que provam os requisitos.
4. Gere o currículo:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/gerador_cv.py" --trilha "<trilha>" --ajustes ajustes.json \
     --saida "${JOBHUNTING_HOME:-$HOME/.jobhunting}/curriculos/<Nome>_<Empresa>_<Cargo>"
   ```
5. Abra o PDF gerado e confira:
   - até 2 páginas;
   - nenhum texto de exemplo restante (ex.: "Empresa Atual", "Verbo de ação");
   - datas no mesmo formato.
6. Entregue os caminhos do PDF e do DOCX, os 3 pontos mais fortes para a vaga e as lacunas. Ofereça a carta (`jobhunting-carta`).

A candidatura é da pessoa. Só ajude a enviar se `busca.candidatura_automatica` for true e ela pedir explicitamente.
