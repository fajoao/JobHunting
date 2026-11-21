#!/usr/bin/env python3
"""JobHunting – gera o "Material de crescimento do SSI no LinkedIn" (PDF e DOCX) para a pessoa.

As seções gerais (o que é o SSI, como postar, horários, como comentar, o que curtir, rotina diária,
vagas ocultas por empresa, o que acompanhar) são fixas. O que é da pessoa vem de plano.json,
escrito pela skill jobhunting-plano-ssi a partir do perfil (veja templates/linkedin/plano-ssi.md):

  {
    "inicio": "AAAA-MM-DD",                 # uma segunda-feira (padrão: a próxima)
    "area": "produto, tecnologia e IA",      # usada nos textos gerais
    "hashtags_exemplo": ["#Tag1", "#Tag2"],
    "lideres_exemplo": "Head de Produto, Gerente de Engenharia",
    "comentarios_exemplo": ["comentário 1", "comentário 2"],
    "mensagem_recrutador": "Oi, [Nome]! Vi seu comentário sobre [assunto]. ...",
    "posts": [ {"titulo": "...", "texto": "linha 1\\nlinha 2", "hashtags": "#A #B #C"}, ... 13 itens ]
  }

Uso: python3 scripts/gerador_plano_ssi.py plano.json [--perfil ...] [--saida caminho_sem_extensao]
"""
import datetime, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jobhunting_docs import gerar, perfil_padrao, jobhunting_home  # noqa: E402

DIAS = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
PUBLICA = {1: '08h30 ou 12h30', 3: '08h30 ou 12h30', 5: '10h00'}   # terça, quinta, sábado
HORA_POST = {1: '08h30', 3: '12h30', 5: '10h00'}
ENGAJA = 'Engajamento: comentar 5 a 10 posts, curtir e responder'


def proxima_segunda(hoje=None):
    hoje = hoje or datetime.date.today()
    return hoje + datetime.timedelta(days=(7 - hoje.weekday()) % 7 or 7)


