# Privacidade e LGPD no JobHunting

## Princípios
1. **Mínimo necessário:** o perfil guarda só o que é preciso para buscar vagas, montar currículo e preencher formulários. CPF, RG, dados bancários e senhas **nunca** são pedidos nem guardados.
2. **Local por padrão:** os dados ficam em `~/.jobhunting/` (permissão 600), fora do repositório e da pasta do plugin.
3. **Consentimento explícito:** candidatura automática e envio de mensagens vêm desligados. Só são ligados quando o usuário pede.
4. **Dados sensíveis opcionais:** autoidentificação (gênero, raça/cor, PcD, orientação sexual) só é usada para responder perguntas de formulários e para incluir vagas afirmativas que o usuário escolher. Nunca aparece no dashboard nem no texto das rotinas.

## Onde cada dado aparece
| Dado | Perfil local | Dashboard (quem tem o link vê) | Rotinas de nuvem |
|---|---|---|---|
| Nome | sim | sim, no topo do painel | lido do perfil privado |
| E-mail, telefone, LinkedIn | sim | não | lido do perfil privado |
| Remuneração e pretensão | sim | **não** | lido do perfil privado, só para formulários |
| Autoidentificação | opcional | **não** | lido do perfil privado, só para formulários |
| Vagas, notas e currículos gerados | sim | sim | sim |
| Contatos com recrutadores | sim | não | não |

O "perfil privado" das rotinas de nuvem é o documento `data/users/<você>/perfil` do dashboard, que só a sua conta consegue ler.

## Terceiros
- O registro de contatos com recrutadores tem dados de outras pessoas (nome, empresa). Ele fica só no seu computador e **não deve** ser publicado.
- Ao publicar o dashboard, lembre que os currículos enviados como asset ficam acessíveis a quem tiver o link.

## Apagar tudo
Apague a pasta `~/.jobhunting/`, o Artifact do dashboard e as rotinas criadas (claude.ai/code/routines e "Scheduled" no app Claude).
