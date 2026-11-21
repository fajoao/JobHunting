# JobHunting

Assistente de busca de emprego que roda no **Claude Code** como plugin (skills e agentes). Ele:

- **coleta vagas** em APIs públicas de portais de carreira (Greenhouse, Lever, Workday, Oracle HCM, Gupy, Amazon Jobs, Google Careers) e dá um **match de 0 a 100** com o seu perfil;
- **adapta o currículo** (DOCX e PDF) e escreve a carta de apresentação para cada vaga, sem inventar fatos;
- ajuda no **LinkedIn**: busca booleana de vagas e os 4 textos para recrutadores, com um registro que impede mensagens repetidas;
- publica um **painel web** (React) com KPIs, funil, gráficos, lista de vagas, botão "Buscar agora" e progresso das buscas;
- cria **rotinas agendadas** (busca 2x ao dia, resumo, follow-up de recrutadores).

Na primeira vez, o JobHunting **pergunta os seus dados** e monta o seu perfil. Nenhum dado pessoal fica neste repositório.

## Instalação (Claude Code)

```text
/plugin marketplace add fajoao/JobHunting
/plugin install jobhunting@jobhunting
```

Depois converse com o agente **JobHunting** ("quero procurar vagas de Product Manager") ou chame as skills direto:

| Skill | O que faz |
|---|---|
| `/jobhunting:jobhunting-setup` | Entrevista e cria o seu perfil (rode primeiro) |
| `/jobhunting:jobhunting-buscar-vagas` | Busca vagas agora e mostra as melhores com link |
| `/jobhunting:jobhunting-curriculo` | Currículo e carta para uma vaga |
| `/jobhunting:jobhunting-linkedin` | Busca booleana, recrutadores e follow-up |
| `/jobhunting:jobhunting-dashboard` | Cria ou atualiza o painel web |
| `/jobhunting:jobhunting-rotinas` | Agenda as rotinas diárias |

### Agentes
- **`jobhunting`**: orquestrador. Confere o perfil, escolhe o caminho e delega para os subagentes (em paralelo, quando dá).
- **`jobhunting-coletor`**: coleta e pontua vagas.
- **`jobhunting-curriculo`**: currículo e carta.
- **`jobhunting-recrutadores`**: LinkedIn e recrutadores.

## Uso sem o Claude

Os scripts funcionam sozinhos, com Python 3.9 ou mais recente:

```bash
python3 scripts/setup_perfil.py                  # cria ~/.jobhunting/profile.json
python3 -I scripts/coletor.py vagas.json         # coleta e pontua vagas
pip install python-docx
python3 scripts/gerador_cv.py --a4               # gera o currículo
```

## Seus dados

| O quê | Onde fica | Vai para o GitHub? |
|---|---|---|
| Perfil (nome, contato, preferências, currículo, dados de formulário) | `~/.jobhunting/profile.json` (ou `$JOBHUNTING_HOME`) | **Não** |
| Contatos com recrutadores | `~/.jobhunting/contatos.csv` | **Não** |
| Vagas coletadas e currículos gerados | `~/.jobhunting/` | **Não** |
| Modelo do perfil, scripts, skills, agentes, app | este repositório | Sim |

O JobHunting **nunca pede CPF, RG, dados bancários ou senhas**. Autoidentificação (gênero, raça/cor, PcD) é opcional. Veja [docs/privacidade.md](docs/privacidade.md).

## Estrutura

```
.claude-plugin/   plugin.json e marketplace.json (instalação no Claude Code)
agents/           orquestrador JobHunting e 3 subagentes
skills/           6 skills (setup, buscar-vagas, curriculo, linkedin, dashboard, rotinas)
scripts/          coletor.py, gerador_cv.py, setup_perfil.py
profile/          profile.example.json (modelo, sem dados reais)
templates/        mensagens para recrutadores, modelos de rotinas, cabeçalho do registro de contatos
app/              painel web (React + TypeScript + Vite)
docs/             privacidade e limites
```

## Limites e uso responsável
- **LinkedIn:** não tem API pública de vagas e proíbe automação de convites e mensagens. O JobHunting prepara os textos. Enviar pelo navegador é escolha sua, com risco de restrição da conta.
- **Candidatura automática:** vem desligada. Quando ligada, só envia em formulários públicos, sem login nem CAPTCHA.
- **Custos:** as rotinas na nuvem e o uso do Claude contam no seu plano Claude.

## Contribuindo
Para adicionar uma empresa, inclua a fonte em `FONTES_PADRAO` (`scripts/coletor.py`) ou em `busca.fontes` no seu perfil. Use só APIs públicas de vagas.