def montar(perfil, plano):
    inicio = datetime.date.fromisoformat(plano['inicio']) if plano.get('inicio') else proxima_segunda()
    if inicio.weekday() != 0:
        inicio = inicio - datetime.timedelta(days=inicio.weekday())
    area = plano.get('area', 'sua área')
    tags = ', '.join(plano.get('hashtags_exemplo', [])) or '#SuaArea, #SeuTema'
    lideres = plano.get('lideres_exemplo', 'Head da área, Gerente, Diretor')
    posts = plano.get('posts', [])

    B = [{'t': 'titulo_doc', 'text': 'Material de Crescimento do SSI no LinkedIn'},
         {'t': 'subtitulo', 'text': f"Plano de 30 dias para {perfil['pessoal'].get('primeiro_nome') or perfil['pessoal']['nome']} manter e aumentar o Social Selling Index"},
         {'t': 'regua'}]

    B += [{'t': 'secao_num', 'text': '1. O que é o SSI'},
          {'t': 'p', 'text': 'O Social Selling Index (SSI) é a pontuação que o LinkedIn calcula para medir o quanto você usa a plataforma de forma profissional e ativa. Ele é dividido em quatro pilares, cada um com peso de até 25 pontos, que somam até 100.'},
          {'t': 'bullets', 'items': [
              '**Estabelecer sua marca profissional:** perfil completo, com título, resumo e experiências atualizados e com palavras-chave.',
              '**Encontrar as pessoas certas:** buscar e conectar-se com recrutadores, decisores e líderes do seu mercado.',
              '**Engajar com insights:** publicar conteúdo relevante e interagir com o conteúdo de outras pessoas.',
              '**Construir relacionamentos:** responder mensagens, aceitar e enviar convites com contexto e manter contato com a sua rede.']},
          {'t': 'p', 'text': 'Os pilares de **engajamento** e de **relacionamentos** são os que mais crescem com uma rotina de publicações e comentários, por isso este plano dá peso a eles. Acompanhe a pontuação na página Social Selling Index do LinkedIn; ela é atualizada com defasagem, então avalie tendências semanais.'}]

    B += [{'t': 'secao_num', 'text': '2. Como postar'},
          {'t': 'bullets', 'items': [
              '**Frequência:** três publicações por semana, nos dias do calendário.',
              '**Primeira linha:** é a que aparece antes do "ver mais". Comece com uma pergunta, um número ou uma afirmação forte.',
              '**Tamanho:** entre 80 e 200 palavras, com quebras de linha a cada duas ou três frases.',
              '**Formato:** texto simples funciona bem. Uma imagem simples, sem dados sensíveis, pode ajudar.',
              '**Links:** evite links externos no corpo do post; coloque no primeiro comentário.',
              f'**Hashtags:** de três a cinco, no final do texto. Exemplos para você: {tags}.',
              '**Responda aos comentários** na primeira hora. Isso aumenta o alcance.']}]

    B += [{'t': 'secao_num', 'text': '3. Qual horário postar'},
          {'t': 'p', 'text': 'Os melhores horários variam para cada perfil. Use esta base e ajuste com as estatísticas das suas publicações.'},
          {'t': 'tabela', 'cabecalho': ['Dia', 'Horário sugerido (Brasília)', 'Por quê'], 'larguras': [0.25, 0.27, 0.48], 'linhas': [
              ['Terça, quarta e quinta', '08h00 a 09h30', 'Início do expediente. Muita gente lê o feed ao chegar.'],
              ['Terça e quinta', '12h00 a 13h00', 'Pausa para almoço. Bom para posts curtos e comentários rápidos.'],
              ['Sábado', '10h00 a 11h00', 'Menos concorrência. Ideal para um texto mais reflexivo.'],
              ['Segunda e sexta', 'Evite posts longos', 'Dias de mais correria. Use para comentar e curtir.']]},
          {'t': 'p', 'text': 'Anote por algumas semanas o horário, as visualizações e os comentários de cada post. Depois de quatro semanas, mantenha o horário que trouxe mais resultados.', 'italic': True}]

    B += [{'t': 'secao_num', 'text': '4. Como comentar'},
          {'t': 'p', 'text': 'Comentar é a forma mais rápida de subir o pilar de engajamento e de se aproximar de recrutadores e líderes. A regra é ser útil, não apenas aparecer.'},
          {'t': 'bullets', 'items': [
              '**Quantas linhas:** de duas a quatro. "Parabéns!" não agrega; textos longos ninguém lê.',
              '**Estrutura:** reconheça o ponto do autor, acrescente uma experiência ou um insight e termine com uma pergunta quando fizer sentido.',
              '**Quantidade:** de cinco a dez comentários qualificados por dia, nos dias de engajamento.',
              '**Momento:** nos primeiros 60 minutos depois da publicação de líderes e recrutadores.',
              '**Evite:** comentários genéricos, autopromoção sem contexto e discordâncias agressivas.']}]
    if plano.get('comentarios_exemplo'):
        B.append({'t': 'subsecao', 'text': 'Exemplos prontos para adaptar:'})
        B += [{'t': 'citacao', 'text': f'"{c}"'} for c in plano['comentarios_exemplo']]

    B += [{'t': 'secao_num', 'text': '5. O que curtir'},
          {'t': 'bullets', 'items': [
              f'**Líderes de {area}**, para se manter visível.',
              '**Recrutadores e profissionais de talent acquisition** das empresas que você quer alcançar.',
              '**Conteúdos que você leu de verdade.** Curtir sem ler não ajuda na relação.',
              '**Comentários de quem respondeu aos seus comentários.** Isso fortalece a conversa.',
              '**Evite curtir em massa.** Dez curtidas bem escolhidas valem mais que cem aleatórias.']}]

    B += [{'t': 'secao_num', 'text': '6. Rotina diária (20 a 25 minutos)'},
          {'t': 'bullets', 'items': [
              '**5 minutos:** responder comentários e mensagens dos seus posts recentes.',
              '**10 minutos:** comentar em cinco a dez publicações relevantes, com duas a quatro linhas cada.',
              '**5 minutos:** curtir conteúdos e conferir novos convites, com foco em recrutadores e líderes.',
              '**5 minutos (opcional):** pesquisar uma empresa-alvo e registrar contatos na planilha.']}]

    B += [{'t': 'secao_num', 'text': '7. Como encontrar vagas ocultas pesquisando uma empresa'},
          {'t': 'p', 'text': 'Vagas ocultas ainda não foram publicadas ou circulam só entre contatos. Pesquisar a empresa e os recrutadores dela é uma das formas mais eficientes de encontrá-las.'},
          {'t': 'subsecao', 'text': 'Passo 1 – Encontre a empresa e seus recrutadores'},
          {'t': 'bullets', 'items': [
              'Busque o nome da empresa, escolha "Empresas" e abra a página.',
              'Clique em "Pessoas" ou busque o nome da empresa com "Talent Acquisition", "Recruiter" ou "Recrutador".',
              'Confira cargo e tempo na empresa. Recrutadores ativos costumam publicar sobre vagas.',
              f'Pesquise também líderes da sua área, como {lideres}.']},
          {'t': 'subsecao', 'text': 'Passo 2 – Aqueça o relacionamento antes de pedir'},
          {'t': 'p', 'text': 'Antes de mandar mensagem, comente duas ou três publicações da pessoa nos últimos dez dias. Assim a mensagem chega com contexto, não como um pedido frio.'},
          {'t': 'subsecao', 'text': 'Passo 3 – Envie uma mensagem curta e específica'}]
    if plano.get('mensagem_recrutador'):
        B.append({'t': 'citacao', 'text': f"\"{plano['mensagem_recrutador']}\""})
    B += [{'t': 'subsecao', 'text': 'Passo 4 – Acompanhe e registre'},
          {'t': 'p', 'text': 'Registre cada contato com nome, empresa, data, canal e próximo passo. Faça o follow-up depois de 7 a 10 dias, sem insistir. Sem resposta, siga com outra empresa do seu radar.'}]

    # calendário
    linhas, destacar, pub = [], [], []
    for i in range(30):
        d = inicio + datetime.timedelta(days=i); wd = d.weekday()
        if wd in PUBLICA:
            linhas.append([str(i + 1), f"{DIAS[wd]} ({d.strftime('%d/%m')})", 'Publicar (texto na seção 9)', PUBLICA[wd]])
            destacar.append(i); pub.append((i + 1, wd, d))
        else:
            linhas.append([str(i + 1), f"{DIAS[wd]} ({d.strftime('%d/%m')})", ENGAJA, '08h00 e 17h00'])
    B += [{'t': 'secao_num', 'text': '8. Calendário de postagem de 30 dias'},
          {'t': 'p', 'text': f"Três publicações por semana (terça, quinta e sábado). Nos outros dias, a tarefa é engajar. O Dia 1 é {inicio.strftime('%d/%m/%Y')}, uma segunda-feira. Os textos da seção 9 foram escritos a partir do seu perfil: revise com as suas palavras antes de publicar."},
          {'t': 'tabela', 'cabecalho': ['Dia', 'Dia da semana', 'Ação', 'Horário'], 'linhas': linhas, 'destacar': destacar, 'larguras': [0.07, 0.22, 0.5, 0.21]},
          {'t': 'p', 'text': 'Linhas com fundo cinza são dias de publicação. As demais são de engajamento.', 'italic': True}]

    B.append({'t': 'secao_num', 'text': '9. Textos das publicações'})
    B.append({'t': 'p', 'text': 'Cada texto tem entre 80 e 150 palavras e pode ser adaptado. Os números usados vêm só do seu currículo.'})
    if len(posts) < len(pub):
        print(f'Aviso: {len(pub)} dias de publicação e {len(posts)} posts; os dias sem texto ficam para você escrever.', file=sys.stderr)
    for (dia, wd, d), post in zip(pub, posts):
        B.append({'t': 'subsecao', 'text': f"Dia {dia} · {DIAS[wd]} · {HORA_POST[wd]} — {post['titulo']}"})
        for linha in post['texto'].split('\n'):
            if linha.strip(): B.append({'t': 'citacao', 'text': linha.strip()})
        if post.get('hashtags'): B.append({'t': 'citacao', 'text': post['hashtags']})

    B += [{'t': 'secao_num', 'text': '10. O que acompanhar'},
          {'t': 'bullets', 'items': [
              '**SSI semanal:** anote a pontuação de cada pilar uma vez por semana.',
              '**Visualizações e comentários** de cada post, para descobrir os melhores temas e horários.',
              '**Convites aceitos e mensagens recebidas**, principalmente de recrutadores.',
              '**Empresas e contatos registrados** na planilha de vagas ocultas, com o status de cada um.']},
          {'t': 'p', 'text': 'Ajuste o plano a cada quatro semanas: mantenha os temas que geraram conversa e troque os que tiveram pouca resposta.'}]
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
        plano = json.load(f)
    padrao = os.path.join(jobhunting_home(), 'linkedin', 'Plano_Crescimento_SSI_LinkedIn')
    for s in gerar(montar(perfil, plano), os.path.splitext(opt('--saida', padrao))[0], rodape=perfil['pessoal']['nome']):
        print(s)


if __name__ == '__main__':
    main()
