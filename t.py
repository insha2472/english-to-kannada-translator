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
import requests
import json

def translate_to_kannada(english_text):
    """
    Translate English to Kannada using Google Translate API
    Supports any word or phrase
    """
    try:
        # Using free Google Translate API endpoint
        url = "https://translate.googleapis.com/translate_a/element.js?cb=googleTranslateElementInit"
        
        # Alternative: Using Google's simple translation endpoint
        params = {
            'client': 'gtx',
            'sl': 'en',
            'tl': 'kn',
            'dt': 't',
            'q': english_text
        }
        
        response = requests.get(
            'https://translate.googleapis.com/translate_a/single',
            params=params,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        
        if response.status_code == 200:
            result = response.json()
            kannada_text = result[0][0][0]
            return kannada_text
        else:
            return english_text
            
    except Exception as e:
        print(f"Translation error: {e}")
        # Fallback to basic dictionary
        return translate_with_fallback(english_text)

def translate_with_fallback(english_text):
    """Fallback translation using basic dictionary"""
    translation_dict = {
        'hello': 'ನಮಸ್ಕಾರ',
        'good morning': 'ಶುಭೋದಯ',
        'good night': 'ಶುಭರಾತ್ರಿ',
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
        'good': 'ಒಳ್ಳೆಯ',
        'bad': 'ಕೆಟ್ಟ',
        'person': 'ವ್ಯಕ್ತಿ',
        'name': 'ಹೆಸರು',
        'house': 'ಮನೆ',
    }
    
    english_text = english_text.lower().strip()
    
    if english_text in translation_dict:
        return translation_dict[english_text]
    
    words = english_text.split()
    translated_words = []
    
    for word in words:
        if word in translation_dict:
            translated_words.append(translation_dict[word])
        else:
            translated_words.append(word)
    
    return ' '.join(translated_words)

# Main Program
print("=" * 60)
print("English to Kannada Translator (Online)")
print("=" * 60)
print("Type 'exit' to quit\n")

while True:
    english_text = input("English: ")
    
    if english_text.lower() == 'exit':
        print("Thank you!")
        break
    
    if english_text.strip():
        kannada_text = translate_to_kannada(english_text)
        print(f"Kannada: {kannada_text}\n")
