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
fixture_map = {item['id']:item for item in fixtures['fixtures']}
files = fixture_map['small_files_sample']['data']['files']
for item in files:
    if len(item['content_utf8'].encode('utf-8')) != item['size_bytes']:
        failures.append('fixture: UTF-8 file size mismatch')
keys = fixture_map['key_metadata_sample']['data']['keys']
if any('material' in item or 'private_key' in item for item in keys):
    failures.append('fixture: key metadata contains secret material')
if not fixture_map['certificate_draft']['resolved'] and fixture_map['certificate_draft']['data']['path'] is not None:
    failures.append('fixture: unresolved certificate unexpectedly has a live path')
schema = json.loads((root/'eval/dataset.schema.json').read_text(encoding='utf-8'))
tools = set(schema['properties']['allowed_tool_plans']['items']['items']['enum'])
canonical = re.search(r'canonical tools：(.*?)。', ddl_text).group(1)
if set(canonical.split('、')) != tools:
    failures.append('schema: canonical tools differ from project engineering contract')
for name in ('files','crypto_keys','key_versions','certificates','artifacts'):
    if name not in tables:
        failures.append(f'DDL: missing crypto resource table {name}')
for name in ('05-UBUNTU-STEP-BY-STEP.md','06-CRYPTO-AGENT-SCOPE.md'):
    content = (root/name).read_text(encoding='utf-8')
    expected_count = 17 if name.startswith('05') else 6
    if content.count('**技术点掌握程度标准**') != expected_count:
        failures.append(f'{name}: mastery table coverage mismatch')
    in_code = False
    widths = []
    for line in content.splitlines()+['']:
        if line.startswith('```'):
            in_code = not in_code
        if not in_code and line.startswith('|'):
            widths.append(len(re.split(r'(?<!\\)\|',line))-2)
        elif widths:
            if len(set(widths)) != 1:
                failures.append(f'{name}: inconsistent table columns')
            widths = []
print(f'Checked {len(markdown)} Markdown files, {links} local links, {python_blocks} Python examples, {json_blocks} JSON examples, {len(tables)} DDL table dependencies, {len(files)} synthetic file sizes, {len(tools)} canonical tools and 23 mastery tables.')
for failure in failures:print('ERROR',failure)
if failures:raise SystemExit(1)
print('PASS static documentation checks (does not execute PostgreSQL or GPU code).')
