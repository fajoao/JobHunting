---
name: jobhunting-buscar-vagas
description: "Busca vagas agora nos sites que o usuário escolher (LinkedIn com busca booleana, Big Techs como Microsoft, Amazon e Google, bancos e fintechs, empresas de tecnologia), pontua o match de 0 a 100 e mostra as melhores com link, sem se candidatar. Use quando o usuário pedir \"buscar vagas\", \"o que tem de novo\", \"vagas com match\", \"buscar no LinkedIn\" ou quiser rodar a coleta manualmente."
model: claude-haiku-5-5
---

# JobHunting – buscar vagas

## Pré-requisito
Perfil em `${JOBHUNTING_HOME:-~/.jobhunting}/profile.json`. Se não existir, rode a skill `jobhunting-setup` primeiro.

## 1. Pergunte onde buscar
1. Veja o catálogo de sites:
   ```bash
   python3 -I "${CLAUDE_PLUGIN_ROOT}/scripts/coletor.py" --listar-sites
   ```
2. Se o usuário ainda não disse os sites neste pedido, pergunte com `AskUserQuestion`, `multiSelect: true`:
   - pergunta: "Em quais sites quer buscar vagas?";
   - opções:
     - "Minha escolha salva", mostrando o que está em `busca.sites` no perfil;
     - "LinkedIn (busca booleana)";
     - "Big Techs", citando Microsoft, Amazon, Google e as demais do grupo;
     - "Bancos e empresas de tecnologia".
   - O usuário pode digitar sites específicos em "Other" (ex.: `microsoft, itau`).
3. Converta a resposta em `--sites`, com ids de grupo ou de site separados por vírgula:
   - grupos: `linkedin`, `big_techs`, `bancos`, `tech`, `personalizadas`;
   - "Bancos e empresas de tecnologia" vira `bancos,tech`.
4. Se a escolha for diferente da salva, pergunte se deve virar o novo padrão. Se sim, grave em `busca.sites` no perfil.

## 2. Rode o coletor
```bash
python3 -I "${CLAUDE_PLUGIN_ROOT}/scripts/coletor.py" "${JOBHUNTING_HOME:-$HOME/.jobhunting}/vagas-$(date +%Y%m%d).json" --sites <ids> [--trilha "Nome da trilha"]
```
- `--trilha` aceita mais de uma, separadas por vírgula. Use `"Outras vagas"` para incluir as vagas fora das trilhas das empresas de `busca.todas_as_vagas` (ex.: `--trilha "Product Manager,Outras vagas"`).
- Pode levar até uns 10 minutos quando inclui Workday, que limita requisições. Rode em segundo plano se o ambiente permitir e avise o usuário.
- **Todas as vagas:** nas empresas de `busca.todas_as_vagas` (padrão: Microsoft, Amazon e Google), o coletor traz todas as vagas no Brasil, sem filtro de cargo, senioridade ou cidade do perfil. As que não batem com nenhuma trilha vêm como "Outras vagas".
- **Nome da aba:** `busca.nome_trilha_todas_as_vagas` troca o nome "Outras vagas" (ex.: `"Big Techs"`). O coletor grava as vagas com esse nome, e `--trilha "Outras vagas"` continua valendo como apelido. Se renomear com vagas já gravadas, atualize também o campo `trilha` delas e a lista de trilhas do painel (`data/radar/perfil`).
- **Só tecnologia:** com `busca.todas_as_vagas_so_tecnologia: true`, as "Outras vagas" ficam só com cargos de tecnologia (engenharia, dados, cloud, segurança, produto, data center etc.). Logística, RH, vendas, manutenção e segurança do trabalho ficam de fora. A regra é `eh_tecnologia()` em `scripts/coletor.py`.
- **Oracle com todas as vagas:** a API da Oracle só busca por palavra-chave. Para aproximar "todas", adicione em `busca.fontes` uma fonte `oracle` com termos amplos (ex.: `brazil`, `sao paulo`, `engineer`, `analyst`) e inclua o `id` dela em `busca.todas_as_vagas`.
- **Microsoft:** às vezes responde 429 a scripts. Se aparecer em `erros`, abra `https://apply.careers.microsoft.com/careers?domain=microsoft.com&location=Brazil` no Claude in Chrome e liste as vagas da página.

## 3. LinkedIn (busca booleana)
O LinkedIn não tem API pública de vagas. Por isso o coletor só monta, no campo `linkedin` do JSON, uma busca por trilha:
- formato: `("título 1" OR "título 2" ...) AND (tema 1 OR tema 2)`;
- títulos: vêm de `titulos_linkedin` da trilha ou, se não existir, são extraídos da regex `titulos`;
- temas: vêm de `busca.linkedin.temas`;
- filtros: `geo_id` (padrão Brasil), `periodo` (`24h`, `semana`, `mes`) e `so_remoto`.

Mostre a busca e o link. Se o usuário quiser a lista:
1. Abra o link no Claude in Chrome, com o LinkedIn já logado pelo usuário.
2. Leia só título, empresa, local e link das primeiras páginas.
3. Junte à tabela com fonte "LinkedIn".

**Nunca** se candidate, salve vagas nem mande mensagens pelo LinkedIn nessa etapa.

## 4. Revise e mostre
1. Leia o JSON de saída. Compare com execuções anteriores (`vagas-*.json`) para marcar o que é **novo**.
2. Para as vagas com match ≥ `busca.corte_voce_aplica`, leia título e descrição e revise o match contra o bloco `curriculo` do perfil.
   - Ajuste até ±10 pontos e explique em uma frase.
   - Nunca invente experiência.
3. Mostre uma tabela ordenada por match com: título, empresa, local, match, motivo e **link**.
   - Destaque os alertas, como inglês fluente ou nível acima.
   - Mostre "Outras vagas" numa seção separada, por empresa.
4. **Não se candidate.** Ofereça os próximos passos:
   - gerar currículo para uma vaga (`jobhunting-curriculo`);
   - gravar no dashboard (`jobhunting-dashboard`);
   - criar a rotina diária (`jobhunting-rotinas`).

## Fontes
- **Catálogo:** `FONTES_PADRAO` e `GRUPOS` em `scripts/coletor.py`, mais o LinkedIn.
- **Adicionar empresas:** inclua em `busca.fontes` no perfil, no formato `{id, nome, grupo, tipo, args}`. Os tipos aceitos são `greenhouse`, `lever`, `workday`, `oracle`, `gupy`, `amazon`, `google` e `microsoft`. Só use APIs públicas de vagas.
