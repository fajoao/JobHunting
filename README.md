# JobHunting

Assistente de busca de emprego que roda no **Claude Code** como plugin (agentes e skills). A pessoa responde a algumas perguntas sobre si mesma, e o JobHunting:

- **encontra vagas** em portais de carreira públicos e dá um **match de 0 a 100** com o perfil dela;
- monta o **currículo no modelo ATS** (PDF e DOCX), adaptado a cada trilha ou vaga, sem inventar fatos;
- escreve a **carta de apresentação** no modelo de 4 parágrafos;
- gera o **guia de abordagem a recrutadores**: os 4 textos, a busca booleana e as 8 formas de achar vagas ocultas;
- gera o **plano de crescimento no LinkedIn (SSI)**, com calendário de 30 dias e 13 posts escritos a partir da trajetória dela;
- mantém o **registro de contatos** e impede mensagens repetidas para a mesma pessoa;
- publica um **painel web** (React) e cria **rotinas agendadas** de busca e follow-up.

Nenhum dado pessoal fica neste repositório: tudo vem do perfil local da pessoa (`~/.jobhunting/profile.json`).

**Dúvidas?** Veja as [Perguntas frequentes](#perguntas-frequentes-faq). **Precisa de plano pago?** Os scripts rodam de graça, sem IA. O painel, as rotinas e os agentes precisam de recursos pagos do Claude. Veja [Roda na versão gratuita do Claude, ChatGPT ou Gemini?](#roda-na-versão-gratuita-do-claude-chatgpt-ou-gemini).

> Arquitetura e diagramas: [docs/arquitetura.md](docs/arquitetura.md) · Privacidade: [docs/privacidade.md](docs/privacidade.md) · Segurança: [SECURITY.md](SECURITY.md)

## Sumário
- [Instalação](#instalação)
- [O que a aplicação faz](#o-que-a-aplicação-faz)
- [Agentes](#agentes)
- [**Modelos: o que cada agente e skill usa** (Opus, Sonnet e Haiku)](#modelos-o-que-cada-agente-e-skill-usa)
- [Skills](#skills)
- [Funciona em outras IAs?](#funciona-em-outras-ias)
- [Roda na versão gratuita do Claude, ChatGPT ou Gemini?](#roda-na-versão-gratuita-do-claude-chatgpt-ou-gemini)
- [Uso sem nenhuma IA](#uso-sem-nenhuma-ia)
- [Dica: envie o currículo em Markdown](#dica-envie-o-currículo-em-markdown)
- [Seus dados](#seus-dados)
- [Limites e uso responsável](#limites-e-uso-responsável)
- [Perguntas frequentes (FAQ)](#perguntas-frequentes-faq)
- [Estrutura do repositório](#estrutura-do-repositório)
- [Contribuindo](#contribuindo)

---

## Instalação

### No Claude Code (recomendado)
```text
/plugin marketplace add fajoao/JobHunting
/plugin install jobhunting@jobhunting
```
Depois, escreva para o agente: *"quero procurar vagas de Product Manager"*. Na primeira vez, ele roda o cadastro.

### Dependências dos scripts
```bash
pip install -r scripts/requirements.txt   # reportlab e python-docx (PDF e DOCX)
```
Python 3.9 ou mais recente. O coletor de vagas usa só a biblioteca padrão.

---

## O que a aplicação faz

| Módulo | O que faz | Saída |
|---|---|---|
| **Cadastro** | Entrevista (Claude) ou perguntas no terminal (`setup_perfil.py`). Sugere converter o currículo para Markdown para gastar menos tokens. Nunca pede CPF, RG ou senhas. Autoidentificação é opcional. | `~/.jobhunting/profile.json` (permissão 600) |
| **Coleta de vagas** | Pergunta em quais sites buscar (LinkedIn, Big Techs, bancos e fintechs, empresas de tecnologia ou sites específicos). Lê APIs públicas (Greenhouse, Lever, Workday, Oracle HCM, Gupy, Amazon Jobs, Google Careers, Microsoft Careers); em Microsoft, Amazon e Google traz todas as vagas no Brasil. Filtra por trilha, senioridade, local, idioma e empresas excluídas, e calcula o match. No LinkedIn, monta a busca booleana por trilha e devolve o link. | `~/.jobhunting/vagas-AAAAMMDD.json` |
| **Currículo ATS** | Esqueleto fixo (uma coluna, até 2 páginas, seções padrão); muda títulos, resumo e ordem dos bullets por trilha ou vaga | PDF e DOCX em `curriculos/` |
| **Carta de apresentação** | Cabeçalho igual ao do currículo e 4 parágrafos (interesse, trajetória, resultado, contribuição) | PDF e DOCX em `cartas/` |
| **Guia de recrutadores** | 4 textos com os dados da pessoa, busca booleana dos cargos-alvo e 8 táticas de vagas ocultas com exemplos personalizados | PDF e DOCX em `linkedin/` |
| **Plano de SSI no LinkedIn** | Pilares do SSI, como e quando postar, como comentar, rotina diária, vagas ocultas por empresa, calendário de 30 dias com datas e 13 posts | PDF e DOCX em `linkedin/` |
| **LinkedIn no dia a dia** | Abre a busca booleana de vagas, lista recrutadores, confere quem aceitou o convite, prepara o follow-up e registra tudo | `contatos.csv` |
| **Painel web** | KPIs, funil, gráficos de match, lista de vagas (Abrir, Marcar como aplicada, Excluir), botão "Buscar agora" e progresso das buscas. Os filtros de trilha vêm das trilhas que a pessoa escolheu na entrevista (mais "Outras vagas", se houver) | Artifact do Claude (tipo Dashboard) |
| **Rotinas** | Busca por trilha 2x ao dia, resumo diário, verificador do "Buscar agora" e Texto 2 no LinkedIn | Rotinas na nuvem e tarefas locais |

---

## Agentes

| Agente | Modelo | Papel | Ferramentas |
|---|---|---|---|
| **`jobhunting`** (orquestrador) | Opus 5.5 | Confere se existe perfil (senão roda o setup), entende o pedido, decide o caminho e delega aos subagentes, em paralelo quando possível (ex.: currículo e carta para a mesma vaga; kit de início). Aplica as regras de privacidade, verdade e confirmação de ações externas. Fecha cada tarefa dizendo o que foi feito e o próximo passo. | Read, Write, Edit, Bash, Glob, Grep, WebFetch, Skill, Task, AskUserQuestion |
| **`jobhunting-curriculo`** | Opus 5.5 | Adapta o currículo ATS à trilha ou à vaga: mapeia requisitos para fatos do perfil, reordena e reescreve sem inventar e aponta lacunas. Entrega o `ajustes.json`. | Read, Write, Bash, WebFetch, Skill |
| **`jobhunting-carta`** | Sonnet 5.5 | Escreve a carta de 4 parágrafos citando um desafio real da vaga. Entrega o `carta.json`. | Read, Write, Bash, WebFetch, Skill |
| **`jobhunting-linkedin-crescimento`** | Sonnet 5.5 | Cria a estratégia de 30 dias para o SSI e escreve os 13 posts a partir da trajetória da pessoa. Entrega o `plano.json`. Não publica por ela. | Read, Write, Bash, Skill, AskUserQuestion |
| **`jobhunting-executor`** | Haiku 5.5 | Executa o que já foi decidido: roda os geradores a partir dos JSON, confere páginas e arquivos, instala dependências, roda a coleta e grava dados. Não decide conteúdo. | Read, Write, Edit, Bash, Glob, Grep |
| **`jobhunting-coletor`** | Haiku 5.5 | Roda o coletor, revisa o match lendo as descrições (ajusta até ±10 pontos, com o motivo), marca as vagas novas e devolve uma tabela com links. Nunca se candidata. | Read, Write, Bash, Glob, Grep, WebFetch, Skill |
| **`jobhunting-recrutadores`** | Haiku 5.5 | Gera o guia de abordagem e cuida do dia a dia com recrutadores a partir dos modelos. Por padrão só prepara as mensagens; confere registro e histórico para nunca repetir uma mensagem. | Read, Write, Edit, Bash, Glob, Grep, Skill |

Diagrama do orquestrador: [docs/arquitetura.md#2-um-agente-jobhunting-orquestrador](docs/arquitetura.md).

---

## Modelos: o que cada agente e skill usa

Cada agente e skill declara o modelo no topo do arquivo (campo `model:`). A regra é usar o modelo mais forte só onde um erro custa caro, e o mais barato no que roda com frequência.

### Os três níveis
| Nível | Modelo | Quando usar |
|---|---|---|
| **Crítico** | **Opus 5.5** (`claude-opus-5-5`) | O erro chega ao recrutador ou se repete em todas as buscas seguintes |
| **Escrita com modelo fixo** | **Sonnet 5.5** (`claude-sonnet-5-5`) | Textos que seguem um modelo e que a pessoa revisa antes de usar |
| **Execução** | **Haiku 5.5** (`claude-haiku-5-5`) | Tarefas já decididas: rodar scripts, preencher modelos, gravar dados. Rodam todo dia. |

### Configuração atual
| Tipo | Nome | Modelo | Por quê |
|---|---|---|---|
| Agente | `jobhunting` (orquestrador) | **Opus 5.5** | Entende o pedido, decide o caminho, aplica as regras e revisa o que os outros entregam |
| Agente | `jobhunting-curriculo` | **Opus 5.5** | Liga cada requisito da vaga ao que o perfil comprova sem exagerar, e aponta lacunas. Um currículo fraco ou inflado vai direto ao recrutador. |
| Skill | `jobhunting-setup` | **Opus 5.5** | Transforma o CV em perfil e cria as regras de título de cada trilha. Uma regra errada faz o coletor perder ou trazer vagas erradas em **todas** as buscas. |
| Skill | `jobhunting-curriculo` | **Opus 5.5** | Mesmo motivo do agente de currículo |
| Agente | `jobhunting-carta` | **Sonnet 5.5** | Quatro parágrafos com estrutura fixa e fatos que vêm do perfil. A pessoa revisa antes de enviar. |
| Agente | `jobhunting-linkedin-crescimento` | **Sonnet 5.5** | Plano e 13 posts a partir de arquétipos prontos. Nada é publicado sem revisão da pessoa. |
| Skill | `jobhunting-carta` | **Sonnet 5.5** | Mesmo motivo do agente de carta |
| Skill | `jobhunting-plano-ssi` | **Sonnet 5.5** | Mesmo motivo do agente de crescimento |
| Agente | `jobhunting-executor` | **Haiku 5.5** | Gera PDF e DOCX a partir de JSON pronto, confere os arquivos, roda a coleta e grava dados. Não decide conteúdo. |
| Agente | `jobhunting-coletor` | **Haiku 5.5** | Roda o coletor e revisa o match dentro de um limite de ±10 pontos. Roda várias vezes por dia. |
| Agente | `jobhunting-recrutadores` | **Haiku 5.5** | Preenche os 4 textos a partir do modelo e mantém o registro de contatos |
| Skill | `jobhunting-buscar-vagas` | **Haiku 5.5** | Pergunta os sites, roda o coletor e monta a tabela |
| Skill | `jobhunting-abordagem-recrutadores` | **Haiku 5.5** | Preenche o guia a partir do modelo |
| Skill | `jobhunting-linkedin` | **Haiku 5.5** | Monta a busca booleana e o registro de contatos |
| Skill | `jobhunting-dashboard` | **Haiku 5.5** | Build e gravação dos dados no painel |
| Skill | `jobhunting-rotinas` | **Haiku 5.5** | Preenche os modelos de rotina e cria os agendamentos |

### Como o trabalho flui
1. O orquestrador (Opus) entende o pedido e escolhe o caminho.
2. Os agentes de conteúdo escrevem só o JSON: o currículo no Opus, a carta e o plano no Sonnet.
3. O orquestrador revisa o que veio do Sonnet. Se encontrar algo inventado ou genérico demais, refaz essa parte.
4. O `jobhunting-executor` (Haiku) gera o PDF e o DOCX a partir do JSON e confere o resultado.
5. Se o Haiku errar duas vezes, ou se a tarefa pedir julgamento, ela volta para o Opus.

Quando uma skill de escrita é usada direto, sem o orquestrador, ela roda inteira no modelo dela, inclusive a geração dos arquivos.

### Por que não usar o Haiku em tudo
- **Custo:** setup, currículo, carta e plano rodam poucas vezes (uma vez por vaga, ou por mês). O que consome o plano todo dia é a coleta e as rotinas, e essas já estão no Haiku. Rebaixar as tarefas de conteúdo economizaria pouco.
- **Risco:** no currículo e no setup, um modelo menor tende a enfeitar fatos ou errar as regras de busca, e o erro se propaga. Na carta e no plano, o Sonnet mantém a qualidade com custo menor, e a pessoa revisa antes de usar.

### Para trocar
Edite o campo `model:` no topo do agente (`agents/*.md`) ou da skill (`skills/*/SKILL.md`). Aceita um ID de modelo (`claude-...`) ou um apelido (`opus`, `sonnet`, `haiku`, `inherit`). O `scripts/checar_seguranca.py` confere se todos têm um modelo válido.

---

## Skills

| Skill (`/jobhunting:...`) | Modelo | O que faz | Usa |
|---|---|---|---|
| `jobhunting-setup` | Opus 5.5 | Entrevista, monta o perfil (inclusive a partir do CV atual) e oferece o kit de início | `setup_perfil.py`, `profile.example.json` |
| `jobhunting-buscar-vagas` | Haiku 5.5 | Busca vagas agora e mostra as melhores com link, sem se candidatar | `coletor.py` |
| `jobhunting-curriculo` | Opus 5.5 | Currículo no modelo ATS para uma trilha ou vaga | `gerador_cv.py`, `templates/curriculo/modelo-ats.md` |
| `jobhunting-carta` | Sonnet 5.5 | Carta de apresentação no modelo de 4 parágrafos | `gerador_carta.py`, `templates/carta/modelo-carta.md` |
| `jobhunting-plano-ssi` | Sonnet 5.5 | Plano de crescimento do SSI com calendário e 13 posts | `gerador_plano_ssi.py`, `templates/linkedin/plano-ssi.md` |
| `jobhunting-abordagem-recrutadores` | Haiku 5.5 | Guia com os 4 textos, a busca booleana e as vagas ocultas | `gerador_guia_recrutadores.py`, `templates/linkedin/abordagem-recrutadores.md` |
| `jobhunting-linkedin` | Haiku 5.5 | Busca booleana de vagas, recrutadores, quem aceitou, follow-up e registro | `templates/mensagens-recrutadores.md`, `contatos.csv` |
| `jobhunting-dashboard` | Haiku 5.5 | Cria ou atualiza o painel (build React, datasets, perfil privado para as rotinas) | `app/` |
| `jobhunting-rotinas` | Haiku 5.5 | Cria as rotinas agendadas a partir dos modelos, sem dados pessoais no texto | `templates/rotinas/` |

Diagrama de uma skill (currículo ATS): [docs/arquitetura.md#3-uma-skill-jobhunting-curriculo-curriculo-ats](docs/arquitetura.md).

---

## Funciona em outras IAs?

Sim, em boa parte. O JobHunting foi feito em camadas, e só algumas dependem do Claude:

| Camada | Depende do Claude? | Como usar em outra IA |
|---|---|---|
| **Scripts Python** (`scripts/`) | **Não** | Funcionam sozinhos ou chamados por qualquer agente que rode comandos. Recebem JSON e geram PDF e DOCX. |
| **Modelos** (`templates/`) | **Não** | Markdown puro: esqueleto do CV, da carta, do plano e do guia. Sirvem como instruções para qualquer modelo. |
| **Skills** (`skills/*/SKILL.md`) | Formato aberto | O formato *Agent Skills* (pasta com `SKILL.md` e frontmatter `name`/`description`) é um padrão aberto. Onde não houver suporte, use o texto do `SKILL.md` como prompt ou instruções, trocando `${CLAUDE_PLUGIN_ROOT}` pelo caminho do repositório. |
| **Agentes** (`agents/*.md`) | Formato de subagente do Claude Code | O corpo é um prompt de sistema comum. Copie para o "system prompt" ou as "instructions" de outra plataforma (GPTs, Assistants, Gemini, frameworks como LangGraph ou CrewAI) e dê a ela ferramentas equivalentes: ler e escrever arquivos e rodar comandos. A orquestração com `Task` vira chamadas entre agentes do framework escolhido. |
| **Painel web** (`app/`) | Hoje roda como Artifact do Claude | O React é independente. `src/runtime.ts` isola a fonte de dados: troque o `dashboardRuntime` por uma API sua (ex.: Supabase) para hospedar em qualquer lugar. O `mockRuntime` mostra o contrato. |
| **Rotinas** (`templates/rotinas/`) | Rotinas do Claude | A coleta (`coletor.py`) pode rodar em cron, GitHub Actions ou qualquer agendador. A revisão com IA pode usar a API de outro modelo. |

---

## Roda na versão gratuita do Claude, ChatGPT ou Gemini?

**Só em parte.** Os scripts Python rodam sem nenhuma IA, e qualquer chat gratuito escreve os textos a partir dos modelos. O painel, as rotinas automáticas e os agentes dependem de recursos pagos do Claude.

> Os planos e limites de cada empresa mudam com frequência. Confira na página de planos de cada uma antes de decidir.

| Parte do JobHunting | Claude grátis | ChatGPT grátis | Gemini grátis |
|---|---|---|---|
| **Scripts Python**: coleta de vagas, currículo ATS, carta, plano de SSI, guia de recrutadores | Sim, rodam no seu computador sem IA | Sim | Sim |
| **Escrever os textos** (resumo do CV, carta, posts) com os modelos de `templates/` | Sim: cole o modelo e o seu currículo `.md` no chat | Sim | Sim |
| **Agentes e skills** `/jobhunting:*` | Não: precisam do Claude Code, que exige plano pago ou chave de API | Não roda como plugin | Em parte: o Gemini CLI tem uso gratuito com conta Google e pode seguir os `SKILL.md` como instruções e rodar os scripts (não testado) |
| **Painel web com dados** (Buscar agora, progresso, Marcar como aplicada) | Não: usa Artifacts com banco de dados e rotinas do Claude | Não | Não |
| **Rotinas automáticas** (busca 2x ao dia, resumo diário) | Não: usam as rotinas do Claude Code | Não | Não |
| **Ações no navegador** (LinkedIn pelo Claude in Chrome) | Não: recurso pago | Não | Não |

### Como usar de graça
1. Crie o perfil no terminal: `python3 scripts/setup_perfil.py`.
2. Busque vagas: `python3 -I scripts/coletor.py vagas.json --perguntar`. Você recebe as vagas com match e link, inclusive a busca booleana do LinkedIn.
3. Agende a coleta de graça:
   - **Mac e Linux:** cron, por exemplo `15 7,13 * * 1-5 cd ~/JobHunting && python3 -I scripts/coletor.py ~/.jobhunting/vagas-$(date +\%Y\%m\%d).json`.
   - **Windows:** Agendador de Tarefas.
   - **Na nuvem:** GitHub Actions, num repositório **privado**, porque o perfil tem dados pessoais.
4. Escreva os textos num chat gratuito: cole o modelo (`templates/curriculo/modelo-ats.md`, `templates/carta/modelo-carta.md` ou `templates/linkedin/plano-ssi.md`) e o seu currículo em `.md`. Depois gere o PDF e o DOCX com os scripts da seção abaixo.
5. Converta o currículo para `.md` antes de colar no chat. Isso ajuda a caber nos limites dos planos gratuitos (veja a dica de Markdown mais abaixo).

### O que você perde sem plano pago
- O painel web com KPIs, gráficos e o botão "Buscar agora".
- As rotinas automáticas na nuvem e o resumo diário.
- A revisão do match vaga a vaga feita pela IA. Sem ela, vale só a nota heurística do coletor.
- As ações no navegador, como conferir convites e mandar mensagens no LinkedIn.

---

## Uso sem nenhuma IA
```bash
python3 scripts/setup_perfil.py                              # cria ~/.jobhunting/profile.json
python3 -I scripts/coletor.py --listar-sites                 # sites e grupos disponíveis
python3 -I scripts/coletor.py vagas.json --perguntar         # pergunta os sites, coleta e pontua
python3 -I scripts/coletor.py vagas.json --sites linkedin,big_techs
python3 scripts/gerador_cv.py --trilha "Product Manager"     # currículo ATS
python3 scripts/gerador_carta.py carta.json                  # carta (você escreve os 4 parágrafos)
python3 scripts/gerador_guia_recrutadores.py guia.json       # guia de recrutadores
python3 scripts/gerador_plano_ssi.py plano.json              # plano de SSI
```
O formato de cada JSON está no início de cada script e em `templates/`.

---

## Dica: envie o currículo em Markdown

Converta o seu PDF ou DOCX para Markdown (`.md`) antes de enviá-lo ao Claude ou a outra IA. O `.md` é texto puro e **gasta bem menos tokens** do que um PDF ou DOCX. As skills de cadastro e de currículo mostram esta dica na hora de pedir o arquivo.

| Ferramenta | Sistemas | Converte | Comando ou caminho |
|---|---|---|---|
| **MarkItDown** (Microsoft, grátis) | Mac, Windows, Linux | PDF, DOCX | `markitdown curriculo.pdf -o curriculo.md` |
| **Pandoc** (grátis) | Mac, Windows, Linux | DOCX | `pandoc curriculo.docx -t gfm -o curriculo.md` |
| **Docling** (IBM, grátis) | Mac, Windows, Linux | PDF com colunas e tabelas, DOCX | `docling curriculo.pdf --to md` |
| **Typora** (pago, com interface gráfica) | Mac, Windows, Linux | DOCX | Arquivo > Importar |
| **Google Docs** (navegador) | Qualquer um | DOCX, PDF | Arquivo > Fazer download > Markdown (.md) |

Instalação, cuidados com privacidade e como conferir o resultado estão em [`templates/converter-para-markdown.md`](templates/converter-para-markdown.md).

## Seus dados

| O quê | Onde fica | Vai para o GitHub? |
|---|---|---|
| Perfil (nome, contato, preferências, currículo, dados de formulário) | `~/.jobhunting/profile.json` ou `$JOBHUNTING_HOME` | **Não** |
| Contatos com recrutadores (dados de terceiros) | `~/.jobhunting/contatos.csv` | **Não** |
| Currículos, cartas, planos, guias e vagas coletadas | `~/.jobhunting/` | **Não** |
| Código, modelos, exemplos fictícios | este repositório | Sim |

O JobHunting **nunca pede CPF, RG, dados bancários ou senhas**. Detalhes em [docs/privacidade.md](docs/privacidade.md).

## Limites e uso responsável
- **LinkedIn:** não tem API pública de vagas e proíbe automação de convites e mensagens. O JobHunting prepara os textos; enviar pelo navegador é escolha da pessoa, com risco de restrição da conta.
- **Candidatura automática:** vem desligada. Quando ligada, só envia em formulários públicos, sem login nem CAPTCHA, com dados que a pessoa informou.
- **Verdade:** currículo, carta, posts e mensagens usam só fatos do perfil. Os agentes apontam lacunas e nunca as preenchem com invenção.
- **Custos:** o uso do Claude e das rotinas na nuvem conta no plano Claude da pessoa.

## Perguntas frequentes (FAQ)

### Começando

**Qual modelo de IA cada parte usa?**
Opus 5.5 no orquestrador, no currículo e no setup; Sonnet 5.5 na carta e no plano de SSI; Haiku 5.5 em toda a execução (coleta, recrutadores, painel, rotinas e geração dos arquivos). A tabela completa, com o motivo de cada escolha, está em [Modelos: o que cada agente e skill usa](#modelos-o-que-cada-agente-e-skill-usa).

**O que é o JobHunting?**
Um assistente de busca de emprego. Ele encontra vagas com match ao seu perfil e monta o currículo ATS, a carta de apresentação, o plano de crescimento no LinkedIn e as mensagens para recrutadores. Roda como plugin do Claude Code, e os scripts também funcionam sem nenhuma IA.

**Preciso saber programar?**
Não, para usar com o Claude Code: você conversa com o agente e ele faz o resto. Sem IA, basta saber rodar alguns comandos no terminal, que estão em [Uso sem nenhuma IA](#uso-sem-nenhuma-ia).

**Como começo?**
Instale o plugin (veja [Instalação](#instalação)) e escreva ao agente algo como *"quero procurar vagas de Product Manager"*. Na primeira vez ele faz uma entrevista curta para montar o seu perfil.

**Que perguntas a entrevista faz?**
- Dados de contato.
- Cargos que você procura (as trilhas).
- Onde buscar e cidades aceitas.
- Nível de inglês e empresas a evitar.
- Dados opcionais de formulário.
- O seu currículo atual.

Nada de CPF, RG, dados bancários ou senhas.

**O que são as "trilhas"?**
São os grupos de cargo que você procura, por exemplo "Product Manager" e "Liderança". Cada trilha tem os títulos que contam para ela, vira um filtro no painel e pode ter a própria rotina de busca. Você escolhe os nomes na entrevista.

**Funciona no plano gratuito?**
Em parte. Os scripts rodam de graça, mas o painel, as rotinas e os agentes precisam de recursos pagos do Claude. Veja a [tabela completa](#roda-na-versão-gratuita-do-claude-chatgpt-ou-gemini).

**Funciona com ChatGPT ou Gemini?**
Os scripts e os modelos funcionam com qualquer IA. Os agentes e skills podem virar instruções em outras plataformas. Veja [Funciona em outras IAs?](#funciona-em-outras-ias).

### Vagas

**Em quais sites ele busca?**
O JobHunting pergunta antes de cada busca. As opções são:
- **LinkedIn**, com busca booleana;
- **Big Techs:** Microsoft, Amazon, Google, NVIDIA, Salesforce, Red Hat, Oracle e Dell;
- **bancos e fintechs;**
- **empresas de tecnologia;**
- **sites específicos** que você indicar.

A lista completa sai com `python3 -I scripts/coletor.py --listar-sites`.

**Posso adicionar outra empresa?**
Sim, se ela publica vagas em Greenhouse, Lever, Workday, Oracle HCM ou Gupy. Inclua a empresa em `busca.fontes` no seu perfil, com `{id, nome, grupo, tipo, args}`. Só use APIs públicas de vagas.

**Por que o LinkedIn só traz um link, e não a lista de vagas?**
O LinkedIn não tem API pública de vagas e proíbe automação. O coletor monta a busca booleana por trilha e devolve o link. Se você pedir, o Claude lê a lista no seu navegador, já logado, só para listar título, empresa e link.

**Por que aparecem vagas fora da minha área na Microsoft, Amazon e Google?**
Nessas empresas o padrão é trazer **todas** as vagas no Brasil, sem filtro do seu perfil. As que não batem com as suas trilhas aparecem na aba "Outras vagas", que abre com todas as vagas, sem o corte de match. Com `busca.todas_as_vagas_so_tecnologia: true` (padrão no exemplo), essa aba fica só com vagas de tecnologia. Para mudar as empresas, edite `busca.todas_as_vagas` no perfil; vazio desliga.

**Como o match de 0 a 100 é calculado?**
O coletor soma quatro coisas:
- o encaixe do título com a trilha;
- as palavras-chave do seu perfil encontradas na descrição;
- a localização;
- a senioridade.

Ele também desconta pontos quando a vaga pede inglês acima do seu nível ou um cargo acima de gerente. Com o Claude, cada vaga acima do corte ainda é revisada pela IA, que pode ajustar até 10 pontos e explica o motivo.

**Ele se candidata sozinho?**
Não, por padrão. A candidatura automática vem desligada. Se você ligar, ela só acontece em formulários públicos, sem login nem CAPTCHA, e com os dados que você informou. Nunca cria conta e nunca contorna bloqueios.

**A Microsoft apareceu em "erros". E agora?**
O site da Microsoft às vezes recusa chamadas de scripts (erro 429). A coleta das outras empresas segue normalmente. Com o Claude, a skill lê a mesma busca no navegador; sem IA, rode de novo mais tarde.

### Currículo, carta e LinkedIn

**O currículo inventa experiência para "dar match"?**
Não. Currículo, carta, posts e mensagens usam só fatos do seu perfil. O JobHunting pode reordenar e reescrever o que existe com o vocabulário da vaga, e aponta as lacunas em vez de preenchê-las.

**Por que converter o currículo para Markdown?**
O `.md` é texto puro e gasta bem menos tokens que um PDF ou DOCX, o que ajuda nos limites do plano. Veja as ferramentas em [Dica: envie o currículo em Markdown](#dica-envie-o-currículo-em-markdown).

**O que é o SSI do LinkedIn e o que o plano entrega?**
O *Social Selling Index* é a nota do LinkedIn para a força da sua presença na rede. O plano de 30 dias traz:
- os pilares do SSI;
- quando e como postar;
- como comentar;
- uma rotina diária;
- 13 posts escritos a partir da sua trajetória.

O JobHunting não publica nada por você.

**Ele manda mensagens para recrutadores por mim?**
O padrão é preparar os textos para você enviar. O Claude só envia pelo navegador se você pedir explicitamente, em lotes pequenos. Antes de cada envio, ele confere no registro de contatos e no histórico da conversa para nunca mandar a mesma mensagem duas vezes à mesma pessoa. O LinkedIn proíbe automação e pode restringir a conta.

### Painel e rotinas

**Como mudo as trilhas que aparecem no painel?**
Peça ao agente para atualizar o perfil (skill `jobhunting-setup`). Os filtros do painel vêm das trilhas do perfil e mudam sem mexer no código.

**Com que frequência as rotinas rodam?**
O padrão sugerido é 2 vezes por dia útil para cada trilha, mais um resumo diário. Você escolhe os horários ao criar as rotinas, e o intervalo mínimo é de 1 hora.

**O botão "Buscar agora" roda na hora?**
Ele põe um pedido na fila. Um verificador roda a cada 30 minutos e dispara as buscas, e o progresso aparece no painel.

**As rotinas gastam meu plano?**
Sim. As rotinas e as ações do Claude contam no uso do seu plano. O verificador do "Buscar agora" é o que mais roda (32 vezes por dia), por isso o agente avisa antes de criá-lo.

### Privacidade e segurança

**Onde ficam meus dados?**
No seu computador, em `~/.jobhunting/`, com acesso só para o seu usuário. Nada pessoal vai para este repositório. Para as rotinas na nuvem, o perfil fica numa área do painel que só a sua conta lê. Veja [Seus dados](#seus-dados).

**Quem consegue ver o meu painel?**
Quem tiver o link. Por isso o painel nunca recebe salário, autoidentificação, contato pessoal ou CPF: só vagas, notas e o seu nome.

**E se uma vaga tiver instruções escondidas para a IA?**
Os agentes e as rotinas tratam o texto de vagas, sites e e-mails como dados, nunca como ordens. Pedidos vindos de dentro desse conteúdo são ignorados e aparecem no resumo como suspeitos. Veja [SECURITY.md](SECURITY.md).

**Como apago tudo?**
Apague a pasta `~/.jobhunting/`, desinstale o plugin (`/plugin uninstall jobhunting@jobhunting`) e exclua o painel e as rotinas nas páginas do Claude.

## Estrutura do repositório
```
.claude-plugin/   plugin.json e marketplace.json
agents/           orquestrador e 5 subagentes
skills/           9 skills
scripts/          coletor, geradores (CV, carta, plano SSI, guia), renderizador PDF/DOCX, setup
profile/          profile.example.json (fictício)
templates/        modelos: currículo ATS, carta, plano SSI, abordagem a recrutadores, mensagens, rotinas
app/              painel web (React + TypeScript + Vite)
docs/             arquitetura (diagramas), privacidade
SECURITY.md       modelo de segurança e como reportar problemas
```

## Contribuindo
- **Nova empresa:** inclua a fonte em `FONTES_PADRAO` (`scripts/coletor.py`), com `id`, `nome` e `grupo`, ou em `busca.fontes` no seu perfil. Use só APIs públicas de vagas.
- **Novo documento:** crie um gerador que monte uma lista de blocos e chame `jobhunting_docs.gerar`.
- **Pull requests:** nunca inclua dados pessoais reais em exemplos, testes ou capturas de tela.
