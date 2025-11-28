with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

total = len(lines)
print(f'Total lines: {total}')

# 找到</style>的位置
style_end = [i+1 for i, line in enumerate(lines) if '</style>' in line]
print(f'</style> at lines: {style_end[-3:] if len(style_end) >= 3 else style_end}')

# 找到</body>的位置  
body_end = [i+1 for i, line in enumerate(lines) if '</body>' in line]
print(f'</body> at line: {body_end[0] if body_end else "Not found"}')

# 显示</body>前的几行
if body_end:
    print(f'\n</body> before 5 lines:')
    for i in range(body_end[0] - 6, body_end[0] - 1):
        print(f'{i+1}: {lines[i].rstrip()[:80]}')

