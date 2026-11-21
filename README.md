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

> Arquitetura e diagramas: [docs/arquitetura.md](docs/arquitetura.md) · Privacidade: [docs/privacidade.md](docs/privacidade.md) · Segurança: [SECURITY.md](SECURITY.md)

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
| **Cadastro** | Entrevista (Claude) ou perguntas no terminal (`setup_perfil.py`). Nunca pede CPF, RG ou senhas. Autoidentificação é opcional. | `~/.jobhunting/profile.json` (permissão 600) |
| **Coleta de vagas** | Lê APIs públicas (Greenhouse, Lever, Workday, Oracle HCM, Gupy, Amazon Jobs, Google Careers), filtra por trilha, senioridade, local, idioma e empresas excluídas, e calcula o match | `~/.jobhunting/vagas-AAAAMMDD.json` |
| **Currículo ATS** | Esqueleto fixo (uma coluna, até 2 páginas, seções padrão); muda títulos, resumo e ordem dos bullets por trilha ou vaga | PDF e DOCX em `curriculos/` |
| **Carta de apresentação** | Cabeçalho igual ao do currículo e 4 parágrafos (interesse, trajetória, resultado, contribuição) | PDF e DOCX em `cartas/` |
| **Guia de recrutadores** | 4 textos com os dados da pessoa, busca booleana dos cargos-alvo e 8 táticas de vagas ocultas com exemplos personalizados | PDF e DOCX em `linkedin/` |
| **Plano de SSI no LinkedIn** | Pilares do SSI, como e quando postar, como comentar, rotina diária, vagas ocultas por empresa, calendário de 30 dias com datas e 13 posts | PDF e DOCX em `linkedin/` |
| **LinkedIn no dia a dia** | Abre a busca booleana de vagas, lista recrutadores, confere quem aceitou o convite, prepara o follow-up e registra tudo | `contatos.csv` |
| **Painel web** | KPIs, funil, gráficos de match, lista de vagas (Abrir, Marcar como aplicada, Excluir), botão "Buscar agora" e progresso das buscas | Artifact do Claude (tipo Dashboard) |
| **Rotinas** | Busca por trilha 2x ao dia, resumo diário, verificador do "Buscar agora" e Texto 2 no LinkedIn | Rotinas na nuvem e tarefas locais |

---

## Agentes

| Agente | Papel | Ferramentas |
|---|---|---|
| **`jobhunting`** (orquestrador) | Confere se existe perfil (senão roda o setup), entende o pedido e delega aos subagentes, em paralelo quando possível (ex.: currículo e carta para a mesma vaga; kit de início). Aplica as regras de privacidade, verdade e confirmação de ações externas. Fecha cada tarefa dizendo o que foi feito e o próximo passo. | Read, Write, Edit, Bash, Glob, Grep, WebFetch, Skill, Task, AskUserQuestion |
| **`jobhunting-coletor`** | Roda o coletor, revisa o match lendo as descrições (ajusta até ±10 pontos, com o motivo), marca as vagas novas e devolve uma tabela com links. Nunca se candidata. | Read, Write, Bash, Glob, Grep, WebFetch, Skill |
| **`jobhunting-curriculo`** | Monta o currículo ATS por trilha ou vaga: mapeia requisitos para fatos do perfil, reordena e reescreve sem inventar, confere o PDF e aponta lacunas. | Read, Write, Bash, WebFetch, Skill |
| **`jobhunting-carta`** | Escreve a carta de 4 parágrafos citando um desafio real da vaga e gera o PDF e o DOCX. | Read, Write, Bash, WebFetch, Skill |
| **`jobhunting-linkedin-crescimento`** | Cria o plano de 30 dias para o SSI e escreve os 13 posts a partir da trajetória da pessoa. Não publica por ela. | Read, Write, Bash, Skill, AskUserQuestion |
| **`jobhunting-recrutadores`** | Gera o guia de abordagem e cuida do dia a dia com recrutadores. Por padrão só prepara as mensagens; confere registro e histórico para nunca repetir uma mensagem. | Read, Write, Edit, Bash, Glob, Grep, Skill |

Diagrama do orquestrador: [docs/arquitetura.md#2-um-agente-jobhunting-orquestrador](docs/arquitetura.md).

---

## Skills

| Skill (`/jobhunting:...`) | O que faz | Usa |
|---|---|---|
| `jobhunting-setup` | Entrevista, monta o perfil (inclusive a partir do CV atual) e oferece o kit de início | `setup_perfil.py`, `profile.example.json` |
| `jobhunting-buscar-vagas` | Busca vagas agora e mostra as melhores com link, sem se candidatar | `coletor.py` |
| `jobhunting-curriculo` | Currículo no modelo ATS para uma trilha ou vaga | `gerador_cv.py`, `templates/curriculo/modelo-ats.md` |
| `jobhunting-carta` | Carta de apresentação no modelo de 4 parágrafos | `gerador_carta.py`, `templates/carta/modelo-carta.md` |
| `jobhunting-plano-ssi` | Plano de crescimento do SSI com calendário e 13 posts | `gerador_plano_ssi.py`, `templates/linkedin/plano-ssi.md` |
| `jobhunting-abordagem-recrutadores` | Guia com os 4 textos, a busca booleana e as vagas ocultas | `gerador_guia_recrutadores.py`, `templates/linkedin/abordagem-recrutadores.md` |
| `jobhunting-linkedin` | Busca booleana de vagas, recrutadores, quem aceitou, follow-up e registro | `templates/mensagens-recrutadores.md`, `contatos.csv` |
| `jobhunting-dashboard` | Cria ou atualiza o painel (build React, datasets, perfil privado para as rotinas) | `app/` |
| `jobhunting-rotinas` | Cria as rotinas agendadas a partir dos modelos, sem dados pessoais no texto | `templates/rotinas/` |

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

## Uso sem nenhuma IA
```bash
python3 scripts/setup_perfil.py                              # cria ~/.jobhunting/profile.json
python3 -I scripts/coletor.py vagas.json                     # coleta e pontua vagas
python3 scripts/gerador_cv.py --trilha "Product Manager"     # currículo ATS
python3 scripts/gerador_carta.py carta.json                  # carta (você escreve os 4 parágrafos)
python3 scripts/gerador_guia_recrutadores.py guia.json       # guia de recrutadores
python3 scripts/gerador_plano_ssi.py plano.json              # plano de SSI
```
O formato de cada JSON está no início de cada script e em `templates/`.

---

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
- **Nova empresa:** inclua a fonte em `FONTES_PADRAO` (`scripts/coletor.py`) ou em `busca.fontes` no seu perfil. Use só APIs públicas de vagas.
- **Novo documento:** crie um gerador que monte uma lista de blocos e chame `jobhunting_docs.gerar`.
- **Pull requests:** nunca inclua dados pessoais reais em exemplos, testes ou capturas de tela.
