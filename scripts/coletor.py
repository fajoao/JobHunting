#!/usr/bin/env python3
"""JobHunting – coletor e pontuação de vagas.

Lê vagas de APIs públicas de portais de carreira (Greenhouse, Lever, Workday, Oracle HCM, Gupy,
Amazon Jobs, Google Careers), filtra pelo perfil do usuário e dá um match heurístico de 0 a 100.

Uso:
    python3 -I scripts/coletor.py saida.json [--perfil ~/.jobhunting/profile.json] [--trilha "Product Manager"]

Saída: JSON {coletadas, erros, vagas:[{id, empresa, titulo, local, url, fonte, desc, trilha, match,
local_fit, pontos_fortes, alertas}], em}

Tudo que é pessoal (cargos-alvo, cidades, palavras-chave, empresas excluídas) vem do perfil.
As fontes padrão ficam em FONTES_PADRAO e podem ser trocadas em perfil["busca"]["fontes"].
"""
import json, re, sys, os, html, time, unicodedata, urllib.request, urllib.error, urllib.parse, concurrent.futures as cf

def jobhunting_home():
    """Pasta dos dados do usuário: $JOBHUNTING_HOME ou ~/.jobhunting (fora do repositório e do plugin)."""
    return os.path.expanduser(os.environ.get('JOBHUNTING_HOME', '~/.jobhunting'))


def perfil_padrao():
    p = os.path.join(jobhunting_home(), 'profile.json')
    if os.path.exists(p):
        return p
    local = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'profile', 'profile.json')
    return local if os.path.exists(local) else p


UA = {'User-Agent': 'Mozilla/5.0 (JobHunting)', 'Accept': 'application/json, text/html'}


def get(url, data=None, headers=None, timeout=30):
    h = dict(UA); h.update(headers or {})
    for tent in range(5):
        req = urllib.request.Request(url, data=data, headers=h)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                if 'myworkdayjobs' in url: time.sleep(0.6)
                return r.read().decode('utf-8', 'ignore')
        except urllib.error.HTTPError as e:
            if e.code == 429 and tent < 4: time.sleep(3 * (tent + 1)); continue
            raise


def strip(s):
    s = html.unescape(s or ''); s = re.sub(r'<[^>]+>', ' ', s); s = html.unescape(s)
    return re.sub(r'\s+', ' ', s).strip()


def norm(s):
    s = unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode().lower()
    return re.sub(r'\s+', ' ', s)


# ---------- fontes (APIs públicas de vagas) ----------
def greenhouse(board, empresa):
    j = json.loads(get(f'https://boards-api.greenhouse.io/v1/boards/{board}/jobs?content=true'))
    for x in j['jobs']:
        yield dict(empresa=empresa, titulo=x['title'], local=(x.get('location') or {}).get('name', ''),
                   url=x['absolute_url'], fonte='Greenhouse', desc=strip(x.get('content', '')), ext=f'gh-{board}-{x["id"]}')


def lever(site, empresa):
    for x in json.loads(get(f'https://api.lever.co/v0/postings/{site}?mode=json')):
        c = x.get('categories', {})
        yield dict(empresa=empresa, titulo=x['text'],
                   local=c.get('location', '') + (' | ' + x.get('workplaceType', '') if x.get('workplaceType') else ''),
                   url=x['hostedUrl'], fonte='Lever',
                   desc=strip(x.get('descriptionPlain', '') + ' ' + ' '.join(strip(l.get('content', '')) for l in x.get('lists', []))),
                   ext=f'lv-{site}-{x["id"]}')


def workday(host, tenant, site, empresa, termos):
    vistos = set()
    for t in termos:
        body = json.dumps({'appliedFacets': {}, 'limit': 20, 'offset': 0, 'searchText': t}).encode()
        j = json.loads(get(f'https://{host}/wday/cxs/{tenant}/{site}/jobs', body, {'Content-Type': 'application/json'}))
        for p in j.get('jobPostings', []):
            if p['externalPath'] in vistos: continue
            vistos.add(p['externalPath'])
            desc, loc = '', p.get('locationsText', '')
            try:
                d = json.loads(get(f'https://{host}/wday/cxs/{tenant}/{site}{p["externalPath"]}'))['jobPostingInfo']
                desc, loc = strip(d.get('jobDescription', '')), d.get('location', loc)
            except Exception:
                pass
            yield dict(empresa=empresa, titulo=p['title'], local=loc, url=f'https://{host}/{site}{p["externalPath"]}',
                       fonte='Workday', desc=desc, ext=f'wd-{tenant}-{p["externalPath"].split("_")[-1]}')


