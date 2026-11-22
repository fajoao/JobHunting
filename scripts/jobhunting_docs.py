#!/usr/bin/env python3
"""JobHunting – renderizador de documentos (PDF e DOCX) a partir de uma lista de blocos.

Usado pelos geradores de currículo ATS, carta de apresentação, plano de crescimento no LinkedIn
e guia de abordagem a recrutadores. O PDF é texto puro (sem imagens, tabelas de layout ou
colunas), o que mantém o currículo legível para sistemas ATS.

Blocos aceitos (dicts com "t"):
  nome, titulos, contato, regua            cabeçalho do currículo/carta
  titulo_doc, subtitulo                    cabeçalho de guias e planos
  secao                                    título de seção em CAIXA ALTA com linha abaixo
  secao_num                                título de seção de guia (ex.: "1. O que é o SSI")
  subsecao                                 título menor em negrito
  empresa, cargo                           linhas de experiência
  p {text, italic?, justify?}              parágrafo; **negrito** é aceito
  bullets {items}                          lista com marcadores; **negrito** é aceito
  citacao {text}                           texto recuado (mensagens e exemplos)
  tabela {cabecalho, linhas, larguras?, destacar?}
  espaco, quebra_pagina
Requer: pip install reportlab python-docx
Se o pip recusar instalar no Python do sistema (PEP 668), crie o ambiente do JobHunting:
    python3 -m venv ~/.jobhunting/venv && ~/.jobhunting/venv/bin/pip install -r scripts/requirements.txt
Os scripts passam a usá-lo sozinhos: se faltar o reportlab, reiniciam com ~/.jobhunting/venv/bin/python.
"""
import os, re, sys


def _usar_venv_se_preciso():
    """Sem reportlab/python-docx no Python atual, reinicia o script com o venv do JobHunting, se existir."""
    try:
        import reportlab, docx  # noqa: F401
        return
    except ImportError:
        pass
    home = os.path.expanduser(os.environ.get('JOBHUNTING_HOME', '~/.jobhunting'))
    venv = os.path.join(home, 'venv')
    py = os.path.join(venv, 'bin', 'python')
    ja_no_venv = os.path.realpath(sys.prefix) == os.path.realpath(venv)
    if os.path.exists(py) and not ja_no_venv and not os.environ.get('JOBHUNTING_NO_VENV'):
        os.environ['JOBHUNTING_NO_VENV'] = '1'  # evita laço se o venv também estiver incompleto
        os.execv(py, [py] + sys.argv)


_usar_venv_se_preciso()

CINZA = (0x55, 0x55, 0x55)
CINZA_CLARO = (0x88, 0x88, 0x88)


