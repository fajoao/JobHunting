#!/usr/bin/env python3
"""JobHunting – gera currículo DOCX (e PDF, se o LibreOffice estiver instalado) a partir do perfil.

Uso:
    python3 scripts/gerador_cv.py [--perfil ~/.jobhunting/profile.json] [--ajustes ajustes.json] [--saida ~/.jobhunting/curriculos/cv.docx] [--a4]

--ajustes: JSON opcional com campos do bloco "curriculo" a sobrescrever para uma vaga específica
(ex.: headline, resumo, competencias). É assim que a skill jobhunting-curriculo personaliza o CV
sem nunca inventar fatos: ela só reordena e reescreve o que já está no perfil.

Requer: pip install python-docx. PDF: soffice --headless --convert-to pdf.
"""
import json, os, subprocess, sys

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def jobhunting_home():
    """Pasta dos dados do usuário: $JOBHUNTING_HOME ou ~/.jobhunting (fora do repositório e do plugin)."""
    return os.path.expanduser(os.environ.get('JOBHUNTING_HOME', '~/.jobhunting'))


def perfil_padrao():
    p = os.path.join(jobhunting_home(), 'profile.json')
    if os.path.exists(p):
        return p
    local = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'profile', 'profile.json')
    return local if os.path.exists(local) else p


ACC = RGBColor(0x1F, 0x3A, 0x5F)
C = WD_ALIGN_PARAGRAPH.CENTER
TITULOS = dict(resumo='Resumo Profissional', competencias='Competências-Chave', experiencias='Experiência Profissional',
               formacao='Formação', certificacoes='Certificações e Treinamentos', comunidade='Educação e Comunidade',
               ferramentas='Ferramentas e Habilidades Técnicas')


def contato(p):
    partes = [f"{p.get('cidade', '')}, {p.get('uf', '')}".strip(', '), p.get('telefone'), p.get('email'), p.get('linkedin')]
    return ' | '.join(x for x in partes if x)


def build(perfil, cv, fname, a4=False):
    pessoal = perfil['pessoal']
    d = Document()
    for s in d.sections:
        if a4: s.page_width, s.page_height = Cm(21), Cm(29.7)
        s.top_margin = s.bottom_margin = Cm(1.2); s.left_margin = s.right_margin = Cm(1.5)
    st = d.styles['Normal']; st.font.name = 'Calibri'; st.font.size = Pt(10)

    def p(text='', bold=False, size=None, align=None, after=2, color=None, italic=False):
        para = d.add_paragraph(); para.paragraph_format.space_after = Pt(after)
        if align: para.alignment = align
        r = para.add_run(text); r.bold = bold; r.italic = italic
        if size: r.font.size = Pt(size)
        if color: r.font.color.rgb = color
        return para

    def h(t):
        x = p(t.upper(), bold=True, size=11.5, color=ACC, after=3); x.paragraph_format.space_before = Pt(6)

    def b(t, lead=None):
        x = d.add_paragraph(style='List Bullet'); x.paragraph_format.space_after = Pt(2)
        if lead: r = x.add_run(lead + ': '); r.bold = True
        x.add_run(t)

    p(pessoal['nome'], bold=True, size=20, align=C, after=0)
    p(cv['headline'], bold=True, size=11, align=C, color=ACC, after=2)
    p(contato(pessoal), size=10, align=C, after=4)
    h(TITULOS['resumo']); p(cv['resumo'], after=2)
    if cv.get('competencias'):
        h(TITULOS['competencias'])
        for lead, t in cv['competencias']: b(t, lead)
    h(TITULOS['experiencias'])
    for e in cv.get('experiencias', []):
        x = p(after=0); x.paragraph_format.space_before = Pt(4)
        r = x.add_run(f"{e['empresa']} | {e['periodo']}"); r.bold = True; r.font.size = Pt(11)
        p(e['cargo'], italic=True, after=2)
        for t in e.get('bullets', []): b(t)
    for key in ('formacao', 'certificacoes', 'comunidade'):
        if cv.get(key):
            h(TITULOS[key])
            for t in cv[key]: b(t)
    ferramentas = list(cv.get('ferramentas', []))
    if cv.get('idiomas'): ferramentas.append(['Idiomas', cv['idiomas']])
    if ferramentas:
        h(TITULOS['ferramentas'])
        for lead, t in ferramentas: b(t, lead)
    os.makedirs(os.path.dirname(fname) or '.', exist_ok=True)
    d.save(fname)
    return fname


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
    nome_arquivo = perfil['pessoal']['nome'].replace(' ', '_')
    saida = opt('--saida', os.path.join(jobhunting_home(), 'curriculos', f'{nome_arquivo}_CV.docx'))
    build(perfil, cv, saida, a4='--a4' in a)
    print('DOCX:', saida)
    try:
        subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', os.path.dirname(saida) or '.', saida],
                       check=True, capture_output=True, timeout=120)
        print('PDF:', os.path.splitext(saida)[0] + '.pdf')
    except Exception:
        print('PDF não gerado (instale o LibreOffice para converter).')


if __name__ == '__main__':
    main()
