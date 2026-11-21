# Mensagens para recrutadores e como achar vagas ocultas

Os campos entre `{{ }}` vêm do seu perfil (`~/.jobhunting/profile.json`, blocos `mensagens` e `pessoal`).
Os campos entre `[ ]` são preenchidos para cada pessoa ou vaga. Mensagens curtas e específicas recebem mais respostas.

## Parte 1 – Os 4 textos

### Texto 1 – Pedido de conexão (até 300 caracteres)
> Olá, [Nome]! Acompanho o trabalho [da/do] [Empresa] com produtos de IA e automação. Sou {{foco_cargo}} e gostaria de me conectar para trocar ideias sobre oportunidades na área. Abraço, {{assinatura}}

Use "do" ou "da" conforme a empresa (do Nubank, da Amazon).

### Texto 2 – Depois que a conexão é aceita: pergunta sobre vagas não divulgadas
> Oi, [Nome], obrigado por aceitar o convite. Atuo com {{foco}} e, em um dos projetos que liderei, {{conquista_principal}}. Estou buscando meu próximo desafio nessa área. Você conhece alguma equipe que esteja estruturando produtos de IA ou que pretenda contratar nesse perfil, mesmo que a vaga ainda não esteja publicada? Agradeço muito qualquer direcionamento.

### Texto 3 – Depois de se candidatar a uma vaga
> Olá, [Nome]! Acabei de me candidatar à vaga de [cargo] [na/no] [Empresa] e gostaria de reforçar meu interesse. Tenho experiência em [2 ou 3 competências do seu perfil ligadas à vaga]. Se fizer sentido, fico à disposição para uma conversa rápida. Obrigado pela atenção!

### Texto 4 – Follow-up depois de silêncio (7 a 10 dias)
> Oi, [Nome], tudo bem? Passo para retomar nosso contato sobre a vaga de [cargo]. Continuo muito interessado e disponível para conversar nesta semana. Se a vaga já tiver sido preenchida, eu agradeço se puder me indicar outras oportunidades em [sua área]. Obrigado!

### Versões em inglês (para recrutadores que não falam português)
- **Texto 1:** Hi, [Name]! I follow [Company]'s work on AI and automation products. I'm a {{foco_cargo_en}} and would love to connect and exchange ideas about opportunities in the area. Best, {{assinatura}}
- **Texto 2:** Hi, [Name], thanks for accepting my invitation. I work in {{foco_en}}, and in one of the projects I led, {{conquista_principal_en}}. I'm looking for my next challenge in this area. Do you know of any team building AI products or planning to hire for this profile, even if the role isn't posted yet? I'd really appreciate any direction.

## Parte 2 – Como achar vagas ocultas

1. **Busca booleana em vagas.** Exemplo para o LinkedIn:
   `("Product Manager" OR "Technical Product Manager" OR "IT Manager" OR "Tech Manager" OR "Gerente de Produto") AND (IA OR AI OR AIOps OR "inteligência artificial")`
   A skill `jobhunting-linkedin` monta essa busca a partir das suas trilhas.
2. **Pessoas dentro da empresa-alvo.** Na página da empresa, vá em "Pessoas" e filtre por "Head de Produto", "Gerente de Engenharia" ou "Recrutador". Líderes costumam contratar antes de abrir a vaga.
3. **Alertas de vaga com palavras amplas**, com frequência diária.
4. **Posts de contratação**: "estamos contratando", "we are hiring", "#hiring" junto com sua área. Comente de forma útil e depois mande mensagem ao autor.
5. **Siga empresas-alvo e interaja com líderes.**
6. **Use a sua rede**: conte a ex-colegas e comunidades o tipo de posição que você procura.
7. **Headhunters e consultorias** de recrutamento em tecnologia.
8. **Dores explícitas nas empresas**: notícias e posts de executivos sobre projetos de IA ou modernização.

**Dica final:** registre cada contato em `~/.jobhunting/contatos.csv` (nome, empresa, data, canal, status, próximo passo). A skill `jobhunting-linkedin` faz isso por você.

## Limites (importante)
- O LinkedIn proíbe automação de convites e mensagens. Se você usar o Claude para enviar, faça em lotes pequenos (15 a 20 por dia), sempre revisando, e entenda que o risco de restrição da conta é seu.
- Nunca mande a mesma mensagem duas vezes para a mesma pessoa: confira o registro e o histórico da conversa antes.
