#!/usr/bin/env python3
"""verify.py: mechanically checks the `path:line` citations of a sumo bout.

Reads the messages (SendMessage) and final reports from the fighters' transcripts. The report is
the SubagentHandback call or, where that tool does not exist, the fighter's last text that starts
with «FINAL REPORT» or contains «Final position» (the Spanish «INFORME FINAL» / «Posición final»
are accepted too). With --text it checks a loose draft, so a fighter validates their citations
before sending them. For every `path:N`, `path:N-M` or `path:N/M` citation:
  1. Resolves the file against the material roots (also by bare file name).
  2. Checks that the cited lines exist.
  3. If the citation carries an attached literal, `path:N → «literal»` (or "literal" / “literal”)
     or `«literal» (path:N)`, checks that the text appears on those lines (±3 tolerance). Only
     literals attached to the citation are taken: quoted text nearby may be a command or a
     citation of another file, and a false accusation is worse than no check.

It does not run commands or judge whether the argument is good: it only says whether the citation
points at something real and whether what the fighter says is there is really there. The referee
still has to read the decisive evidence; this tells them where to start and catches fabrications
at scale.

Usage:
  verify.py --root DIR [--root DIR ...] [--md] ROLE=transcript.output [ROLE=transcript.output ...]
  verify.py --root DIR --text FILE|-        # draft; with «-» it reads standard input

Output: one row per citation and a summary per fighter. Exit code 0, except with --text when
some citation fails (1), so the fighter fixes it before sending.
"""
import argparse
import json
import os
import re
import sys
import unicodedata
from pathlib import Path

CITATION = re.compile(r'(?<![\w/.-])((?:[\w.-]+/)*[\w.-]+\.[A-Za-z]{1,6}):(\d+)(?:\s*[-–/]\s*(\d+))?')
QUOTED = r'(?:«([^»\n]{3,240})»|"([^"\n]{3,240})"|“([^”\n]{3,240})”)'
AFTER = re.compile(r'`?\s*(?:→|->|:|=|—)?\s*' + QUOTED)
BEFORE = re.compile(QUOTED + r'\s*\(\s*`?$')
REPORT = re.compile(r'^\s*\**\s*(FINAL REPORT|INFORME FINAL)|final position|posici[oó]n final', re.I | re.M)
TOLERANCE = 3
SKIP = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', 'dist', 'build'}


def norm(s):
    s = unicodedata.normalize('NFKC', s).lower()
    return re.sub(r'\s+', ' ', s).strip()


def events(role, f):
    out = []
    texts = []
    with open(f, encoding='utf-8', errors='replace') as fh:
        for line in fh:
            try:
                e = json.loads(line)
            except ValueError:
                continue
            if e.get('type') != 'assistant':
                continue
            for c in (e.get('message') or {}).get('content') or []:
                if isinstance(c, dict) and c.get('type') == 'text' and REPORT.search(c.get('text') or ''):
                    texts.append({'role': role, 'ts': e.get('timestamp', ''), 'kind': 'SubagentHandback', 'text': c['text']})
                if isinstance(c, dict) and c.get('type') == 'tool_use' and c.get('name') in ('SendMessage', 'SubagentHandback'):
                    m = (c.get('input') or {}).get('message')
                    if isinstance(m, str):
                        out.append({'role': role, 'ts': e.get('timestamp', ''), 'kind': c['name'], 'text': m})
    if texts and not any(x['kind'] == 'SubagentHandback' for x in out):
        out.append(texts[-1])
    return out


class Index:
    """Resolves cited paths against the roots, also by suffix or file name."""

    def __init__(self, roots):
        self.roots = [Path(r).resolve() for r in roots]
        self.files = []
        for r in self.roots:
            for d, dirs, fs in os.walk(r):
                dirs[:] = [x for x in dirs if x not in SKIP]
                self.files += [Path(d) / x for x in fs]
        self.cache = {}

    def resolve(self, path):
        if path in self.cache:
            return self.cache[path]
        clean = path.lstrip('./')
        cands = []
        p = Path(path)
        if p.is_absolute() and p.is_file():
            cands = [p]
        if not cands:
            cands = [r / clean for r in self.roots if (r / clean).is_file()]
        if not cands:
            suf = '/' + clean
            cands = [f for f in self.files if str(f).endswith(suf)]
        self.cache[path] = cands
        return cands


def read_lines(p, cache={}):
    if p not in cache:
        try:
            cache[p] = Path(p).read_text(encoding='utf-8', errors='replace').split('\n')
        except OSError:
            cache[p] = None
    return cache[p]


def first_group(m):
    return next(g for g in m.groups() if g is not None)


def attached_literals(text, start, end):
    """Literal right after (`path:N → «…»`) or right before (`«…» (path:N)`) the citation."""
    out = []
    m = AFTER.match(text, end)
    if m:
        out.append(first_group(m))
    m = BEFORE.search(text[max(0, start - 260):start])
    if m:
        out.append(first_group(m))
    return out


