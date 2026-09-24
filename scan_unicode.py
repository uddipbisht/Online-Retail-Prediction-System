import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

files = [
    'train_models.py',
    'backend/app.py',
    'backend/ml_model.py',
    'frontend/streamlit_app.py',
]

for fpath in files:
    print(f'\n=== {fpath} ===')
    with open(fpath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for i, line in enumerate(lines, 1):
        non_ascii = [(j, hex(ord(c)), c) for j, c in enumerate(line) if ord(c) > 127]
        if non_ascii:
            safe_line = line.rstrip().encode('ascii', 'replace').decode()
            print(f'  Line {i:3d}: {safe_line[:100]}')
            for pos, code, ch in non_ascii:
                print(f'           pos={pos} code={code} name={ch.encode("unicode_escape").decode()}')
