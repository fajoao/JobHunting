#!/usr/bin/env python3
"""JobHunting – gera o guia "Textos para recrutadores e vagas ocultas" (PDF e DOCX) para a pessoa.

A estrutura (4 textos + 8 formas de achar vagas ocultas + dica final) é fixa. Os textos e exemplos
vêm de guia.json, escrito pela skill jobhunting-abordagem-recrutadores a partir do perfil
(veja templates/linkedin/abordagem-recrutadores.md):

  {
    "textos": {"t1": "...", "t2": "...", "t3": "...", "t4": "..."},     # com [Nome], [Empresa], [cargo]
    "textos_en": {"t1": "...", "t2": "..."},                            # opcional
    "busca_booleana": "(\\"Cargo A\\" OR \\"Cargo B\\") AND (tema1 OR tema2)",
    "termos_alerta": ["termo 1", "termo 2", "termo 3"],
    "cargos_lideres": "Head de X, Gerente de Y",
    "exemplo_comentario_post": "...",
    "exemplo_mensagem_rede": "...",
    "exemplo_mensagem_dor": "..."
  }

Uso: python3 scripts/gerador_guia_recrutadores.py guia.json [--perfil ...] [--saida caminho_sem_extensao]
"""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jobhunting_docs import gerar, perfil_padrao, jobhunting_home  # noqa: E402