def amazon(termos=('manager', 'gerente', 'product manager', 'program manager', 'head'), pais='BRA'):
    vistos = set()
    for q in termos:
        j = json.loads(get('https://www.amazon.jobs/en/search.json?' + urllib.parse.urlencode({'base_query': q, 'country[]': pais, 'result_limit': 100})))
        for x in j.get('jobs', []):
            if x['id_icims'] in vistos: continue
            vistos.add(x['id_icims'])
            yield dict(empresa='Amazon / AWS', titulo=x['title'], local=x.get('normalized_location') or x.get('location', ''),
                       url='https://www.amazon.jobs' + x['job_path'], fonte='Amazon Jobs',
                       desc=strip(x.get('description', '') + ' ' + x.get('basic_qualifications', '') + ' ' + x.get('preferred_qualifications', '')),
                       ext=f'amz-{x["id_icims"]}')


def oracle(host, site, empresa, termos):
    vistos = set()
    for t in termos:
        u = (f'https://{host}/hcmRestApi/resources/latest/recruitingCEJobRequisitions?onlyData=true&expand=requisitionList'
             f'&finder=findReqs;siteNumber={site},keyword={urllib.parse.quote(t)},limit=100')
        for it in json.loads(get(u)).get('items', []):
            for r in it.get('requisitionList', []):
                loc = r.get('PrimaryLocation', '') or ''
                if 'brazil' not in norm(loc + ' ' + (r.get('PrimaryLocationCountry') or '')) and r.get('PrimaryLocationCountry') != 'BR': continue
                if r['Id'] in vistos: continue
                vistos.add(r['Id'])
                yield dict(empresa=empresa, titulo=r['Title'],
                           local=loc + (' | ' + r.get('WorkplaceType', '') if r.get('WorkplaceType') else ''),
                           url=f'https://{host}/hcmUI/CandidateExperience/en/sites/{site}/job/{r["Id"]}', fonte='Oracle HCM',
                           desc=strip((r.get('ShortDescriptionStr') or '') + ' ' + (r.get('ExternalResponsibilitiesStr') or '') + ' ' + (r.get('ExternalQualificationsStr') or '')),
                           ext=f'orc-{site}-{r["Id"]}')


def google(termos=('manager', 'product manager', 'program manager'), pais='Brazil'):
    vistos = set()
    for q in termos:
        g = get('https://www.google.com/about/careers/applications/jobs/results?' + urllib.parse.urlencode({'location': pais, 'q': q}))
        for jid, slug in re.findall(r'jobs/results/(\d+)-([a-z0-9-]+)', g):
            if jid in vistos: continue
            vistos.add(jid)
            yield dict(empresa='Google', titulo=slug.replace('-', ' ').title(), local=f'{pais} (ver vaga)',
                       url=f'https://www.google.com/about/careers/applications/jobs/results/{jid}-{slug}', fonte='Google Careers', desc='', ext=f'goo-{jid}')


def gupy(sub, empresa):
    s = get(f'https://{sub}.gupy.io/')
    d = json.loads(re.search(r'__NEXT_DATA__[^>]*>(.*?)</script>', s, re.S).group(1))
    for x in d['props']['pageProps'].get('jobs', []):
        w = x.get('workplace') or {}; a = w.get('address') or {}
        yield dict(empresa=empresa, titulo=x['title'], local=f"{a.get('city','')}/{a.get('stateShortName','')} | {w.get('workplaceType','')}",
                   url=f'https://{sub}.gupy.io/jobs/{x["id"]}', fonte='Gupy', desc=x.get('department', '') or '', ext=f'gupy-{sub}-{x["id"]}')


WD_TERMOS = ['manager', 'gerente', 'product', 'head', 'coordenador']

