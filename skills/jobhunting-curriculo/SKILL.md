---
name: jobhunting-curriculo
description: Gera um currículo personalizado (DOCX e PDF) e uma carta de apresentação curta para uma vaga específica, usando só os fatos do perfil do usuário. Use quando o usuário colar o link ou a descrição de uma vaga e pedir currículo, CV, carta ou "adaptar meu currículo".
---

# JobHunting – currículo para uma vaga

## Regra de ouro
**Nunca invente fatos.** Você pode:
- reordenar o que está no perfil;
- reescrever headline, resumo e competências;
- dar ênfase aos bullets que combinam com a vaga.

Não crie números, cargos, certificações ou tecnologias que não estejam no bloco `curriculo` do perfil.

## Passos
1. Leia o perfil (`${JOBHUNTING_HOME:-~/.jobhunting}/profile.json`) e a vaga (link ou texto).
2. Liste para o usuário os 5 a 8 requisitos centrais da vaga e o que no perfil comprova cada um. Mostre também as lacunas, com honestidade.
3. Escreva `ajustes.json` com os campos a sobrescrever do bloco `curriculo`: `headline`, `resumo`, `competencias` e `experiencias` com bullets reordenados ou reescritos.
4. Gere o currículo:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/gerador_cv.py" --ajustes ajustes.json --a4 \
     --saida "${JOBHUNTING_HOME:-$HOME/.jobhunting}/curriculos/<Empresa>_<Cargo>.docx"
   ```
   Requer `pip install python-docx`. Para gerar o PDF, é preciso o LibreOffice (`soffice`).
5. Escreva uma carta de apresentação de até 1.200 caracteres, no tom do usuário.
6. Entregue os caminhos dos arquivos. Ofereça o Texto 3 (mensagem ao recrutador depois de se candidatar), de `${CLAUDE_PLUGIN_ROOT}/templates/mensagens-recrutadores.md`.

A candidatura fica com o usuário. Só ajude a enviar se `busca.candidatura_automatica` for true e ele pedir explicitamente para aquela vaga.