def montar(perfil, g):
    t = g['textos']
    B = [{'t': 'titulo_doc', 'text': '4 textos para abordar recrutadores no LinkedIn'},
         {'t': 'subtitulo', 'text': 'E como achar vagas ocultas'},
         {'t': 'regua'},
         {'t': 'p', 'text': 'Substitua os trechos entre colchetes antes de enviar. Mensagens curtas e específicas recebem mais respostas do que mensagens genéricas.', 'italic': True},
         {'t': 'secao_num', 'text': 'Parte 1 – Os 4 textos'}]
    for chave, titulo in (('t1', 'Texto 1 – Pedido de conexão (até 300 caracteres)'),
                          ('t2', 'Texto 2 – Depois que a conexão for aceita: pergunta sobre vagas não divulgadas'),
                          ('t3', 'Texto 3 – Depois de se candidatar a uma vaga'),
                          ('t4', 'Texto 4 – Follow-up depois de silêncio (7 a 10 dias)')):
        B += [{'t': 'subsecao', 'text': titulo}, {'t': 'citacao', 'text': f'"{t[chave]}"'}]
    if g.get('textos_en'):
        B.append({'t': 'subsecao', 'text': 'Versões em inglês (para recrutadores que não falam português)'})
        for chave, v in g['textos_en'].items():
            B.append({'t': 'citacao', 'text': f'**{chave.upper()}:** "{v}"'})

    termos = ', '.join(f'"{x}"' for x in g.get('termos_alerta', []))
    B += [{'t': 'secao_num', 'text': 'Parte 2 – Como achar vagas ocultas'},
          {'t': 'p', 'text': 'Vagas ocultas são as que não aparecem publicadas ou só circulam dentro de redes de contatos. Formas práticas de encontrá-las:'},
          {'t': 'subsecao', 'text': '1. Busca booleana em vagas e pessoas'},
          {'t': 'p', 'text': 'Use operadores para refinar a pesquisa. A sua busca, montada a partir dos seus cargos-alvo:'},
          {'t': 'citacao', 'text': g.get('busca_booleana', '')},
          {'t': 'p', 'text': 'Filtre também por "Pessoas", não só por "Vagas": a equipe real pode aparecer na busca de pessoas. No LinkedIn, a busca de pessoas funciona melhor com expressões curtas e sem acentos.'},
          {'t': 'subsecao', 'text': '2. Pesquise pessoas dentro da empresa-alvo'},
          {'t': 'p', 'text': f"Na página da empresa, vá em \"Pessoas\" e filtre por cargo, como {g.get('cargos_lideres', 'líderes da sua área')} ou \"Recrutador\". Líderes costumam contratar antes de abrir a vaga. Exemplo: procure \"Recruiter [área] [Empresa]\" e, depois que a pessoa aceitar o convite, envie o Texto 2."},
          {'t': 'subsecao', 'text': '3. Ative alertas de vagas com palavras-chave amplas'},
          {'t': 'p', 'text': f"Crie alertas com termos como {termos or 'os seus cargos-alvo'} e marque a frequência como diária. Assim você recebe a vaga assim que for publicada."},
          {'t': 'subsecao', 'text': '4. Monitore posts de contratação'},
          {'t': 'p', 'text': 'Pesquise posts com "estamos contratando", "we are hiring" ou "#hiring" junto com a sua área. Comente de forma útil, mencionando sua experiência, e depois mande mensagem ao autor.'}]
    if g.get('exemplo_comentario_post'):
        B.append({'t': 'citacao', 'text': f"Exemplo de comentário: \"{g['exemplo_comentario_post']}\""})
    B += [{'t': 'subsecao', 'text': '5. Siga as empresas-alvo e interaja com líderes'},
          {'t': 'p', 'text': 'Ative as notificações de posts das empresas e de líderes que você admira. Comentários frequentes e relevantes fazem o recrutador ou gestor lembrar do seu nome quando surgir uma oportunidade.'},
          {'t': 'subsecao', 'text': '6. Use a rede de contatos de forma ativa'},
          {'t': 'p', 'text': 'Conte a ex-colegas, gestores e comunidades que você está buscando uma oportunidade específica. Indicações são uma das principais fontes de vagas ocultas.'}]
    if g.get('exemplo_mensagem_rede'):
        B.append({'t': 'citacao', 'text': f"Exemplo: \"{g['exemplo_mensagem_rede']}\""})
    B += [{'t': 'subsecao', 'text': '7. Fale com headhunters e consultorias de recrutamento'},
          {'t': 'p', 'text': 'Consultorias especializadas costumam ter vagas ainda não divulgadas. Envie seu currículo e explique a posição que procura, com senioridade e setor. Pergunte também quais empresas estão contratando agora.'},
          {'t': 'subsecao', 'text': '8. Procure por dores explícitas nas empresas'},
          {'t': 'p', 'text': 'Leia notícias, balanços e posts de executivos. Se uma empresa anunciou um projeto na sua área, ela provavelmente vai precisar de gente para executá-lo. Mande uma mensagem mostrando como você resolveu um problema parecido.'}]
    if g.get('exemplo_mensagem_dor'):
        B.append({'t': 'citacao', 'text': f"Exemplo: \"{g['exemplo_mensagem_dor']}\""})
    B += [{'t': 'secao_num', 'text': 'Dica final'},
          {'t': 'p', 'text': 'Registre cada contato numa planilha simples com nome, empresa, data, canal e próximo passo. Acompanhar o funil ajuda a manter o ritmo e a fazer follow-ups no momento certo. O JobHunting mantém esse registro em ~/.jobhunting/contatos.csv.'},
          {'t': 'secao_num', 'text': 'Limites'},
          {'t': 'bullets', 'items': [
              'O LinkedIn proíbe automação de convites e mensagens. Envie você mesmo, em lotes pequenos.',
              'Nunca mande a mesma mensagem duas vezes para a mesma pessoa: confira o registro e a conversa antes.']}]
    return B


def main():
    a = sys.argv[1:]
    if not a or a[0].startswith('--'):
        sys.exit(__doc__)
    def opt(nome, padrao=None):
        return a[a.index(nome) + 1] if nome in a else padrao
    with open(opt('--perfil', perfil_padrao()), encoding='utf-8') as f:
        perfil = json.load(f)
    with open(a[0], encoding='utf-8') as f:
        guia = json.load(f)
    padrao = os.path.join(jobhunting_home(), 'linkedin', 'Textos_Recrutadores_e_Vagas_Ocultas')
    for s in gerar(montar(perfil, guia), os.path.splitext(opt('--saida', padrao))[0], rodape=perfil['pessoal']['nome']):
        print(s)


if __name__ == '__main__':
    main()