def check(citation, index):
    cands = index.resolve(citation['path'])
    if not cands:
        return 'NOT_FOUND', None, ''
    a, b = citation['from'], citation['to']
    best = ('OUT_OF_RANGE', cands[0], '')
    for p in cands:
        ls = read_lines(p)
        if ls is None:
            continue
        if a < 1 or b > len(ls):
            continue
        if not citation['literals']:
            return 'EXISTS', p, ''
        zone = norm('\n'.join(ls[max(0, a - 1 - TOLERANCE):b + TOLERANCE]))
        exact = norm('\n'.join(ls[a - 1:b]))
        for lit in citation['literals']:
            n = norm(lit)
            if n in exact:
                return 'LITERAL_OK', p, lit
            if n in zone:
                best = ('LITERAL_SHIFTED', p, lit)
        if best[0] == 'OUT_OF_RANGE':
            best = ('LITERAL_MISSING', p, citation['literals'][0])
    return best


SYMBOL = {
    'LITERAL_OK': '✔ literal on the cited line',
    'LITERAL_SHIFTED': '≈ literal within ±3 lines',
    'EXISTS': '· the line exists (no literal to check)',
    'LITERAL_MISSING': '✘ the quoted text is not there (invented or paraphrased?)',
    'OUT_OF_RANGE': '✘ the file does not have those lines',
    'NOT_FOUND': '✘ the file does not exist',
}
FAILURE = {'LITERAL_MISSING', 'OUT_OF_RANGE', 'NOT_FOUND'}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--root', action='append', required=True, help='material root (repeatable)')
    ap.add_argument('--md', action='store_true', help='Markdown output')
    ap.add_argument('--text', help='checks a draft (file, or «-» for standard input)')
    ap.add_argument('pairs', nargs='*', help='ROLE=transcript.output')
    a = ap.parse_args()
    if not a.pairs and not a.text:
        ap.error('give ROLE=transcript or --text')

    evs = []
    if a.text:
        t = sys.stdin.read() if a.text == '-' else Path(a.text).read_text(encoding='utf-8', errors='replace')
        evs.append({'role': 'DRAFT', 'ts': '', 'kind': 'SendMessage', 'text': t})
    for pair in a.pairs:
        role, _, f = pair.partition('=')
        if not f or not os.path.isfile(f):
            print(f'verify.py: cannot read {pair}', file=sys.stderr)
            continue
        evs += events(role, f)
    evs.sort(key=lambda e: e['ts'])
    index = Index(a.root)

    rows = []
    for i, e in enumerate(evs, 1):
        where = f'{e["role"]} #{i}' if e['kind'] == 'SendMessage' else f'{e["role"]} report'
        for m in CITATION.finditer(e['text']):
            start = int(m.group(2))
            end = int(m.group(3)) if m.group(3) else start
            if end < start:  # «811/828» are two separate lines: the whole span is checked
                start, end = end, start
            citation = {'path': m.group(1), 'from': start, 'to': end,
                        'literals': attached_literals(e['text'], m.start(), m.end())}
            status, p, lit = check(citation, index)
            rows.append({'where': where, 'role': e['role'], 'citation': m.group(0), 'status': status,
                         'file': str(p) if p else '',
                         'literal': lit or (citation['literals'][0] if citation['literals'] else '')})

    roles = sorted({r['role'] for r in rows} | {e['role'] for e in evs})
    summary = []
    for role in roles:
        rr = [r for r in rows if r['role'] == role]
        bad = [r for r in rr if r['status'] in FAILURE]
        ok = [r for r in rr if r['status'] == 'LITERAL_OK']
        summary.append(f'{role}: {len(rr)} citations · {len(ok)} with literal verified · {len(bad)} failed')

    if a.md:
        print('| Where | Citation | Result | Literal |')
        print('|---|---|---|---|')
        for r in rows:
            lit = r['literal'].replace('|', '\\|')[:80]
            print(f'| {r["where"]} | `{r["citation"]}` | {SYMBOL[r["status"]]} | {lit} |')
        print()
        for s in summary:
            print(f'- {s}')
    else:
        for r in rows:
            print(f'{SYMBOL[r["status"]][:1]} {r["where"]:<16} {r["citation"]:<34} {SYMBOL[r["status"]][2:]}'
                  + (f'  «{r["literal"][:70]}»' if r['literal'] else ''))
        print('---')
        for s in summary:
            print(s)
    if not rows:
        print('(no path:line citations in the bout)')
    if a.text:
        if not rows:
            return 0
        no_literal = sum(r['status'] == 'EXISTS' for r in rows)
        if no_literal:
            print(f'Warning: {no_literal} citations without «literal»: add it so they count as verified.')
        return 1 if any(r['status'] in FAILURE for r in rows) else 0
    return 0


if __name__ == '__main__':
    sys.exit(main())
