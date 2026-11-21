#!/usr/bin/env python3
"""JobHunting – cria o seu perfil respondendo a perguntas no terminal.

Uso:
    python3 scripts/setup_perfil.py            # cria ~/.jobhunting/profile.json
    python3 scripts/setup_perfil.py --revisar  # pergunta de novo, mostrando as respostas atuais

O perfil fica só no seu computador, em ~/.jobhunting/profile.json (ou $JOBHUNTING_HOME), fora do repositório.
Nunca pedimos CPF, RG ou senhas. Dados sensíveis são opcionais: deixe em branco para não informar.
Com o Claude Code, prefira a skill /jobhunting:jobhunting-setup, que faz a mesma entrevista em conversa.
"""
import json, os, sys, copy

EXEMPLO = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'profile', 'profile.example.json')
BASE = os.path.expanduser(os.environ.get('JOBHUNTING_HOME', '~/.jobhunting'))
DESTINO = os.path.join(BASE, 'profile.json')


def perguntar(texto, atual='', obrigatorio=False):
    dica = f' [{atual}]' if atual else ''
    while True:
        r = input(f'{texto}{dica}: ').strip()
        if r: return r
        if atual or not obrigatorio: return atual
        print('  Esta resposta é obrigatória.')


def sim_nao(texto, atual=True):
    r = input(f"{texto} [{'S/n' if atual else 's/N'}]: ").strip().lower()
    return atual if not r else r.startswith('s')


def lista(texto, atual):
    r = input(f"{texto} (separe por vírgula) [{', '.join(atual)}]: ").strip()
    return [x.strip() for x in r.split(',') if x.strip()] if r else atual


