# Modelo de carta de apresentação do JobHunting

O gerador `scripts/gerador_carta.py` monta o PDF e o DOCX. A skill `jobhunting-carta` escreve os 4 parágrafos a partir do perfil e da vaga. Abaixo, a estrutura. O conteúdo vem sempre da pessoa.

## Esqueleto

```
[Cabeçalho igual ao do currículo: NOME / TÍTULOS-ALVO / contato / linha]

Cidade – UF, DD de mês de AAAA

Prezado(a) [Nome do recrutador],            (use o nome real quando souber)

§1 INTERESSE E QUEM É (3 a 4 frases)
   "Escrevo para manifestar meu interesse na vaga de [cargo] na/no [Empresa]."
   + identidade profissional + "mais de N anos de experiência em" + domínios.
   + cargo e empresa atual (ou mais recente) e o foco do trabalho.

§2 TRAJETÓRIA (3 a 4 frases)
   Onde começou → como evoluiu (1 ou 2 marcos com empresa e cargo) → o que faz hoje.
   Fecha com o que essa combinação permite (ex.: "dialogar com negócio e engenharia na
   mesma linguagem" ou "decidir com clareza sobre riscos, custos e prioridades").

§3 RESULTADO DE QUE MAIS SE ORGULHA (3 a 4 frases)
   "Um dos resultados de que mais me orgulho é..." + número (de A para B, em N meses).
   + como chegou lá (2 ou 3 ações concretas) + outras entregas relevantes.

§4 CONTRIBUIÇÃO E FECHAMENTO (2 a 3 frases)
   "Acredito que posso contribuir com a/o [Empresa], especialmente nos desafios de
   [desafio tirado da descrição da vaga], combinando [2 ou 3 forças]."
   "Fico à disposição para uma conversa e agradeço desde já a atenção."

Atenciosamente,

Nome Completo
telefone | e-mail | linkedin
```

## Regras
- Uma página, de 250 a 400 palavras.
- Adapte à trilha: para Produto, destaque visão, discovery, roadmap e métricas; para Liderança, equipes, governança, riscos, custos e entrega.
- O §4 precisa citar algo **específico da vaga** (um desafio, produto ou área da descrição). Se não houver vaga, deixe `[desafio ou área específica da vaga]` para a pessoa completar.
- Use o artigo certo para a empresa (na Amazon, no Nubank).
- Só fatos do perfil. Nada de números ou experiências que a pessoa não informou.

## Entrada do gerador (carta.json)
```json
{"empresa": "Empresa", "cargo": "Cargo", "recrutador": "Nome ou vazio", "trilha": "Product Manager",
 "paragrafos": ["§1", "§2", "§3", "§4"]}
```
