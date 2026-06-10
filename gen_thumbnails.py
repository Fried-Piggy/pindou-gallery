"""批量生成缩略图——每次 push 前运行一次即可"""
from PIL import Image
import os, sys

SRC = 'images'
THUMB = os.path.join(SRC, 'thumbnails')
os.makedirs(THUMB, exist_ok=True)

count = 0
for fname in os.listdir(SRC):
    if not fname.lower().endswith(('.jpg','.jpeg','.png','.webp')):
        continue
    fpath = os.path.join(SRC, fname)
    tpath = os.path.join(THUMB, fname)
    if os.path.exists(tpath):
        continue
    try:
        img = Image.open(fpath)
        w, h = img.size
        ratio = min(400 / w, 400 / h)
        if ratio < 1:
            img = img.resize((int(w * ratio), int(h * ratio)), Image.LANCZOS)
        img.convert('RGB').save(tpath, 'JPEG', quality=70, optimize=True)
        count += 1
        print(f'  {fname}')
    except Exception as e:
        print(f'  FAIL {fname}: {e}', file=sys.stderr)

print(f'\nDone: {count} thumbnails')