def _md_rl(text):
    t = (text or '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)


def _md_runs(text):
    partes = re.split(r'(\*\*.+?\*\*)', text or '')
    return [(p[2:-2], True) if p.startswith('**') and p.endswith('**') else (p, False) for p in partes if p]


# ---------------------------------------------------------------- PDF (reportlab)
def gerar_pdf(blocos, caminho, rodape='', pagina='Página'):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm
    from reportlab.lib import colors
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable,
                                    ListFlowable, ListItem, PageBreak, KeepTogether)

    cinza = colors.Color(*[c / 255 for c in CINZA])
    cinza_claro = colors.Color(*[c / 255 for c in CINZA_CLARO])
    base = dict(fontName='Helvetica', fontSize=9.5, leading=12.6)
    S = {
        'nome': ParagraphStyle('nome', fontName='Helvetica-Bold', fontSize=21, leading=25, alignment=TA_CENTER),
        'titulos': ParagraphStyle('titulos', fontName='Helvetica-Bold', fontSize=9.5, leading=12, alignment=TA_CENTER, textColor=cinza, spaceBefore=2),
        'contato': ParagraphStyle('contato', fontName='Helvetica', fontSize=9, leading=12, alignment=TA_CENTER, spaceBefore=2),
        'titulo_doc': ParagraphStyle('titulo_doc', fontName='Helvetica-Bold', fontSize=18, leading=22),
        'subtitulo': ParagraphStyle('subtitulo', fontName='Helvetica', fontSize=11, leading=14, textColor=cinza, spaceBefore=2),
        'secao': ParagraphStyle('secao', fontName='Helvetica-Bold', fontSize=11, leading=13, spaceBefore=9),
        'secao_num': ParagraphStyle('secao_num', fontName='Helvetica-Bold', fontSize=12.5, leading=15, spaceBefore=11, spaceAfter=3),
        'subsecao': ParagraphStyle('subsecao', fontName='Helvetica-Bold', fontSize=9.5, leading=12, spaceBefore=6, spaceAfter=1),
        'empresa': ParagraphStyle('empresa', fontName='Helvetica-Bold', fontSize=10, leading=12.5, spaceBefore=6),
        'cargo': ParagraphStyle('cargo', fontName='Helvetica-Bold', fontSize=9.5, leading=12, textColor=cinza, spaceAfter=1),
        'p': ParagraphStyle('p', alignment=TA_JUSTIFY, spaceAfter=3, **base),
        'p_esq': ParagraphStyle('p_esq', alignment=TA_LEFT, spaceAfter=3, **base),
        'bullet': ParagraphStyle('bullet', alignment=TA_JUSTIFY, **base),
        'citacao': ParagraphStyle('citacao', leftIndent=14, spaceAfter=4, alignment=TA_LEFT, **base),
        'cel': ParagraphStyle('cel', fontName='Helvetica', fontSize=8.5, leading=10.5),
        'cel_h': ParagraphStyle('cel_h', fontName='Helvetica-Bold', fontSize=8.5, leading=10.5, textColor=colors.white),
        'rodape': ParagraphStyle('rodape', fontName='Helvetica', fontSize=7.5, alignment=TA_CENTER, textColor=cinza_claro),
    }

    flow = []
    for b in blocos:
        t = b['t']
        if t in ('nome', 'titulos', 'contato', 'titulo_doc', 'subtitulo', 'subsecao', 'empresa', 'cargo'):
            txt = b['text'].upper() if t in ('nome', 'titulos') else b['text']
            flow.append(Paragraph(_md_rl(txt), S[t]))
        elif t == 'regua':
            flow.append(HRFlowable(width='100%', thickness=1.3, color=colors.black, spaceBefore=5, spaceAfter=7))
        elif t == 'secao':
            flow.append(KeepTogether([Paragraph(_md_rl(b['text'].upper()), S['secao']),
                                      HRFlowable(width='100%', thickness=0.6, color=colors.black, spaceBefore=1, spaceAfter=4)]))
        elif t == 'secao_num':
            flow.append(Paragraph(_md_rl(b['text']), S['secao_num']))
        elif t == 'p':
            st = S['p'] if b.get('justify', True) else S['p_esq']
            if b.get('after') is not None:
                st = ParagraphStyle(st.name + str(b['after']), parent=st, spaceAfter=b['after'])
            txt = _md_rl(b['text'])
            if b.get('italic'): txt = f'<i>{txt}</i>'
            flow.append(Paragraph(txt, st))
        elif t == 'bullets':
            itens = [ListItem(Paragraph(_md_rl(x), S['bullet']), leftIndent=10, value='•') for x in b['items']]
            flow.append(ListFlowable(itens, bulletType='bullet', start='•', leftIndent=10, bulletFontSize=9, bulletOffsetY=-1, spaceAfter=3))
        elif t == 'citacao':
            flow.append(Paragraph(_md_rl(b['text']), S['citacao']))
        elif t == 'tabela':
            dados = [[Paragraph(_md_rl(c), S['cel_h']) for c in b['cabecalho']]]
            dados += [[Paragraph(_md_rl(str(c)), S['cel']) for c in linha] for linha in b['linhas']]
            larg = b.get('larguras')
            largura_total = A4[0] - 3.4 * cm
            col = [largura_total * w for w in larg] if larg else None
            tab = Table(dados, colWidths=col, repeatRows=1)
            estilo = [('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.12, 0.12, 0.12)),
                      ('GRID', (0, 0), (-1, -1), 0.4, colors.Color(0.8, 0.8, 0.8)),
                      ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                      ('TOPPADDING', (0, 0), (-1, -1), 3), ('BOTTOMPADDING', (0, 0), (-1, -1), 3)]
            for i in b.get('destacar', []):
                estilo.append(('BACKGROUND', (0, i + 1), (-1, i + 1), colors.Color(0.9, 0.9, 0.9)))
            tab.setStyle(TableStyle(estilo))
            flow.append(Spacer(1, 3)); flow.append(tab); flow.append(Spacer(1, 4))
        elif t == 'espaco':
            flow.append(Spacer(1, b.get('altura', 8)))
        elif t == 'quebra_pagina':
            flow.append(PageBreak())

    def rodape_fn(canvas, doc):
        if not rodape: return
        canvas.saveState()
        canvas.setFont('Helvetica', 7.5); canvas.setFillColor(cinza_claro)
        canvas.drawCentredString(A4[0] / 2, 1.0 * cm, f'{rodape}  |  {pagina} {doc.page}')
        canvas.restoreState()

    os.makedirs(os.path.dirname(caminho) or '.', exist_ok=True)
    doc = SimpleDocTemplate(caminho, pagesize=A4, leftMargin=1.7 * cm, rightMargin=1.7 * cm,
                            topMargin=1.4 * cm, bottomMargin=1.6 * cm, title=rodape or 'JobHunting', author=rodape)
    doc.build(flow, onFirstPage=rodape_fn, onLaterPages=rodape_fn)
    return caminho


# ---------------------------------------------------------------- DOCX (python-docx)
def gerar_docx(blocos, caminho, rodape='', pagina='Página'):
    from docx import Document
    from docx.shared import Pt, Cm, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement

    d = Document()
    for s in d.sections:
        s.page_width, s.page_height = Cm(21), Cm(29.7)
        s.top_margin, s.bottom_margin = Cm(1.4), Cm(1.6)
        s.left_margin = s.right_margin = Cm(1.7)
        if rodape:
            fp = s.footer.paragraphs[0]; fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = fp.add_run(f'{rodape}  |  {pagina} '); r.font.size = Pt(7.5); r.font.color.rgb = RGBColor(*CINZA_CLARO)
            for tag, txt in (('begin', None), (None, 'PAGE'), ('end', None)):
                run = fp.add_run(); run.font.size = Pt(7.5)
                if tag:
                    el = OxmlElement('w:fldChar'); el.set(qn('w:fldCharType'), tag)
                else:
                    el = OxmlElement('w:instrText'); el.set(qn('xml:space'), 'preserve'); el.text = txt
                run._r.append(el)
    st = d.styles['Normal']; st.font.name = 'Arial'; st.font.size = Pt(9.5)

    def linha_inferior(par, espessura=8):
        pPr = par._p.get_or_add_pPr(); bdr = OxmlElement('w:pBdr'); bot = OxmlElement('w:bottom')
        bot.set(qn('w:val'), 'single'); bot.set(qn('w:sz'), str(espessura)); bot.set(qn('w:space'), '1'); bot.set(qn('w:color'), '000000')
        bdr.append(bot); pPr.append(bdr)

    def par(texto, size=9.5, bold=False, italic=False, color=None, align=None, after=3, before=0, md=True, upper=False):
        p = d.add_paragraph(); f = p.paragraph_format; f.space_after = Pt(after); f.space_before = Pt(before)
        if align: p.alignment = align
        texto = texto.upper() if upper else texto
        for txt, neg in (_md_runs(texto) if md else [(texto, False)]):
            r = p.add_run(txt); r.bold = bold or neg; r.italic = italic; r.font.size = Pt(size)
            if color: r.font.color.rgb = RGBColor(*color)
        return p

    C, J = WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.JUSTIFY
    for b in blocos:
        t = b['t']
        if t == 'nome': par(b['text'], 21, True, align=C, after=0, upper=True)
        elif t == 'titulos': par(b['text'], 9.5, True, color=CINZA, align=C, after=1, upper=True)
        elif t == 'contato': par(b['text'], 9, align=C, after=2)
        elif t == 'regua': linha_inferior(par('', 2, after=6), 12)
        elif t == 'titulo_doc': par(b['text'], 18, True, after=1)
        elif t == 'subtitulo': par(b['text'], 11, color=CINZA, after=4)
        elif t == 'secao': linha_inferior(par(b['text'], 11, True, before=9, after=4, upper=True))
        elif t == 'secao_num': par(b['text'], 12.5, True, before=11, after=3)
        elif t == 'subsecao': par(b['text'], 9.5, True, before=6, after=1)
        elif t == 'empresa': par(b['text'], 10, True, before=6, after=0)
        elif t == 'cargo': par(b['text'], 9.5, True, color=CINZA, after=1)
        elif t == 'p': par(b['text'], italic=b.get('italic', False), align=J if b.get('justify', True) else None, after=b.get('after', 3))
        elif t == 'bullets':
            for x in b['items']:
                p = d.add_paragraph(style='List Bullet'); p.paragraph_format.space_after = Pt(1); p.alignment = J
                for txt, neg in _md_runs(x):
                    r = p.add_run(txt); r.bold = neg; r.font.size = Pt(9.5)
        elif t == 'citacao':
            p = par(b['text']); p.paragraph_format.left_indent = Cm(0.5)
        elif t == 'tabela':
            tab = d.add_table(rows=1, cols=len(b['cabecalho'])); tab.style = 'Table Grid'
            for i, h in enumerate(b['cabecalho']):
                c = tab.rows[0].cells[i]; c.text = ''; r = c.paragraphs[0].add_run(h); r.bold = True; r.font.size = Pt(8.5)
            for linha in b['linhas']:
                cells = tab.add_row().cells
                for i, v in enumerate(linha):
                    cells[i].text = ''
                    for txt, neg in _md_runs(str(v)):
                        r = cells[i].paragraphs[0].add_run(txt); r.bold = neg; r.font.size = Pt(8.5)
            d.add_paragraph()
        elif t == 'espaco': d.add_paragraph()
        elif t == 'quebra_pagina': d.add_page_break()

    os.makedirs(os.path.dirname(caminho) or '.', exist_ok=True)
    d.save(caminho)
    return caminho


def pasta_privada(caminho):
    """Cria a pasta (e as intermediárias) com permissão 700: os documentos têm dados pessoais."""
    os.makedirs(caminho, mode=0o700, exist_ok=True)
    try: os.chmod(caminho, 0o700)
    except OSError: pass


def gerar(blocos, base_sem_extensao, rodape='', formatos=('pdf', 'docx'), pagina='Página'):
    """Gera os formatos pedidos (arquivos com permissão 600) e devolve a lista de caminhos."""
    pasta_privada(os.path.dirname(os.path.abspath(base_sem_extensao)))
    saidas = []
    if 'pdf' in formatos: saidas.append(gerar_pdf(blocos, base_sem_extensao + '.pdf', rodape, pagina))
    if 'docx' in formatos: saidas.append(gerar_docx(blocos, base_sem_extensao + '.docx', rodape, pagina))
    for s in saidas:
        try: os.chmod(s, 0o600)
        except OSError: pass
    return saidas


def jobhunting_home():
    return os.path.expanduser(os.environ.get('JOBHUNTING_HOME', '~/.jobhunting'))


def perfil_padrao():
    p = os.path.join(jobhunting_home(), 'profile.json')
    if os.path.exists(p): return p
    local = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'profile', 'profile.json')
    return local if os.path.exists(local) else p


def slug(texto):
    import unicodedata
    s = unicodedata.normalize('NFKD', texto or '').encode('ascii', 'ignore').decode()
    return re.sub(r'[^A-Za-z0-9]+', '_', s).strip('_')


def contato(pessoal):
    local = ' – '.join(x for x in (pessoal.get('cidade'), pessoal.get('uf')) if x)
    return ' | '.join(x for x in (local, pessoal.get('telefone'), pessoal.get('email'), pessoal.get('linkedin')) if x)


MESES = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']


def data_extenso(d):
    return f'{d.day} de {MESES[d.month - 1]} de {d.year}'
