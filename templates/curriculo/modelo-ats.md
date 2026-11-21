# Modelo de currículo ATS do JobHunting

Este é o esqueleto que as skills e agentes seguem. O gerador `scripts/gerador_cv.py` monta o PDF e o DOCX a partir do bloco `curriculo` do perfil. Os textos abaixo são **estrutura**, não conteúdo: tudo vem dos dados da pessoa.

## Esqueleto

```
NOME COMPLETO                                              (caixa alta, negrito, centralizado)
TÍTULO-ALVO 1 | TÍTULO-ALVO 2 | TÍTULO-ALVO 3              (caixa alta, cinza; muda por trilha)
Cidade – UF | (DDD) telefone | e-mail | linkedin.com/in/... (centralizado)
──────────────────────────────────────────────────────────

RESUMO PROFISSIONAL
§1  Quem é: cargo/identidade + "mais de N anos de experiência em" + 3 a 4 domínios.
    Atua com/no que: 4 a 6 competências centrais da trilha.
§2  Contexto atual (ou mais recente): "Na [Empresa], atuo como [Cargo], liderando [o quê]..."
    + 2 ou 3 entregas que comprovam o perfil.
Resultado de destaque: um resultado com número (de A para B, em N meses, impacto).

EXPERIÊNCIA PROFISSIONAL
EMPRESA | Cidade – UF                                       (caixa alta, negrito)
Cargo | Área ou produto | Mmm/AAAA – Mmm/AAAA               (negrito, cinza)
Uma frase de escopo (opcional, para o cargo mais recente).
• Verbo de ação no passado + o que fez + resultado/impacto (número quando houver).
• 6 a 13 bullets no cargo atual; 4 a 8 nos anteriores; 2 a 4 nos mais antigos.

FORMAÇÃO ACADÊMICA
Curso – Grau | Instituição | Período ou "Em andamento, conclusão prevista em AAAA".

FORMAÇÃO COMPLEMENTAR (o título pode nomear o tema, ex.: "em Produtos e IA")
Curso – Escola; Curso – Escola; ...

CERTIFICAÇÕES PROFISSIONAIS
Grupo (ex.: fornecedor): certificação; certificação; ...

IDIOMAS (opcional)

Rodapé em todas as páginas: Nome Completo | Página N
```

## Regras ATS (o que mantém o currículo legível para robôs)
- Uma coluna. Nada de tabelas, caixas de texto, ícones, fotos, gráficos ou cabeçalhos em imagem.
- Títulos de seção padrão (Resumo Profissional, Experiência Profissional, Formação Acadêmica, Certificações).
- Fonte padrão (Helvetica/Arial), PDF com texto selecionável. Tamanho A4, **até 2 páginas**.
- Datas no mesmo formato em todo o documento (Mmm/AAAA – Mmm/AAAA).
- Palavras-chave da vaga escritas como aparecem na vaga (ex.: "Product Discovery", "roadmap", "FinOps").
- Bullets começam com verbo no passado (Liderei, Defini, Estruturei, Reduzi, Aumentei).

## Como adaptar por trilha ou por vaga (sem inventar)
O conteúdo é o mesmo; muda a **ênfase**:
1. **Títulos-alvo:** `curriculo.titulos_alvo[trilha]`.
2. **Resumo:** reescreva o §1 com o vocabulário da trilha (ex.: Produto → discovery, roadmap, backlog; Liderança → equipes, governança, disponibilidade, orçamento). Pode ficar em `curriculo.resumo_por_trilha`.
3. **Ordem dos bullets:** suba os bullets que provam os requisitos da vaga. Ex.: para gestão, os de liderança de equipes e governança primeiro; para produto, visão, discovery e backlog primeiro.
4. **Experiências antigas:** mantenha só os bullets que ajudam a vaga.
5. Escreva os ajustes num `ajustes.json` (campos do bloco `curriculo`) e rode:
   `python3 scripts/gerador_cv.py --trilha "<trilha>" --ajustes ajustes.json`

**Nunca** crie números, cargos, empresas, ferramentas ou certificações que não estejam no perfil. Se faltar algo que a vaga pede, aponte como lacuna para a pessoa.
