---
name: jobhunting-buscar-vagas
description: "Busca vagas agora nos portais de carreira (Greenhouse, Lever, Workday, Oracle, Gupy, Amazon, Google) com o perfil do usuário, pontua o match de 0 a 100 e mostra as melhores com link, sem se candidatar. Use quando o usuário pedir \"buscar vagas\", \"o que tem de novo\", \"vagas com match\", ou quiser rodar a coleta manualmente."
---

# JobHunting – buscar vagas

## Pré-requisito
Perfil em `${JOBHUNTING_HOME:-~/.jobhunting}/profile.json`. Se não existir, rode a skill `jobhunting-setup` primeiro.

## Passos
1. Rode o coletor (pode levar uns 10 minutos, porque o Workday limita requisições):
   ```bash
   python3 -I "${CLAUDE_PLUGIN_ROOT}/scripts/coletor.py" "${JOBHUNTING_HOME:-$HOME/.jobhunting}/vagas-$(date +%Y%m%d).json" [--trilha "Nome da trilha"]
   ```
   Rode em segundo plano se o ambiente permitir e avise o usuário.
2. Leia o JSON de saída. Compare com execuções anteriores (`vagas-*.json`) para marcar o que é **novo**.
3. Para as vagas com match ≥ `busca.corte_voce_aplica`, leia título e descrição e revise o match contra o bloco `curriculo` do perfil. Ajuste até ±10 pontos e explique em uma frase. Nunca invente experiência.
4. Mostre uma tabela ordenada por match com: título, empresa, local, match, motivo e **link**. Destaque os alertas, como inglês fluente ou nível acima.
5. **Não se candidate.** Ofereça os próximos passos:
   - gerar currículo para uma vaga (`jobhunting-curriculo`);
   - gravar no dashboard (`jobhunting-dashboard`);
   - criar a rotina diária (`jobhunting-rotinas`).

## Fontes
- **Padrão:** `FONTES_PADRAO` em `scripts/coletor.py`.
- **Trocar ou adicionar empresas:** edite `busca.fontes` no perfil, no mesmo formato `{tipo, args}`. Só use APIs públicas de vagas.
- **LinkedIn:** não é lido por este coletor. Para vagas do LinkedIn, use a skill `jobhunting-linkedin` (busca booleana aberta no navegador ou alertas por e-mail).
