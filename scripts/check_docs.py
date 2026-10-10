from pathlib import Path
import ast
import json
import re
import hashlib

root = Path(__file__).resolve().parents[1]
failures = []
markdown = sorted(root.rglob('*.md'))
python_blocks = 0
json_blocks = 0
links = 0
for path in markdown:
    text = path.read_text(encoding='utf-8')
    if text.count('```') % 2:
        failures.append(f'{path.name}: unbalanced fenced code blocks')
    for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', text):
        if re.match(r'^[a-z]+://', target) or target.startswith('#'):
            continue
        target = target.split('#',1)[0].strip('<>')
        links += 1
        if not (path.parent/target).is_file():
            failures.append(f'{path.name}: missing local link {target}')
    for lang,code in re.findall(r'```([^\n]*)\n(.*?)```',text,re.S):
        if lang.strip() == 'python':
            python_blocks += 1
            try:ast.parse(code)
            except SyntaxError as exc:failures.append(f'{path.name}: invalid Python example {exc}')
        if lang.strip() == 'json':
            json_blocks += 1
            try:json.loads(code)
            except ValueError as exc:failures.append(f'{path.name}: invalid JSON example {exc}')
for path in root.rglob('*.json'):
    json.loads(path.read_text(encoding='utf-8'))

ddl_text = (root/'repo-structure.md').read_text(encoding='utf-8')
ddl = re.search(r'```sql\n(.*?)```',ddl_text,re.S).group(1)
tables = []
for match in re.finditer(r'CREATE TABLE (\w+) \((.*?)\n\);',ddl,re.S):
    name,body=match.groups()
    for ref in re.findall(r'REFERENCES (\w+)\(',body):
        if ref not in tables and ref != name:
            failures.append(f'DDL: {name} references {ref} before creation')
    tables.append(name)
if "DEFAULT 'user'" in ddl or "DEFAULT 'viewer'" not in ddl:
    failures.append('DDL: role default regression')
if not re.search(r'CREATE UNIQUE INDEX idx_memories_active_hash',ddl):
    failures.append('DDL: active memory dedup not unique')
if 'runtime_config JSONB NOT NULL' not in ddl:
    failures.append('DDL: missing config snapshot column')

fixtures = json.loads((root/'eval/fixtures.json').read_text(encoding='utf-8'))
experiments = next(f['data']['experiments'] for f in fixtures['fixtures'] if f['id']=='experiments_sample')
expected_bytes = {'100MB':100_000_000,'500MB':500_000_000,'1GB':1_000_000_000}
for row in experiments:
    if row['data_bytes'] != expected_bytes[row['data_scale']]:
        failures.append('fixture: inconsistent SI bytes')
lookup = {(r['data_scale'],r['metric']):r['value'] for r in experiments}
if abs(lookup['500MB','audit_time']-lookup['100MB','audit_time']-7.13)>1e-9:
    failures.append('fixture: time difference wrong')
print(f'Checked {len(markdown)} Markdown files, {links} local links, {python_blocks} Python examples, {json_blocks} JSON examples, {len(tables)} DDL table dependencies, {len(experiments)} SI-unit fixture rows.')
for failure in failures:print('ERROR',failure)
if failures:raise SystemExit(1)
print('PASS static documentation checks (does not execute PostgreSQL or GPU code).')
