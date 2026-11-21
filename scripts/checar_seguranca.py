#!/usr/bin/env python3
"""JobHunting – checagem de segurança e privacidade antes de commitar ou publicar.

Procura no repositório:
  • perfis reais versionados (profile.json, contatos.csv, documentos gerados);
  • segredos (tokens do GitHub, chaves de API, chaves privadas, senhas);
  • CPF, telefones e e-mails reais fora dos exemplos fictícios;
  • links javascript: no app;
  • frontmatter de skills e agentes com description fora de aspas (quebra o YAML com ": ").
Uso: python3 -I scripts/checar_seguranca.py   (sai com código 1 se achar algo)
"""
import os, re, subprocess, sys

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
IGNORAR_DIRS = {'.git', 'node_modules', 'dist', 'publish'}
EXTENSOES = {'.py', '.md', '.json', '.ts', '.tsx', '.js', '.html', '.csv', '.txt', '.yml', '.yaml', '.css'}
PROIBIDOS = [r'(^|/)profile/profile\.json$', r'contatos\.csv$', r'\.(pdf|docx)$', r'(^|/)\.env']
PADROES = {
    'token GitHub': r'gh[pousr]_[A-Za-z0-9]{20,}',
    'chave de API': r'\b(sk-[A-Za-z0-9_-]{20,}|AKIA[0-9A-Z]{16}|xox[baprs]-[A-Za-z0-9-]{10,})',
    'chave privada': r'-----BEGIN [A-Z ]*PRIVATE KEY-----',
    'CPF': r'\b\d{3}\.\d{3}\.\d{3}-\d{2}\b',
    'telefone': r'\(\d{2}\)\s?9?\d{4,5}-\d{4}',
    'e-mail': r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',
    'link javascript:': r'href=["\']?javascript:',
}
# Valores fictícios e endereços técnicos permitidos
PERMITIDOS = [r'voce@exemplo\.com', r'@exemplo\.com', r'\(00\) 00000-0000', r'noreply@anthropic\.com',
              r'users\.noreply\.github\.com', r'@users\.noreply', r'\(DDD\)', r'example\.com']


def versionados():
    try:
        out = subprocess.run(['git', 'ls-files', '--cached', '--others', '--exclude-standard'], cwd=RAIZ,
                             capture_output=True, text=True, check=True).stdout.split('\n')
        return [f for f in out if f]
    except Exception:
        arquivos = []
        for raiz, dirs, nomes in os.walk(RAIZ):
            dirs[:] = [d for d in dirs if d not in IGNORAR_DIRS]
            arquivos += [os.path.relpath(os.path.join(raiz, n), RAIZ) for n in nomes]
        return arquivos


def checar_frontmatter():
    import glob, json
    erros = []
    for f in sorted(glob.glob(os.path.join(RAIZ, 'skills', '*', 'SKILL.md')) + glob.glob(os.path.join(RAIZ, 'agents', '*.md'))):
        texto = open(f, encoding='utf-8').read()
        m = re.match(r'---\n(.*?)\n---\n', texto, re.S)
        rel = os.path.relpath(f, RAIZ)
        if not m:
            erros.append(f'{rel}: sem frontmatter'); continue
        campos = {l.split(':', 1)[0]: l.split(':', 1)[1].strip() for l in m.group(1).splitlines() if ':' in l and not l.startswith(' ')}
        if not campos.get('name'):
            erros.append(f'{rel}: frontmatter sem name')
        desc = campos.get('description', '')
        try:
            if not (desc.startswith('"') and json.loads(desc)):
                raise ValueError
        except ValueError:
            erros.append(f'{rel}: description precisa estar entre aspas duplas (YAML quebra com ": ")')
    return erros


def main():
    problemas = checar_frontmatter()
    for f in versionados():
        if any(re.search(p, f) for p in PROIBIDOS):
            problemas.append(f'{f}: arquivo que não deve ser versionado')
            continue
        if any(part in IGNORAR_DIRS for part in f.split('/')) or os.path.splitext(f)[1] not in EXTENSOES:
            continue
        if f.endswith('package-lock.json') or f == 'scripts/checar_seguranca.py':
            continue
        try:
            linhas = open(os.path.join(RAIZ, f), encoding='utf-8').read().splitlines()
        except (UnicodeDecodeError, FileNotFoundError):
            continue
        for n, linha in enumerate(linhas, 1):
            for nome, pad in PADROES.items():
                for m in re.finditer(pad, linha):
                    trecho = m.group(0)
                    if any(re.search(p, trecho) or re.search(p, linha) for p in PERMITIDOS):
                        continue
                    problemas.append(f'{f}:{n}: possível {nome}: {trecho[:40]}')
    if problemas:
        print('Encontrei itens para revisar antes de publicar:')
        for p in problemas: print('  -', p)
        sys.exit(1)
    print('OK: nenhum dado pessoal, segredo ou arquivo proibido encontrado.')


if __name__ == '__main__':
    main()
