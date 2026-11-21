# Segurança do JobHunting

## Modelo de ameaças e proteções

| Risco | Proteção |
|---|---|
| Dados pessoais vazarem para o GitHub | O perfil, os contatos e os documentos gerados ficam em `~/.jobhunting/`, fora do repositório. O `.gitignore` bloqueia `profile.json`, `*.pdf`, `*.docx`, `.env` e `data/`. `scripts/checar_seguranca.py` procura CPF, telefones, e-mails, tokens e chaves antes de cada publicação. |
| Outros usuários do computador lerem os dados | `~/.jobhunting/` é criada com permissão 700, e o perfil e os documentos com 600. |
| Coleta de dados sensíveis | O cadastro nunca pede CPF, RG, dados bancários ou senhas. Autoidentificação é opcional e nunca vai para o dashboard nem para o texto das rotinas. |
| Dashboard com dados demais | Só vagas, notas, nome e currículos enviados como asset ficam no dashboard. A cópia do perfil para as rotinas fica em `data/users/<você>`, que só a sua conta lê. |
| Link malicioso de uma fonte de vagas (XSS) | O app só aceita links `https:`, `http:` e `/_blob/`. Links `javascript:`, `data:` e outros são descartados. O React escapa todo o texto, e o app não usa `innerHTML`. |
| Texto injetado em PDF ou DOCX | O renderizador escapa `&`, `<` e `>` antes de montar os parágrafos do PDF. |
| Prompt injection (texto de vaga, site, e-mail ou perfil tentando dar ordens à IA) | Agentes, skills e rotinas tratam esse conteúdo como dado, nunca como instrução, e registram quando encontram algo suspeito. |
| Ações externas indevidas | Candidatura automática vem desligada. Envio de mensagens no LinkedIn só com pedido explícito, em lotes pequenos, conferindo o histórico para nunca repetir. Os agentes confirmam antes de publicar, enviar, excluir ou criar rotinas. |
| Contornar proteções de sites | É proibido contornar CAPTCHA, criar contas ou burlar bloqueios. O coletor usa só APIs públicas de vagas. |
| Execução de código | Os scripts não usam `eval`, `exec`, `pickle`, `os.system` nem `shell=True`. As URLs do coletor sempre começam com `https://`. |
| Segredos no repositório | Não há tokens nem chaves no código. As rotinas usam os conectores da conta do Claude, e nenhuma credencial é gravada em arquivo. |

## Antes de publicar uma mudança
```bash
python3 -I scripts/checar_seguranca.py
cd app && npm audit --omit=dev
```

## Reportar um problema
Abra uma issue **sem incluir dados pessoais**. Se o problema expuser dados de alguém, descreva só o tipo de dado e onde ele aparece, e peça um contato privado ao mantenedor.