# Cada fonte: {tipo, args}. Workday roda em sequência (limita requisições); as demais em paralelo.
FONTES_PADRAO = [
    {'tipo': 'greenhouse', 'args': ['btgpactual', 'BTG Pactual']},
    {'tipo': 'greenhouse', 'args': ['inter', 'Banco Inter']},
    {'tipo': 'greenhouse', 'args': ['xpinc', 'XP Inc']},
    {'tipo': 'greenhouse', 'args': ['c6bank', 'C6 Bank']},
    {'tipo': 'greenhouse', 'args': ['stone', 'Stone']},
    {'tipo': 'greenhouse', 'args': ['vtex', 'VTEX']},
    {'tipo': 'greenhouse', 'args': ['gympass', 'Wellhub']},
    {'tipo': 'greenhouse', 'args': ['quintoandar', 'QuintoAndar']},
    {'tipo': 'greenhouse', 'args': ['ebanx', 'EBANX']},
    {'tipo': 'lever', 'args': ['bv', 'Banco BV']},
    {'tipo': 'lever', 'args': ['ciandt', 'CI&T']},
    {'tipo': 'workday', 'args': ['santander.wd3.myworkdayjobs.com', 'santander', 'SantanderCareers', 'Santander', WD_TERMOS]},
    {'tipo': 'workday', 'args': ['nvidia.wd5.myworkdayjobs.com', 'nvidia', 'NVIDIAExternalCareerSite', 'NVIDIA', ['brazil']]},
    {'tipo': 'workday', 'args': ['salesforce.wd12.myworkdayjobs.com', 'salesforce', 'External_Career_Site', 'Salesforce', ['brazil', 'sao paulo']]},
    {'tipo': 'workday', 'args': ['redhat.wd5.myworkdayjobs.com', 'redhat', 'jobs', 'Red Hat', ['brazil']]},
    {'tipo': 'amazon', 'args': []},
    {'tipo': 'google', 'args': []},
    {'tipo': 'oracle', 'args': ['eeho.fa.us2.oraclecloud.com', 'CX_45001', 'Oracle', ['manager brazil', 'product manager', 'gerente']]},
    {'tipo': 'oracle', 'args': ['enterpriseplatform.dell.com', 'CX_1', 'Dell', ['manager brazil', 'gerente']]},
    {'tipo': 'gupy', 'args': ['vemproitau', 'Itaú Unibanco']},
]
TIPOS = {'greenhouse': greenhouse, 'lever': lever, 'workday': workday, 'amazon': amazon, 'oracle': oracle, 'google': google, 'gupy': gupy}

# ---------- regras padrão (o perfil pode sobrescrever) ----------
# Vagas afirmativas: só entram se o perfil marcar o grupo em busca.vagas_afirmativas (ex.: ["pcd", "mulheres"]).
AFIRMATIVAS = {
    'pcd': r'(exclusiva (para )?(pessoas? com deficiencia|pcd)|para pcd|people with disabilities)',
    'mulheres': r'(exclusiva para mulher(es)?|women in tech|for women|para mulheres|vaga afirmativa para mulheres)',
}
SENIORIDADE_EXCLUIDA = r'\b(jr|junior|pleno|pl|estagi\w*|intern(ship)?|aprendiz|trainee|assistente|auxiliar|banco de talentos|talent pool|pool)\b'
TITULOS_EXCLUIDOS = (r'(veiculos|relacionamento|agencia|comercial|vendas|sales|account executive|private banker|credito|cobranca|juridico|'
                     r'recursos humanos|recruiter|marketing|contabil|fiscal|tributar|warehouse|fulfillment|logistics|site manager)')
TITULO_NO_DOMINIO = r'\b(ai|ia|automation|automacao|cloud|platform|plataforma|operations|operacoes|sre|infra|data|dados|payments|pagamentos)\b'
INGLES_FLUENTE = r'(fluent english|english fluency|fluency in english|ingles fluente|ingles avancado|advanced english|native english|business fluent)'
NIVEL_ACIMA = r'\b(director|diretor|vp|vice president|superintendente)\b'
SENIOR = r'(senior|sr\b|especialista|staff|principal|coordenador|manager|gerente|head|lead)'


def carregar_perfil(caminho):
    if not caminho or not os.path.exists(caminho):
        sys.exit(f'Perfil não encontrado: {caminho}. Rode a skill jobhunting-setup ou scripts/setup_perfil.py.')
    with open(caminho, encoding='utf-8') as f:
        return json.load(f)


