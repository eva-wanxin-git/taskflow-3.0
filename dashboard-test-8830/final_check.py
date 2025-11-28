import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

modules = [
    ('architect-module', '架构师'),
    ('engineer-module', '全栈工程师'),
    ('memory-space-module', '记忆空间'),
    ('pulse-module', '实时脉动'),
    ('devops-module', '运维工程师'),
    ('code-manager-module', 'Noah')
]

print("=== CSS Final Check ===\n")

for m, name in modules:
    match = re.search(rf'\.{m}\s*{{([^}}]{{500}})', content, re.DOTALL)
    if match:
        css = match.group(1)
        has_max_width = '1600px' in css
        has_margin = '64px auto 48px auto' in css
        
        status = 'OK' if (has_max_width and has_margin) else 'ERROR'
        print(f'{name:12s}: max-width={has_max_width}, margin={has_margin} - {status}')
    else:
        print(f'{name:12s}: NOT FOUND')

