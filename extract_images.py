"""从 posts.json 中提取所有 base64 图片，保存到 images/ 文件夹，更新 JSON 为文件名引用"""
import json
import os
import re
import sys
import base64

# Fix Windows encoding
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

IMAGES_DIR = 'images'
JSON_PATH = 'posts.json'

os.makedirs(IMAGES_DIR, exist_ok=True)

with open(JSON_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

posts = data.get('posts', data) if isinstance(data, dict) else data
extracted = 0

for post in posts:
    images = post.get('images', [])
    new_images = []
    for idx, img in enumerate(images):
        if isinstance(img, str) and img.startswith('data:'):
            # Parse data URL: data:image/jpeg;base64,xxxx
            match = re.match(r'data:image/(\w+);base64,(.+)', img)
            if match:
                ext = match.group(1)
                if ext == 'jpeg':
                    ext = 'jpg'
                b64_data = match.group(2)
                # Generate filename
                safe_title = re.sub(r'[^\w\s-]', '', post.get('title', 'image'))[:20].strip()
                filename = f"{safe_title}_{idx}.{ext}"
                filepath = os.path.join(IMAGES_DIR, filename)

                # Handle duplicates
                counter = 1
                while os.path.exists(filepath):
                    filename = f"{safe_title}_{idx}_{counter}.{ext}"
                    filepath = os.path.join(IMAGES_DIR, filename)
                    counter += 1

                # Write image file
                try:
                    img_bytes = base64.b64decode(b64_data)
                    with open(filepath, 'wb') as f:
                        f.write(img_bytes)
                    new_images.append(filename)
                    extracted += 1
                    print(f'[OK] {filename} ({len(img_bytes)} bytes)')
                except Exception as e:
                    print(f'[FAIL] {post.get("title")}[{idx}]: {e}')
                    new_images.append(img)  # Keep original if decode fails
            else:
                print(f'[WARN] Skipping malformed data URL: {post.get("title")}[{idx}]')
                new_images.append(img)
        else:
            # Already a filename reference
            new_images.append(img)
    post['images'] = new_images

# Save updated JSON
if isinstance(data, dict) and 'posts' in data:
    data['posts'] = posts
    output = data
else:
    output = data if isinstance(data, list) else posts

with open(JSON_PATH, 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f'\nDone! Extracted {extracted} images to {IMAGES_DIR}/')
print(f'Updated {JSON_PATH} with filename references')
