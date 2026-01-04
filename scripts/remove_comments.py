#!/usr/bin/env python3
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDE_DIRS = {'venv', '.venv', 'node_modules', '.git'}
TEXT_EXTS = ['.py', '.js', '.jsx', '.ts', '.tsx', '.css', '.html']

changed = []

for p in ROOT.rglob('*'):
    if any(part in EXCLUDE_DIRS for part in p.parts):
        continue
    if not p.is_file():
        continue
    if p.suffix.lower() not in TEXT_EXTS:
        continue

    s = p.read_text(encoding='utf-8')
    orig = s

    if p.suffix == '.py':
        s = re.sub(r'(?m)^(?!\s*#\!|\s*#\s*coding)[ \t]*#.*\n', '', s)
        s = re.sub(r"(?m)^\s+\n", "\n", s)
    else:
        s = re.sub(r'(?m)^[ \t]*//.*\n', '', s)
        s = re.sub(r'/\*[\s\S]*?\*/', '', s)
        s = re.sub(r'<!--([\s\S]*?)-->', '', s)
        s = re.sub(r"(?m)^\s+\n", "\n", s)

    if s != orig:
        p.write_text(s, encoding='utf-8')
        changed.append(str(p.relative_to(ROOT)))

print('Modified files:')
for c in changed:
    print(c)
print(f'Total modified: {len(changed)}')
