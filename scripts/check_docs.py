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
mastery_counts = {'00-ROADMAP.md':17, '05-UBUNTU-STEP-BY-STEP.md':17, '06-CRYPTO-AGENT-SCOPE.md':6}
for name, expected_count in mastery_counts.items():
    content = (root/name).read_text(encoding='utf-8')
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

# 所有Markdown表格都检查列宽，不只检查操作指南。
for path in markdown:
    in_code = False
    widths = []
    for line in path.read_text(encoding='utf-8').splitlines()+['']:
        if line.startswith('```'):
            in_code = not in_code
        if not in_code and line.startswith('|'):
            widths.append(len(re.split(r'(?<!\\)\|',line))-2)
        elif widths:
            if len(set(widths)) != 1:
                failures.append(f'{path.name}: inconsistent table columns')
            widths = []


for path in markdown:
    if re.search(r'^\|[-: |]+\|\n\s*\n\|',path.read_text(encoding='utf-8'),re.M):
        failures.append(f'{path.name}: table body detached by blank line')

roadmap = (root/'00-ROADMAP.md').read_text(encoding='utf-8')
goal_sections = re.findall(r'^### (目标\d+|Phase 0)：[^\n]+\n(.*?)(?=^### |^## |\Z)', roadmap, re.M|re.S)
if {title for title, _ in goal_sections} != {'Phase 0'} | {f'目标{i}' for i in range(1,17)}:
    failures.append('roadmap: Phase 0 or one of 16 goals missing/duplicated')
if len(goal_sections) != 17:
    failures.append('roadmap: unexpected number of goal sections')
for title, content in goal_sections:
    for required in ('**进入条件**', '**Agent目标**', '**技术点掌握程度标准**',
                     '**学习与实现顺序**', '**必须独立回答**', '**独立练习**', '**退出条件**'):
        if required not in content:
            failures.append(f'roadmap: {title} missing {required}')
    if '| 技术点 | 能解释 | 独立做到 | 排错与边界 | 验收证据 | 后置内容 |' not in content:
        failures.append(f'roadmap: {title} missing mastery dimensions')

    block = re.search(r'\| 技术点 \| 能解释 .*?\n\|[-|]+\|\n((?:\|[^\n]*\n)+)',content)
    if not block or len(block.group(1).splitlines()) < 4:
        failures.append(f'roadmap: {title} mastery body is missing or detached from header')

for name in ('07-AGENT-SYSTEM-DESIGN.md','08-API-AND-WEB.md','09-DELIVERY-AND-ACCEPTANCE.md'):
    if not (root/name).is_file():
        failures.append(f'missing supporting guide {name}')
    if name not in (root/'README.md').read_text(encoding='utf-8'):
        failures.append(f'README: guide not indexed {name}')


# 交付阶段是唯一时间路径；技术卡与任务编号是稳定索引。
plan = json.loads((root/'learning-plan.json').read_text(encoding='utf-8'))
expected_stage_ids = [f'V{i}' for i in range(7)]
stages = plan['stages']
stage_ids = [stage['id'] for stage in stages]
if stage_ids != expected_stage_ids:
    failures.append('plan: delivery order must be V0 through V6')
if plan['weekly_hours'] != [20,25] or plan['baseline_hours'] != 450:
    failures.append('plan: weekly or total learning budget drift')
if sum(stage['hours'] for stage in stages) != plan['baseline_hours']:
    failures.append('plan: stage budgets do not sum to baseline')
if sum(plan['goal_hours'].values()) != plan['baseline_hours']:
    failures.append('plan: goal budgets do not sum to baseline')
if set(plan['goal_hours']) != {str(i) for i in range(17)} | {'integration'}:
    failures.append('plan: missing goal budget')
for stage in stages:
    if sum(stage['alloc'].values()) != stage['hours']:
        failures.append(f"plan: {stage['id']} allocation sum differs from stage budget")
    if set(stage['alloc']) - set(plan['goal_hours']):
        failures.append(f"plan: {stage['id']} has unknown goal")
