---
name: jobhunting-setup
description: Onboarding do JobHunting. Entrevista o usuário, uma pergunta por vez, para criar ou revisar o perfil de busca de vagas (~/.jobhunting/profile.json) com dados pessoais, cargos-alvo, cidades, idioma, dados de formulário e currículo. Use quando o usuário começar a usar o JobHunting, disser "configurar", "meu perfil", "atualizar meus dados", ou quando outra skill JobHunting não encontrar o perfil.
---

# JobHunting – configuração do perfil

O perfil é o único lugar com dados pessoais do usuário. Todas as outras skills, scripts e rotinas leem dele.

- **Arquivo:** `${JOBHUNTING_HOME:-~/.jobhunting}/profile.json` (permissão 600, fora de qualquer repositório).
- **Modelo com todos os campos:** `${CLAUDE_PLUGIN_ROOT}/profile/profile.example.json`.
- **Alternativa sem Claude:** `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/setup_perfil.py`.

## Regras de privacidade (inegociáveis)
- **Nunca peça** CPF, RG, número de documento, dados bancários ou senhas. Se o usuário oferecer, recuse e não grave.
- Autoidentificação (gênero, raça/cor, PcD, orientação) é **opcional**: pergunte se ele quer responder; vazio = "prefiro não informar".
- Explique uma vez que os dados ficam só no computador dele e só são usados para buscar vagas, montar currículo e preencher formulários **quando ele autorizar**.

## Como conduzir
1. Verifique se o perfil já existe. Se existir, mostre um resumo (sem salário nem autoidentificação) e pergunte o que mudar.
2. Peça o currículo atual (PDF, DOCX ou texto do LinkedIn) e preencha o bloco `curriculo` no formato do modelo ATS (`${CLAUDE_PLUGIN_ROOT}/templates/curriculo/modelo-ats.md`):
   - `titulos_alvo` por trilha;
   - `resumo` em 2 parágrafos;
   - `resultado_destaque` e `trajetoria`;
   - `experiencias`: empresa, cidade, cargo, área, período, escopo e bullets;
   - `formacao`, `formacao_complementar` e `certificacoes` por grupo;
   - `idiomas`.

   **Nunca invente fatos.** Confirme números e datas que estiverem ambíguos.
3. Faça a entrevista em blocos curtos, uma pergunta por vez (use AskUserQuestion quando houver opções):
   - **Pessoal:** nome, e-mail, telefone, LinkedIn, cidade, UF.
   - **Busca:**
     - trilhas de cargo; para cada uma, confirme os títulos que contam e gere as regex `titulos`/`titulos_fortes`;
     - remoto no Brasil e cidades aceitas;
     - mudança de cidade e nível de inglês;
     - empresas a excluir (ex.: empregador atual);
     - vagas afirmativas a incluir (opcional);
     - cortes de match (padrão 65 e 80).
   - **Palavras-chave:** proponha pesos a partir do currículo (1 a 6) e peça confirmação.
   - **Candidatura automática:** explique que só ocorre em formulários públicos, sem login nem CAPTCHA; padrão **desligado**.
   - **Formulários (opcional):** empresa atual, remuneração, pretensão por trilha, regra PJ, disponibilidade, modelo, autoidentificação.
   - **Mensagens:**
     - como se apresenta (`foco_cargo`);
     - área (`foco`);
     - principal conquista com número;
     - versões em inglês, se ele quiser falar com recrutadores de fora.
4. Grave o JSON seguindo exatamente a estrutura do exemplo, com `chmod 600`. Valide o JSON lendo de volta.
5. Ofereça o **kit de início**, gerado em paralelo pelo agente `jobhunting`: currículo ATS por trilha, guia de abordagem a recrutadores e plano de SSI no LinkedIn.
6. Termine dizendo o que ele pode fazer agora: `/jobhunting:jobhunting-buscar-vagas`, `/jobhunting:jobhunting-curriculo`, `/jobhunting:jobhunting-carta`, `/jobhunting:jobhunting-plano-ssi`, `/jobhunting:jobhunting-abordagem-recrutadores`, `/jobhunting:jobhunting-linkedin`, `/jobhunting:jobhunting-dashboard`, `/jobhunting:jobhunting-rotinas`.