class Regras:
    def __init__(self, perfil):
        b = perfil.get('busca', {})
        self.trilhas = [(t['nome'], t['titulos'], t.get('titulos_fortes', t['titulos'])) for t in b.get('trilhas', [])]
        if not self.trilhas:
            sys.exit('O perfil não tem trilhas em busca.trilhas.')
        self.senioridade = b.get('senioridade_excluida') or SENIORIDADE_EXCLUIDA
        self.excluidos = b.get('titulos_excluidos') or TITULOS_EXCLUIDOS
        self.palavras = b.get('palavras_chave') or {}
        loc = b.get('locais', {})
        self.remoto = loc.get('aceita_remoto_brasil', True)
        self.cidades = [norm(c) for c in loc.get('cidades_aceitas', [])]
        self.mudanca = loc.get('aceita_mudanca', False)
        self.ingles_fluente_ok = (b.get('nivel_ingles') or '').upper() in ('C1', 'C2', 'FLUENTE', 'NATIVO')
        self.empresas_excluidas = [norm(e) for e in b.get('empresas_excluidas', [])]
        incluir = {norm(x) for x in b.get('vagas_afirmativas', [])}
        self.afirmativas_fora = [pat for grupo, pat in AFIRMATIVAS.items() if grupo not in incluir]

    def trilha(self, titulo):
        n = norm(titulo)
        if any(re.search(p, n) for p in self.afirmativas_fora) or re.search(self.senioridade, n) or re.search(self.excluidos, n):
            return None
        for nome, pat, _ in self.trilhas:
            if re.search(pat, n):
                return nome
        return None

    def local(self, loc, desc):
        n = norm(loc + ' ' + desc[:600])
        nl = norm(loc)
        remoto = bool(re.search(r'\b(remote|remoto|home office|anywhere)\b', n))
        na_cidade = any(c and c in nl for c in self.cidades)
        brasil = na_cidade or bool(re.search(r'(brasil|brazil|\b(sp|rj|mg|pr|sc|rs|df|pe|ba|go|es)\b|sao paulo|rio de janeiro|belo horizonte|curitiba|recife|campinas|porto alegre|florianopolis|brasilia)', nl))
        if not brasil and not (remoto and ('brasil' in n or 'brazil' in n)):
            return None, 'fora do Brasil'
        if na_cidade: return 10, 'cidade aceita'
        if remoto and self.remoto: return 10, 'remoto (Brasil)'
        if self.mudanca: return 5, 'outra cidade (aceita mudança)'
        return None, 'outra cidade presencial/híbrida'

    def score(self, v, tri):
        t, d = norm(v['titulo']), norm(v['desc'])
        pts, achados = 0, []
        forte = next((f for nome, _, f in self.trilhas if nome == tri), None)
        pts += 30 if forte and re.search(forte, t) else 22
        if re.search(TITULO_NO_DOMINIO, t): pts += 5; achados.append('título no seu domínio')
        kw = 0
        for pat, w in self.palavras.items():
            if re.search(pat, d) or re.search(pat, t):
                kw += w; achados.append(pat.split('|')[0].replace('\\b', ''))
        pts += min(kw, 40) * 35 // 40 if d else 12
        lp, lmot = self.local(v['local'], v['desc'])
        pts += lp or 0
        pts += 10 if re.search(SENIOR, t) else 5
        pen = []
        if not self.ingles_fluente_ok and (re.search(INGLES_FLUENTE, d) or (d and not re.search(r'\b(voce|para|com|experiencia|nos)\b', d))):
            pts -= 10; pen.append('exige inglês fluente')
        if re.search(NIVEL_ACIMA, t): pts -= 8; pen.append('nível acima de gerente')
        if not d: pen.append('sem descrição completa na fonte')
        return max(0, min(100, pts)), lmot, achados[:8], pen


def main(out, caminho_perfil, so_trilha=None):
    perfil = carregar_perfil(caminho_perfil)
    regras = Regras(perfil)
    fontes = perfil.get('busca', {}).get('fontes') or FONTES_PADRAO
    vagas, erros = [], {}

    def rodar(f):
        return list(TIPOS[f['tipo']](*f['args']))

    def workdays():
        out = []
        for f in fontes:
            if f['tipo'] != 'workday': continue
            try: out += rodar(f)
            except Exception as e: erros[f['args'][3]] = repr(e)[:200]
        return out

    with cf.ThreadPoolExecutor(8) as ex:
        futs = {ex.submit(rodar, f): (f['args'][1] if len(f['args']) > 1 else f['tipo']) for f in fontes if f['tipo'] != 'workday'}
        futs[ex.submit(workdays)] = 'workday'
        for fu in cf.as_completed(futs):
            try: vagas += fu.result()
            except Exception as e: erros[str(futs[fu])] = repr(e)[:200]

    res, total = [], len(vagas)
    for v in vagas:
        if any(e and e in norm(v['empresa']) for e in regras.empresas_excluidas): continue
        tri = regras.trilha(v['titulo'])
        if not tri or (so_trilha and tri != so_trilha): continue
        lp, _ = regras.local(v['local'], v['desc'])
        if lp is None: continue
        s, lmot, ach, pen = regras.score(v, tri)
        v.update(id=re.sub(r'[^A-Za-z0-9_.~:@+-]', '-', v['ext'])[:180], trilha=tri, match=s, local_fit=lmot, pontos_fortes=ach, alertas=pen)
        v['desc'] = v['desc'][:6000]
        res.append(v)
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, 'w', encoding='utf-8') as f:
        json.dump({'coletadas': total, 'erros': erros, 'vagas': res, 'em': time.strftime('%Y-%m-%dT%H:%M:%S')}, f, ensure_ascii=False)
    print(f'coletadas={total} no_perfil_filtradas={len(res)} erros={erros}')


if __name__ == '__main__':
    a = sys.argv[1:]
    def opt(nome, padrao=None):
        return a[a.index(nome) + 1] if nome in a else padrao
    saida = a[0] if a and not a[0].startswith('--') else 'vagas.json'
    main(saida, opt('--perfil', perfil_padrao()), opt('--trilha'))
