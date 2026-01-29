#!/usr/bin/env python3
"""
Robust English → Kannada translator Flask web app (no external packages required).

Features:
- Uses Google's unofficial translate endpoint via urllib (no API key).
- Retries network requests and handles timeouts.
- Falls back to an improved offline dictionary preserving punctuation.
- Flask web UI.

Usage: python t.py
"""
import urllib.request
import urllib.parse
import json
import time
import re
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse


def translate_online(text, retries=2, timeout=6):
    """Attempt online translation using Google's free endpoint.

    Returns translated text on success, or raises an exception on failure.
    """
    if not text:
        return ""

    params = urllib.parse.urlencode({
        'client': 'gtx',
        'sl': 'en',
        'tl': 'kn',
        'dt': 't',
        'q': text,
    })

    url = f'https://translate.googleapis.com/translate_a/single?{params}'

    last_exc = None
    for attempt in range(1, retries + 1):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read().decode('utf-8')
            data = json.loads(raw)
            # The response structure is nested lists: [[['translated', 'source', ...], ...], ...]
            return data[0][0][0]
        except Exception as e:
            last_exc = e
            time.sleep(0.4 * attempt)
            continue

    raise last_exc


def translate_with_fallback(text):
    """Fallback translator using a dictionary and simple tokenization.

    This preserves punctuation and unknown words.
    """
    if not text:
        return ""

    # Improved dictionary (extend as needed)
    d = {
        'hello': 'ನಮಸ್ಕಾರ',
        'hi': 'ಹಲೋ',
        'good': 'ಒಳ್ಳೆಯ',
        'morning': 'ಬೆಳಗ್ಗೆ',
        'good morning': 'ಶುಭೋದಯ',
        'night': 'ರಾತ್ರಿ',
        'good night': 'ಶುಭರಾತ್ರಿ',
        'thank': 'ಧನ್ಯ',
        'thank you': 'ಧನ್ಯವಾದ',
        'please': 'ದಯವಿಟ್ಟು',
        'yes': 'ಹೌದು',
        'no': 'ಇಲ್ಲ',
        'water': 'ನೀರು',
        'food': 'ಆಹಾರ',
        'friend': 'ಸ್ನೇಹಿತ',
        'family': 'ಕುಟುಂಬ',
        'love': 'ಪ್ರೀತಿ',
        'happy': 'ಸುಖ',
        'sad': 'ದುಃಖ',
        'help': 'ಸಹಾಯ',
        'house': 'ಮನೆ',
        'name': 'ಹೆಸರು',
        'person': 'ವ್ಯಕ್ತಿ',
        'i': 'ನಾನು',
        'you': 'ನೀವು',
        'we': 'ನಾವು',
        'they': 'ಅವರು',
        'he': 'ಅವನು',
        'she': 'ಅವಳು',
        'is': 'ಆಗಿದೆ',
        'are': 'ಇವೆ',
        'am': 'ನಾನು',
    }

    text_lower = text.lower()

    # Try exact phrase match first
    if text_lower in d:
        return d[text_lower]

    # Tokenize into words and punctuation
    tokens = re.findall(r"\w+|[^\t\w\s]", text, flags=re.UNICODE)
    out_tokens = []

    for tok in tokens:
        key = tok.lower()
        if key in d:
            out_tokens.append(d[key])
        else:
            out_tokens.append(tok)

    # Join with space but avoid space before punctuation
    result = ''
    for i, t in enumerate(out_tokens):
        if i > 0 and not re.match(r"[.,!?;:%)\]]", t):
            result += ' '
        result += t

    return result


def translate(text):
    """Translate using online then fallback gracefully."""
    try:
        return translate_online(text)
    except Exception:
        return translate_with_fallback(text)


class TranslatorHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            # Read and serve the HTML file content
            try:
                with open('t.html', 'r', encoding='utf-8') as f:
                    html_content = f.read()
                self.wfile.write(html_content.encode('utf-8'))
            except FileNotFoundError:
                # Fallback HTML if t.html not found
                html = '''
<!DOCTYPE html>
<html>
<head><title>English → Kannada Translator</title></head>
<body>
<h1>English → Kannada Translator</h1>
<p>Error: t.html file not found. Please ensure t.html is in the same directory.</p>
</body>
</html>'''
                self.wfile.write(html.encode())
        elif self.path == '/translate':
            # Handle AJAX translation requests
            self.send_response(405)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"error": "Use POST method"}')
    
    def do_POST(self):
        if self.path == '/translate':
            # Handle AJAX translation requests from the HTML
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            
            try:
                import json
                data = json.loads(post_data)
                text = data.get('text', '')
                kannada = translate(text) if text else ''
                
                response = {'translation': kannada}
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
        else:
            # Handle form submissions (fallback)
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            params = parse_qs(post_data)
            text = params.get('text', [''])[0]
            
            kannada = translate(text) if text else ''
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = f'''
<!DOCTYPE html>
<html>
<head><title>English → Kannada Translator</title></head>
<body>
<h1>English → Kannada Translator</h1>
<form method="post">
<textarea name="text" rows="4" cols="50">{text}</textarea><br><br>
<button type="submit">Translate</button>
</form>
<h2>Translation:</h2>
<p style="font-size:18px;">{kannada}</p>
</body>
</html>'''
            self.wfile.write(html.encode())

def main():
    port = 5000
    server = HTTPServer(('0.0.0.0', port), TranslatorHandler)
    print(f'English → Kannada Translator running at: http://localhost:{port}')
    print('Press Ctrl+C to stop')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nServer stopped')
        server.server_close()


if __name__ == '__main__':
    main()
