#!/usr/bin/env python3
"""Scans images/<project-id>/ and writes data/gallery.json  ({project-id: [files...]})."""
import json, os, re
EXT = {'.jpg', '.jpeg', '.png', '.webp', '.gif', '.avif'}
nat = lambda s: [int(x) if x.isdigit() else x.lower() for x in re.split(r'(\d+)', s)]
out = {}
if os.path.isdir('images'):
    for pid in sorted(os.listdir('images')):
        d = os.path.join('images', pid)
        if not os.path.isdir(d):
            continue
        files = sorted((f for f in os.listdir(d) if os.path.splitext(f)[1].lower() in EXT), key=nat)
        if files:
            out[pid] = [f'images/{pid}/{f}' for f in files]
os.makedirs('data', exist_ok=True)
with open('data/gallery.json', 'w', encoding='utf-8') as fh:
    json.dump(out, fh, ensure_ascii=False, indent=2)
print(f'{sum(len(v) for v in out.values())} images in {len(out)} projects')
