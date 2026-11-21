#!/usr/bin/env python3
"""JobHunting – gera a carta de apresentação (PDF e DOCX) no modelo do JobHunting.

Modelo (veja templates/carta/modelo-carta.md):
  Cabeçalho igual ao do currículo (nome, títulos-alvo, contato, linha)
  Cidade – UF, DD de mês de AAAA
  Prezado(a) [Nome],
  §1 interesse na vaga + quem é + anos + domínios + cargo/empresa atual e foco
  §2 trajetória (onde começou → como evoluiu → hoje) e o que essa combinação permite
  §3 resultado de que mais se orgulha (com número) + como chegou lá + outras entregas
  §4 como pode contribuir com a empresa no desafio da vaga + disponibilidade + agradecimento
  Atenciosamente, / Nome / contato

Uso:
  python3 scripts/gerador_carta.py carta.json [--perfil ~/.jobhunting/profile.json] [--saida caminho_sem_extensao]

carta.json:
  {"empresa": "...", "cargo": "...", "recrutador": "Nome (opcional)", "trilha": "Product Manager (opcional)",
   "paragrafos": ["§1", "§2", "§3", "§4"], "data": "AAAA-MM-DD (opcional)"}
Os parágrafos são escritos pela skill jobhunting-carta a partir do perfil, sem inventar fatos.
"""
import datetime, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jobhunting_docs import gerar, perfil_padrao, jobhunting_home, slug, contato, data_extenso  # noqa: E402


def montar(perfil, carta):
    p = perfil['pessoal']; cv = perfil.get('curriculo', {})
    titulos = carta.get('titulos') or (cv.get('titulos_alvo') or {}).get(carta.get('trilha', ''), '') \
        or next(iter((cv.get('titulos_alvo') or {}).values()), '')
    data = datetime.date.fromisoformat(carta['data']) if carta.get('data') else datetime.date.today()
    local = ' – '.join(x for x in (p.get('cidade'), p.get('uf')) if x)
    if len(carta.get('paragrafos', [])) != 4:
        sys.exit('A carta precisa de exatamente 4 parágrafos (interesse, trajetória, resultado, contribuição).')

    B = [{'t': 'nome', 'text': p['nome']}]
    if titulos: B.append({'t': 'titulos', 'text': titulos})
    B += [{'t': 'contato', 'text': contato(p)}, {'t': 'regua'}]
    B.append({'t': 'p', 'text': f'{local}, {data_extenso(data)}' if local else data_extenso(data), 'justify': False, 'after': 8})
    B.append({'t': 'p', 'text': f"Prezado(a) {carta.get('recrutador') or '[Nome do recrutador]'},", 'justify': False, 'after': 8})
    B += [{'t': 'p', 'text': x, 'after': 8} for x in carta['paragrafos']]
    B += [{'t': 'espaco', 'altura': 4}, {'t': 'p', 'text': 'Atenciosamente,', 'justify': False},
          {'t': 'espaco', 'altura': 6}, {'t': 'p', 'text': f"**{p['nome']}**", 'justify': False},
          {'t': 'p', 'text': ' | '.join(x for x in (p.get('telefone'), p.get('email'), p.get('linkedin')) if x), 'italic': True, 'justify': False}]
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
        carta = json.load(f)
    nome = perfil['pessoal']['nome']
    padrao = os.path.join(jobhunting_home(), 'cartas', f"Carta_{slug(carta.get('empresa', ''))}_{slug(carta.get('cargo', ''))}")
    for s in gerar(montar(perfil, carta), os.path.splitext(opt('--saida', padrao))[0], rodape=nome):
        print(s)


if __name__ == '__main__':
    main()
