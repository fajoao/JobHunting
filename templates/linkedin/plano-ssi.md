# Modelo do plano de crescimento do SSI no LinkedIn

O gerador `scripts/gerador_plano_ssi.py` monta o material (PDF e DOCX) com:
- as seções gerais, que são fixas: o que é o SSI, como e quando postar, como comentar, o que curtir, rotina diária, vagas ocultas por empresa e o que acompanhar;
- o calendário de 30 dias, calculado a partir da data de início (terça, quinta e sábado são dias de publicação).

A skill `jobhunting-plano-ssi` escreve o `plano.json` **com base no perfil da pessoa**:

| Campo | O que é |
|---|---|
| `inicio` | Data do Dia 1 (uma segunda-feira) |
| `area` | Área da pessoa, em poucas palavras (ex.: "produto, tecnologia e IA") |
| `hashtags_exemplo` | 4 a 6 hashtags da área dela |
| `lideres_exemplo` | Cargos de líderes que contratam na área dela |
| `comentarios_exemplo` | 2 comentários de 2 a 4 linhas: reconhece o ponto do autor + experiência real da pessoa + pergunta |
| `mensagem_recrutador` | "Oi, [Nome]! Vi seu comentário sobre [assunto]. Sou {foco_cargo} e {conquista_principal}. Estou buscando oportunidades nessa área. Você conhece alguma equipe da [Empresa] que...?" |
| `posts` | **13 posts**, na ordem dos dias de publicação |

## Os 13 posts (arquétipos)
Cada post tem 80 a 150 palavras, quebras de linha a cada 1 ou 2 frases, primeira linha forte, uma pergunta no fim e 3 a 5 hashtags. **Os números vêm só do currículo da pessoa.**

| # | Dia | Arquétipo | O que usar do perfil |
|---|---|---|---|
| 1 | Terça | Minha trajetória | `curriculo.trajetoria`, anos de experiência, o fio condutor da carreira |
| 2 | Quinta | Resultado com dados | `resultado_destaque`: o que fez diferença, além da ferramenta |
| 3 | Sábado | Pergunta para engajar | Uma métrica ou dor comum da área que quase ninguém mede |
| 4 | Terça | Método antes da solução | O método/processo principal da área (ex.: discovery, diagnóstico) em 3 perguntas |
| 5 | Quinta | Trade-offs da área | Tensões clássicas do trabalho dela e como decide |
| 6 | Sábado | Boa prática vista como burocracia | Uma prática que ela defende, com contexto real |
| 7 | Terça | Conceito explicado | Um conceito central da área em linguagem simples + uma entrega dela |
| 8 | Quinta | Como medir qualidade | Como ela mede se algo funcionou (métricas, critérios) |
| 9 | Sábado | Pessoas e liderança | Um programa, time ou iniciativa de pessoas que ela conduziu |
| 10 | Terça | Lição de risco ou prevenção | Algo que só funciona se testado ou revisado de verdade |
| 11 | Quinta | O que levei de uma área para outra | 3 aprendizados da transição de carreira |
| 12 | Sábado | Estrutura e governança | Como ela organizou demanda, prioridade ou portfólio |
| 13 | Terça | Balanço do mês | A lição que repete + convite para trocar ideias |

Se a pessoa não tiver material para um arquétipo (ex.: nunca liderou pessoas), troque por outro tema real dela e avise.
