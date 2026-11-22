#!/usr/bin/env python3
"""JobHunting – gera o currículo no modelo ATS (PDF e DOCX) a partir do perfil.

Modelo (veja templates/curriculo/modelo-ats.md):
  NOME
  TÍTULOS-ALVO SEPARADOS POR |
  Cidade – UF | telefone | e-mail | linkedin
  ───────────────
  RESUMO PROFISSIONAL       2 parágrafos + "Resultado de destaque:" (com "idioma": "en" nos ajustes, títulos em inglês)
  EXPERIÊNCIA PROFISSIONAL  EMPRESA | Cidade – UF / Cargo | Área | Período / escopo / bullets
  FORMAÇÃO ACADÊMICA        Curso – Grau | Instituição | Período
  FORMAÇÃO COMPLEMENTAR     itens separados por ;
  CERTIFICAÇÕES             Grupo: itens
  IDIOMAS                   (opcional)
  Rodapé: Nome | Página N

Uso:
  python3 scripts/gerador_cv.py [--trilha "Product Manager"] [--ajustes ajustes.json]
                                [--perfil ~/.jobhunting/profile.json] [--saida ~/.jobhunting/curriculos/Nome_CV]
                                [--formatos pdf,docx]

--trilha escolhe os títulos-alvo (curriculo.titulos_alvo[trilha]) e, se houver, o resumo da trilha.
--ajustes: JSON com campos do bloco "curriculo" a sobrescrever para uma vaga. A skill
jobhunting-curriculo usa isso para reordenar e reescrever, sem inventar fatos.
Requer: pip install reportlab python-docx
"""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jobhunting_docs import gerar, perfil_padrao, jobhunting_home, slug, contato  # noqa: E402


ROTULOS = {
    'pt': {'resumo': 'Resumo Profissional', 'destaque': 'Resultado de destaque', 'experiencia': 'Experiência Profissional',
           'formacao': 'Formação Acadêmica', 'complementar': 'Formação Complementar', 'certificacoes': 'Certificações Profissionais',
           'idiomas': 'Idiomas', 'pagina': 'Página'},
    'en': {'resumo': 'Professional Summary', 'destaque': 'Key achievement', 'experiencia': 'Professional Experience',
           'formacao': 'Education', 'complementar': 'Additional Education', 'certificacoes': 'Certifications',
           'idiomas': 'Languages', 'pagina': 'Page'},
}


def montar(perfil, cv, trilha=None):
    R = ROTULOS.get((cv.get('idioma') or 'pt').lower()[:2], ROTULOS['pt'])
    p = perfil['pessoal']
    titulos = cv.get('titulos') or (cv.get('titulos_alvo') or {}).get(trilha or '', '') \
        or next(iter((cv.get('titulos_alvo') or {}).values()), '')
    resumo = cv.get('resumo_por_trilha', {}).get(trilha or '') or cv.get('resumo', [])
    if isinstance(resumo, str): resumo = [resumo]

    B = [{'t': 'nome', 'text': p['nome']}]
    if titulos: B.append({'t': 'titulos', 'text': titulos})
    linha_contato = contato(p)
    if R is ROTULOS['en']:
        local = ', '.join(x for x in (p.get('cidade'), p.get('uf'), 'Brazil') if x)
        fone = p.get('telefone', '')
        if fone and not fone.startswith('+'):
            fone = '+55 ' + fone.replace('(', '').replace(')', '')
        linha_contato = ' | '.join(x for x in (local, fone, p.get('email'), p.get('linkedin')) if x)
    B += [{'t': 'contato', 'text': linha_contato}, {'t': 'regua'}]

    B.append({'t': 'secao', 'text': R['resumo']})
    B += [{'t': 'p', 'text': x} for x in resumo]
    if cv.get('resultado_destaque'):
        B.append({'t': 'p', 'text': f"**{R['destaque']}:** {cv['resultado_destaque']}"})

    if cv.get('experiencias'):
        B.append({'t': 'secao', 'text': R['experiencia']})
        for e in cv['experiencias']:
            B.append({'t': 'empresa', 'text': ' | '.join(x for x in ((e.get('empresa') or '').upper(), e.get('cidade')) if x)})
            B.append({'t': 'cargo', 'text': ' | '.join(x for x in (e.get('cargo'), e.get('area'), e.get('periodo')) if x)})
            if e.get('escopo'): B.append({'t': 'p', 'text': e['escopo']})
            if e.get('bullets'): B.append({'t': 'bullets', 'items': e['bullets']})

    if cv.get('formacao'):
        B.append({'t': 'secao', 'text': R['formacao']})
        for f in cv['formacao']:
            curso = ' – '.join(x for x in (f.get('curso'), f.get('grau')) if x)
            resto = ' | '.join(x for x in (f.get('instituicao'), f.get('periodo')) if x)
            B.append({'t': 'p', 'text': f'**{curso}**' + (f' | {resto}' if resto else ''), 'justify': False})

    fc = cv.get('formacao_complementar')
    if fc and fc.get('itens'):
        B.append({'t': 'secao', 'text': fc.get('titulo') or R['complementar']})
        B.append({'t': 'p', 'text': '; '.join(fc['itens']) + '.'})

    if cv.get('certificacoes'):
        B.append({'t': 'secao', 'text': R['certificacoes']})
        for g in cv['certificacoes']:
            B.append({'t': 'p', 'text': f"**{g['grupo']}:** " + '; '.join(g['itens']) + '.'})

    if cv.get('idiomas'):
        B.append({'t': 'secao', 'text': R['idiomas']})
        B.append({'t': 'p', 'text': cv['idiomas']})
    return B


def main():
    a = sys.argv[1:]
    def opt(nome, padrao=None):
        return a[a.index(nome) + 1] if nome in a else padrao
    with open(opt('--perfil', perfil_padrao()), encoding='utf-8') as f:
        perfil = json.load(f)
    cv = dict(perfil['curriculo'])
    if opt('--ajustes'):
        with open(opt('--ajustes'), encoding='utf-8') as f:
            cv.update(json.load(f))
    trilha = opt('--trilha')
    nome = perfil['pessoal']['nome']
    padrao = os.path.join(jobhunting_home(), 'curriculos', f"{slug(nome)}_CV" + (f"_{slug(trilha)}" if trilha else ''))
    base = os.path.splitext(opt('--saida', padrao))[0]
    formatos = tuple(opt('--formatos', 'pdf,docx').split(','))
    R = ROTULOS.get((cv.get('idioma') or 'pt').lower()[:2], ROTULOS['pt'])
    for s in gerar(montar(perfil, cv, trilha), base, rodape=nome, formatos=formatos, pagina=R['pagina']):
        print(s)


if __name__ == '__main__':
    main()
