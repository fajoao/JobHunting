# Modelo do guia de abordagem a recrutadores e vagas ocultas

O gerador `scripts/gerador_guia_recrutadores.py` monta o guia (PDF e DOCX):
- **parte fixa:** a estrutura (4 textos e 8 formas de achar vagas ocultas), a dica final e os limites;
- **parte da pessoa:** a skill `jobhunting-abordagem-recrutadores` escreve o `guia.json` a partir do perfil.

| Campo | Como escrever |
|---|---|
| `textos.t1` | **Convite**, até 300 caracteres: "Olá, [Nome]! Acompanho o trabalho [da/do] [Empresa] com {tema da área}. Sou {foco_cargo} e gostaria de me conectar para trocar ideias sobre oportunidades na área. Abraço, {assinatura}" |
| `textos.t2` | **Depois que a conexão for aceita**: agradece + "Atuo com {foco} e, em um dos projetos que liderei, {conquista_principal}." + está buscando o próximo desafio + pergunta se conhece equipe contratando, mesmo sem vaga publicada + agradece |
| `textos.t3` | **Depois de se candidatar**: "Acabei de me candidatar à vaga de [cargo] [na/no] [Empresa]..." + 2 ou 3 competências reais do perfil ligadas à trilha + disponibilidade para conversa |
| `textos.t4` | **Follow-up de 7 a 10 dias**: retoma o contato sobre [cargo], reforça interesse e disponibilidade, pede indicação de outras oportunidades em {área} se a vaga já tiver sido preenchida |
| `textos_en` | Versões em inglês de t1 e t2, se a pessoa quiser falar com recrutadores de fora |
| `busca_booleana` | `("Título 1" OR "Título 2" OR ...) AND (tema1 OR tema2 OR "tema 3")`, a partir das trilhas e palavras-chave do perfil |
| `termos_alerta` | 3 a 5 termos amplos para alertas diários de vaga |
| `cargos_lideres` | Quem contrata na área (ex.: "Head de Produto", "Gerente de Engenharia") |
| `exemplo_comentario_post` | Comentário em post de contratação citando uma experiência real da pessoa |
| `exemplo_mensagem_rede` | "Estou buscando uma posição de {cargo} em {área}. Você conhece alguma empresa que esteja nesse momento de expansão?" |
| `exemplo_mensagem_dor` | "Vi o anúncio sobre [iniciativa] [na/no] [Empresa]. {algo parecido que a pessoa já resolveu}. Posso compartilhar como fizemos?" |

## Regras
- Use só fatos do perfil. Os trechos entre colchetes ficam para a pessoa preencher em cada envio.
- Mensagens curtas e específicas: o Texto 1 tem no máximo 300 caracteres, e os demais até cerca de 600.
