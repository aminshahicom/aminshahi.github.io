#!/usr/bin/env python3
"""1) moves images uploaded from the CMS (images/uploads/) into images/<project-id>/ and updates data/projects.json
   2) scans images/<project-id>/ and writes data/gallery.json"""
import json, os, re, shutil, time
EXT = {'.jpg', '.jpeg', '.png', '.webp', '.gif', '.avif'}
UP = 'images/uploads'
nat = lambda s: [int(x) if x.isdigit() else x.lower() for x in re.split(r'(\d+)', s)]

def move(path, pid):
    if not path:
        return path
    src = os.path.join(UP, os.path.basename(path))
    if not os.path.isfile(src):
        return path
    dest = f'images/{pid}'
    os.makedirs(dest, exist_ok=True)
    name = os.path.basename(src)
    if os.path.exists(os.path.join(dest, name)):
        base, ext = os.path.splitext(name)
        name = f'{base}-{int(time.time())}{ext}'
    shutil.move(src, os.path.join(dest, name))
    return f'{dest}/{name}'

if os.path.isfile('data/projects.json'):
    with open('data/projects.json', encoding='utf-8') as fh:
        data = json.load(fh)
    before = json.dumps(data, sort_keys=True)
    for p in data.get('projects', []):
        pid = p.get('id')
        if not pid:
            continue
        p['cover'] = move(p.get('cover', ''), pid)
        p['images'] = [move(x, pid) for x in p.get('images', [])]
    if json.dumps(data, sort_keys=True) != before:
        with open('data/projects.json', 'w', encoding='utf-8') as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)

out = {}
for pid in sorted(os.listdir('images')) if os.path.isdir('images') else []:
    d = os.path.join('images', pid)
    if pid == 'uploads' or not os.path.isdir(d):
        continue
    files = sorted((f for f in os.listdir(d) if os.path.splitext(f)[1].lower() in EXT), key=nat)
    if files:
        out[pid] = [f'images/{pid}/{f}' for f in files]
os.makedirs('data', exist_ok=True)
with open('data/gallery.json', 'w', encoding='utf-8') as fh:
    json.dump(out, fh, ensure_ascii=False, indent=2)
print(f'{sum(len(v) for v in out.values())} images in {len(out)} projects')