for goal, hours in plan['goal_hours'].items():
    if sum(stage['alloc'].get(goal,0) for stage in stages) != hours:
        failures.append(f'plan: goal {goal} double-counted or missing allocation')
headers = re.findall(r'^### (目标\d+|Phase 0)：[^\n]*（(\d+)h）',roadmap,re.M)
for title,hours in headers:
    goal = '0' if title == 'Phase 0' else title.removeprefix('目标')
    if plan['goal_hours'].get(goal) != int(hours):
        failures.append(f'plan: {title} budget differs from goal card')
if re.findall(r'^## \d+\. (V\d)：',roadmap,re.M) != expected_stage_ids:
    failures.append('roadmap: delivery chapters not in V0-V6 order')
step_text = (root/'05-UBUNTU-STEP-BY-STEP.md').read_text(encoding='utf-8')
if re.findall(r'^## \d+ (V\d) ',step_text,re.M) != expected_stage_ids:
    failures.append('steps: delivery chapters not in V0-V6 order')
detail_task_ids = []
for line in step_text.splitlines():
    match = re.match(r'^\| (M[1-6] \d{2}) \|',line)
    if match and len(re.split(r'(?<!\\)\|',line))-2 == 4:
        detail_task_ids.append(match.group(1))
if len(detail_task_ids) != 81 or len(set(detail_task_ids)) != 81:
    failures.append('steps: must retain 81 unique four-column detailed task rows')
expected_tasks = set(detail_task_ids) | {f'P0 {i:02}' for i in range(1,6)}
if set(plan['task_stages']) != expected_tasks:
    failures.append('plan: task navigation differs from detailed guide')
nav_ids = re.findall(r'^\| ((?:P0|M[1-6]) \d{2}) \| V\d \| V\d \|$',step_text,re.M)
if len(nav_ids) != 86 or set(nav_ids) != expected_tasks:
    failures.append('steps: task navigation must cover all 86 task entrances')
for task, mapping in plan['task_stages'].items():
    first, finish = mapping['first_stage'], mapping['finish_stage']
    if first not in stage_ids or finish not in stage_ids:
        failures.append(f'plan: {task} unknown stage')
    elif stage_ids.index(first) > stage_ids.index(finish):
        failures.append(f'plan: {task} finishes before first learning slice')
    if f'| {task} | {first} | {finish} |' not in step_text:
        failures.append(f'plan: {task} stage mapping differs from guide')
for name in ('00-ROADMAP.md','03-LEARNING-ORDER.md','05-UBUNTU-STEP-BY-STEP.md'):
    content = (root/name).read_text(encoding='utf-8')
    cumulative = 0
    for stage in stages:
        cumulative += stage['hours']
        row = f"| {stage['id']} {stage['name']} | {stage['hours']}h | {cumulative}h |"
        if row not in content:
            failures.append(f'{name}: stage budget/cumulative table differs for {stage["id"]}')
for name in ('00-ROADMAP.md','03-LEARNING-ORDER.md'):
    content=(root/name).read_text(encoding='utf-8')
    for goal,hours in plan['goal_hours'].items():
        label='Phase 0' if goal=='0' else ('综合验收' if goal=='integration' else '目标'+goal)
        alloc=[f"{s['id']} {s['alloc'][goal]}h" for s in stages if goal in s['alloc']]
        row=f"| {label} | {hours}h | {'；'.join(alloc)} | {alloc[-1].split()[0]} |"
        if row not in content:
            failures.append(f'{name}: goal slice table differs for {goal}')
print('Checked V0-V6 order, 450h stage/goal allocation, 81 detailed task rows and 86 navigation entries.')

print(f'Checked {len(markdown)} Markdown files, {links} local links, {python_blocks} Python examples, {json_blocks} JSON examples, {len(tables)} DDL table dependencies, {len(files)} synthetic file sizes, {len(tools)} canonical tools and {sum(mastery_counts.values())} mastery tables.')
for failure in failures:print('ERROR',failure)
if failures:raise SystemExit(1)
print('PASS static documentation checks (does not execute PostgreSQL or GPU code).')
