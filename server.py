"""本地开发服务器 — 支持图片上传到 images/ 文件夹"""
import http.server
import os
import cgi
import json
import urllib.parse

UPLOAD_DIR = 'images'
os.makedirs(UPLOAD_DIR, exist_ok=True)

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path.startswith('/upload'):
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )
            if 'image' not in form:
                self.send_json({'error': 'no image field'}, 400)
                return

            fileitem = form['image']
            filename = form.getvalue('filename', 'image.jpg')
            # Sanitize filename
            safe_name = "".join(c for c in filename if c.isalnum() or c in '._- ')
            if not safe_name:
                safe_name = 'image.jpg'
            filepath = os.path.join(UPLOAD_DIR, safe_name)

            # Avoid overwriting: append number if exists
            base, ext = os.path.splitext(safe_name)
            counter = 1
            while os.path.exists(filepath):
                filepath = os.path.join(UPLOAD_DIR, f"{base}_{counter}{ext}")
                counter += 1

            with open(filepath, 'wb') as f:
                f.write(fileitem.file.read())

            saved_name = os.path.basename(filepath)
            self.send_json({'ok': True, 'filename': saved_name, 'size': os.path.getsize(filepath)})
        else:
            super().do_POST()

    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def log_message(self, format, *args):
        # Quieter logging
        if 'POST' in str(args):
            print(f'  [UPLOAD] {args[0]}')
        else:
            pass  # silence GET logs

if __name__ == '__main__':
    port = 8080
    print(f'Pindou dev server running at http://localhost:{port}')
    print(f'Images saved to: {os.path.abspath(UPLOAD_DIR)}/')
    http.server.HTTPServer(('', port), Handler).serve_forever()