def main():
    revisar = '--revisar' in sys.argv
    origem = DESTINO if (revisar and os.path.exists(DESTINO)) else EXEMPLO
    with open(origem, encoding='utf-8') as f:
        perfil = json.load(f)
    if origem == EXEMPLO:
        perfil = copy.deepcopy(perfil)
        for k in ('nome', 'primeiro_nome', 'email', 'telefone', 'linkedin', 'cidade', 'uf'):
            perfil['pessoal'][k] = ''

    print('\n== JobHunting: seu perfil ==')
    print('Só você vê estas respostas. Nada de CPF, RG ou senha.\n')

    p = perfil['pessoal']
    p['nome'] = perguntar('Nome completo', p['nome'], True)
    p['primeiro_nome'] = perguntar('Primeiro nome (usado nas mensagens)', p['primeiro_nome'] or p['nome'].split()[0])
    p['email'] = perguntar('E-mail para candidaturas', p['email'], True)
    p['telefone'] = perguntar('Telefone com DDD', p['telefone'])
    p['linkedin'] = perguntar('URL do seu LinkedIn', p['linkedin'])
    p['cidade'] = perguntar('Cidade onde mora', p['cidade'], True)
    p['uf'] = perguntar('UF', p['uf'], True)

    b = perfil['busca']
    print('\n-- Vagas que você procura --')
    nomes = lista('Trilhas de cargo (ex.: Product Manager, Liderança)', [t['nome'] for t in b['trilhas']])
    trilhas = []
    for n in nomes:
        ex = next((t for t in b['trilhas'] if t['nome'] == n), None)
        if ex:
            trilhas.append(ex); continue
        termos = lista(f'  Títulos que contam como "{n}" (ex.: data manager, gerente de dados)', [n.lower()])
        pat = '(' + '|'.join(t.lower() for t in termos) + ')'
        trilhas.append({'nome': n, 'titulos': pat, 'titulos_fortes': pat})
    b['trilhas'] = trilhas
    print('\n-- Onde buscar --')
    print('Grupos: linkedin (busca booleana), big_techs (Microsoft, Amazon, Google, NVIDIA, Salesforce, Red Hat, Oracle, Dell),')
    print('        bancos (bancos e fintechs), tech (empresas de tecnologia). Também aceita um site, ex.: microsoft.')
    print('Liste tudo com: python3 -I scripts/coletor.py --listar-sites')
    b['sites'] = [x.lower() for x in lista('Em quais sites buscar vagas? (todos = tudo)', b.get('sites') or ['todos'])]
    b['todas_as_vagas'] = [x.lower() for x in lista('Empresas em que você quer TODAS as vagas, não só as da sua trilha', b.get('todas_as_vagas', ['microsoft', 'amazon', 'google']))]
    if 'linkedin' in b['sites'] or 'todos' in b['sites']:
        li = b.setdefault('linkedin', {})
        li['temas'] = lista('LinkedIn: temas para o AND da busca booleana (ex.: IA, cloud; vazio = só títulos)', li.get('temas', []))
        li['periodo'] = perguntar('LinkedIn: período das vagas (24h, semana, mes; vazio = qualquer)', li.get('periodo', ''))
        li['so_remoto'] = sim_nao('LinkedIn: só vagas remotas?', li.get('so_remoto', False))
    loc = b['locais']
    loc['aceita_remoto_brasil'] = sim_nao('Aceita trabalho remoto no Brasil?', loc['aceita_remoto_brasil'])
    loc['cidades_aceitas'] = [c.lower() for c in lista('Cidades aceitas para híbrido/presencial', loc['cidades_aceitas'])]
    loc['aceita_mudanca'] = sim_nao('Aceita mudar de cidade?', loc['aceita_mudanca'])
    b['nivel_ingles'] = perguntar('Nível de inglês (A1–C2, Fluente)', b['nivel_ingles'])
    b['empresas_excluidas'] = lista('Empresas que você NÃO quer ver (ex.: empregador atual)', b['empresas_excluidas'])
    b['vagas_afirmativas'] = [x.lower() for x in lista('Incluir vagas afirmativas para quais grupos? (pcd, mulheres; deixe vazio para nenhum)', b.get('vagas_afirmativas', []))]
    b['candidatura_automatica'] = sim_nao('Permitir que o Claude envie candidaturas em formulários públicos (sem login/CAPTCHA)?', b['candidatura_automatica'])

    c = perfil['candidatura']
    print('\n-- Dados para formulários (todos opcionais) --')
    c['empresa_atual_ou_anterior'] = perguntar('Empresa atual ou anterior', c['empresa_atual_ou_anterior'])
    c['remuneracao_atual'] = perguntar('Remuneração atual/anterior (ex.: R$ 10.000 CLT)', c['remuneracao_atual'])
    for t in b['trilhas']:
        c['pretensao_salarial'][t['nome']] = perguntar(f"Pretensão salarial para {t['nome']}", c['pretensao_salarial'].get(t['nome'], ''))
    c['disponibilidade'] = perguntar('Disponibilidade para início', c['disponibilidade'])
    if sim_nao('Quer responder perguntas de autoidentificação (gênero, raça/cor, PcD)? Elas aparecem em alguns formulários.', False):
        a = c['autoidentificacao']
        for k, rot in (('genero', 'Gênero'), ('raca_cor', 'Raça/cor'), ('pcd', 'Pessoa com deficiência (sim/não)'), ('orientacao_sexual', 'Orientação sexual')):
            a[k] = perguntar(f'  {rot} (deixe em branco para não informar)', a.get(k, ''))

    m = perfil['mensagens']
    print('\n-- Mensagens para recrutadores --')
    m['foco_cargo'] = perguntar('Como você se apresenta (ex.: Product Manager com foco em IA)', m['foco_cargo'])
    m['foco'] = perguntar('Sua área em uma frase curta (ex.: Product Management de IA)', m['foco'])
    m['conquista_principal'] = perguntar('Sua principal conquista com número (ex.: reduzi o tempo de X de N para M)', m['conquista_principal'])
    if sim_nao('Quer as versões em inglês das mensagens (para recrutadores de fora)?', False):
        m['foco_cargo_en'] = perguntar('  Como você se apresenta, em inglês', m['foco_cargo_en'])
        m['foco_en'] = perguntar('  Sua área, em inglês', m['foco_en'])
        m['conquista_principal_en'] = perguntar('  Sua conquista, em inglês', m['conquista_principal_en'])
    m['assinatura'] = p['primeiro_nome']

    print('\nO bloco "curriculo" (resumo, experiências, formação, certificações) segue o modelo ATS e é longo para o terminal.')
    print(f'Edite-o em {DESTINO} ou peça à skill jobhunting-setup para montar a partir do seu CV atual.')

    os.makedirs(BASE, mode=0o700, exist_ok=True)
    os.chmod(BASE, 0o700)
    with open(DESTINO, 'w', encoding='utf-8') as f:
        json.dump(perfil, f, ensure_ascii=False, indent=2)
    os.chmod(DESTINO, 0o600)
    print(f'\nPerfil salvo em {DESTINO} (só você pode ler).')


if __name__ == '__main__':
    main()
