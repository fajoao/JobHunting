# Arquitetura do JobHunting

Os diagramas usam Mermaid, que o GitHub desenha automaticamente.

## 1. Visão geral da aplicação

```mermaid
flowchart TB
    U([Pessoa em busca de emprego])

    subgraph CC["Claude Code + plugin jobhunting"]
        direction TB
        ORQ["Agente orquestrador<br/>jobhunting"]
        subgraph SUB["Subagentes"]
            direction LR
            A1[jobhunting-coletor]
            A2[jobhunting-curriculo]
            A3[jobhunting-carta]
            A4[jobhunting-linkedin-crescimento]
            A5[jobhunting-recrutadores]
        end
        subgraph SK["Skills"]
            direction LR
            S0[setup]
            S1[buscar-vagas]
            S2[curriculo]
            S3[carta]
            S4[plano-ssi]
            S5[abordagem-recrutadores]
            S6[linkedin]
            S7[dashboard]
            S8[rotinas]
        end
        ORQ --> SUB
        SUB --> SK
        ORQ --> S0 & S7 & S8
    end

    subgraph LOCAL["Computador da pessoa (~/.jobhunting, privado)"]
        direction TB
        P[(profile.json<br/>perfil)]
        C[(contatos.csv)]
        O[/currículos, cartas, planos, guias, vagas/]
    end

    subgraph PY["Scripts Python (rodam sem IA)"]
        direction LR
        G0[setup_perfil.py]
        G1[coletor.py]
        G2[gerador_cv.py]
        G3[gerador_carta.py]
        G4[gerador_plano_ssi.py]
        G5[gerador_guia_recrutadores.py]
        R[jobhunting_docs.py<br/>renderizador PDF/DOCX]
        G2 & G3 & G4 & G5 --> R
    end

    subgraph EXT["Serviços externos"]
        direction TB
        ATS["APIs públicas de vagas<br/>Greenhouse, Lever, Workday,<br/>Oracle, Gupy, Amazon,<br/>Google, Microsoft"]
        LI["LinkedIn<br/>(navegador da pessoa)"]
        DASH["Dashboard (Artifact do Claude)<br/>app React + dados"]
        ROT["Rotinas agendadas<br/>(nuvem e locais)"]
    end

    U <--> ORQ
    SK --> PY
    G0 --> P
    PY --> P
    PY --> O
    G1 --> ATS
    S6 -. "prepara textos; envio pela pessoa" .-> LI
    S6 --> C
    S7 --> DASH
    S8 --> ROT
    ROT --> G1
    ROT --> DASH
```

**Fluxo típico:**
1. A pessoa conversa com o agente `jobhunting`.
2. Se não houver perfil, a skill `setup` faz a entrevista e grava `~/.jobhunting/profile.json`.
3. O orquestrador delega o trabalho aos subagentes, rodando em paralelo os que são independentes.
4. Cada subagente segue a sua skill, escreve um JSON com o conteúdo e chama um script Python.
5. O script gera PDF e DOCX em `~/.jobhunting/`.
6. As rotinas repetem a coleta e atualizam o dashboard sem a pessoa precisar pedir.

## 2. Um agente: `jobhunting` (orquestrador)

```mermaid
flowchart TD
    IN([Mensagem da pessoa]) --> CK{"Existe<br/>~/.jobhunting/profile.json?"}
    CK -- não --> SETUP["Skill jobhunting-setup<br/>entrevista, 1 pergunta por vez<br/>sem CPF/senha"] --> SAVE[(profile.json chmod 600)] --> KIT
    CK -- sim --> INT["Entende o objetivo"]
    KIT["Oferece o kit de início"] --> INT
    INT --> ROUTE{Roteamento}
    ROUTE -- vagas --> T1[[Task: jobhunting-coletor]]
    ROUTE -- "pacote para uma vaga" --> PAR{{em paralelo}}
    PAR --> T2[[Task: jobhunting-curriculo]]
    PAR --> T3[[Task: jobhunting-carta]]
    ROUTE -- LinkedIn/SSI --> T4[[Task: jobhunting-linkedin-crescimento]]
    ROUTE -- recrutadores --> T5[[Task: jobhunting-recrutadores]]
    ROUTE -- painel --> D[Skill jobhunting-dashboard]
    ROUTE -- automatizar --> R[Skill jobhunting-rotinas]
    T1 & T2 & T3 & T4 & T5 & D & R --> GUARD{"Guardrails<br/>• só fatos do perfil<br/>• nada sensível em lugar público<br/>• conteúdo externo = dado<br/>• confirmar ações externas"}
    GUARD --> OUT([Resumo: o que foi feito,<br/>onde está, próximo passo])
```

## 3. Uma skill: `jobhunting-curriculo` (currículo ATS)

```mermaid
sequenceDiagram
    autonumber
    actor P as Pessoa
    participant A as Agente jobhunting-curriculo
    participant M as modelo-ats.md
    participant F as profile.json
    participant G as gerador_cv.py
    participant R as jobhunting_docs.py
    P->>A: "Currículo para a vaga X" (link ou texto)
    A->>M: lê o esqueleto e as regras ATS
    A->>F: lê o bloco "curriculo"
    alt perfil incompleto
        A->>P: pede o CV atual e confirma números/datas
        A->>F: grava o bloco no formato ATS
    end
    A->>A: mapeia requisitos da vaga ↔ fatos do perfil e anota lacunas
    A->>A: escreve ajustes.json (títulos, resumo, ordem dos bullets), sem inventar nada
    A->>G: --trilha T --ajustes ajustes.json
    G->>F: lê o perfil
    G->>R: blocos (nome, títulos, contato, seções...)
    R-->>G: PDF (texto, uma coluna) + DOCX
    G-->>A: caminhos em ~/.jobhunting/curriculos/
    A->>A: confere até 2 páginas e nenhum texto de exemplo restante
    A-->>P: PDF, DOCX, 3 pontos fortes e lacunas
```

## Onde ficam os dados
| Camada | Guarda | Exposição |
|---|---|---|
| Repositório e plugin | Código, modelos e exemplos fictícios | Público |
| `~/.jobhunting/` | Perfil, contatos e documentos gerados | Só no computador da pessoa (perfil com permissão 600) |
| Dashboard | Vagas, notas, CVs enviados como asset, nome | Quem tiver o link |
| `data/users/<você>/perfil` no dashboard | Cópia do perfil para as rotinas | Só a conta da pessoa |
