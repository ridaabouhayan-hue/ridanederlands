import json
import urllib.request
import urllib.parse
import time
import sys
import os

def translate_text(text, target_lang, source_lang='nl'):
    """Vertaalt tekst via de gratis Google Translate web API."""
    if not text.strip():
        return text
    url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={source_lang}&tl={target_lang}&dt=t&q={urllib.parse.quote(text)}"
    
    for _ in range(3):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode())
                translated = ''.join([sentence[0] for sentence in result[0]])
                return translated
        except Exception as e:
            time.sleep(1)
    print(f"Waarschuwing: Vertaling mislukt voor '{text}' naar {target_lang}")
    return text

def process_dictionary(filepath, target_languages):
    """Leest een JSON woordenboek en vertaalt alle ontbrekende talen gebaseerd op 'nl'."""
    if not os.path.exists(filepath):
        print(f"Fout: Bestand {filepath} bestaat niet.")
        return

    print(f"Bestand {filepath} laden...")
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print("Fout: Bestand is geen geldige JSON. Zorg ervoor dat het een .json bestand is met geldige syntax.")
            return

    changes_made = 0
    total_keys = len(data)

    print(f"{total_keys} sleutels gevonden. Controleren op ontbrekende vertalingen...")

    for key, translations in data.items():
        if 'nl' not in translations:
            print(f"Waarschuwing: Geen Nederlandse ('nl') tekst gevonden voor sleutel '{key}'. Overslaan.")
            continue
            
        nl_text = translations['nl']
        
        for lang in target_languages:
            if lang not in translations or not translations[lang].strip():
                print(f"Vertalen: '{key}' naar {lang}...")
                translated = translate_text(nl_text, lang)
                translations[lang] = translated
                changes_made += 1

    if changes_made > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Klaar! {changes_made} vertalingen toegevoegd en opgeslagen in {filepath}.")
    else:
        print("Geen ontbrekende vertalingen gevonden. Alles is al up-to-date!")

if __name__ == "__main__":
    print("NT2 Vertaal Assistent")
    print("---------------------")
    if len(sys.argv) < 3:
        print("Gebruik: python vertaler.py <bestand.json> <taal1,taal2,taal3>")
        print("Voorbeeld: python vertaler.py woordenboek.json en,tr,ar,ps,da,fa,vi")
    else:
        file_path = sys.argv[1]
        langs = sys.argv[2].split(',')
        process_dictionary(file_path, langs)
