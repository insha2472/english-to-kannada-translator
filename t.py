#!/usr/bin/env python3
"""
Robust English → Kannada translator (no external packages required).

Features:
- Uses Google's unofficial translate endpoint via urllib (no API key).
- Retries network requests and handles timeouts.
- Falls back to an improved offline dictionary preserving punctuation.
- Simple terminal UI.

Usage: python t.py
"""
import urllib.request
import urllib.parse
import json
import time
import re
import sys


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


def main():
    print('=' * 60)
    print('English → Kannada Translator')
    print('=' * 60)
    print("Type 'exit' to quit. Paste sentences (max ~500 chars).")

    try:
        while True:
            english = input('\nEnglish: ').strip()
            if not english:
                continue
            if english.lower() in ('exit', 'quit'):
                print('Goodbye!')
                break

            kannada = translate(english)
            print('\nKannada:', kannada)
    except (KeyboardInterrupt, EOFError):
        print('\nGoodbye!')


if __name__ == '__main__':
    main()
