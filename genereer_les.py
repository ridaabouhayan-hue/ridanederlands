import os
import sys
import json
import requests
import time
import re
import google.generativeai as genai
from pydub import AudioSegment

GEMINI_API_FILE = "API.txt"
ELEVEN_API_FILE = "API_ELEVENLABS.txt"
VOICES_FILE = "stemmen.json"

OUTPUT_DIR = "Luisterlessen"
AUDIO_DIR = os.path.join(OUTPUT_DIR, "audio")
DATA_FILE = os.path.join(OUTPUT_DIR, "data.json")
TEMP_DIR = "temp_audio"

def load_gemini_key():
    if not os.path.exists(GEMINI_API_FILE):
        print(f"Fout: {GEMINI_API_FILE} niet gevonden.")
        sys.exit(1)
    with open(GEMINI_API_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith("GEMINI_API_KEY="):
                return line.split("=", 1)[1].strip()
    print("Fout: GEMINI_API_KEY niet gevonden in API.txt.")
    sys.exit(1)

def load_eleven_key():
    if not os.path.exists(ELEVEN_API_FILE):
        print(f"Fout: {ELEVEN_API_FILE} niet gevonden.")
        print("Maak dit bestand aan en zet hier puur je ElevenLabs API key in.")
        sys.exit(1)
    with open(ELEVEN_API_FILE, 'r', encoding='utf-8') as f:
        return f.read().strip()

def load_voices():
    if not os.path.exists(VOICES_FILE):
        dummy_data = {
            "Vrouw": "vul_hier_vrouwen_voice_id_in",
            "Man": "vul_hier_mannen_voice_id_in"
        }
        with open(VOICES_FILE, 'w', encoding='utf-8') as f:
            json.dump(dummy_data, f, indent=4)
        print(f"Bestand {VOICES_FILE} aangemaakt. Vul hier eerst je Voice ID's in voor 'Man' en 'Vrouw'!")
        sys.exit(1)
        
    with open(VOICES_FILE, 'r', encoding='utf-8') as f:
        voices = json.load(f)
        
    for k, v in voices.items():
        if "vul_hier" in v:
            print(f"Let op: Voice ID voor {k} is nog niet ingevuld in {VOICES_FILE}.")
            sys.exit(1)
            
    return voices

def genereer_les_data(prompt, niveau, gemini_key):
    print("1. AI aan het werk zetten via Gemini...")
    genai.configure(api_key=gemini_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    systeem_prompt = f"""Je bent een expert in het schrijven van lesmateriaal voor NT2 (Nederlands als tweede taal).
Schrijf een extreem simpele conversatie op ERK-niveau {niveau} over het volgende onderwerp/situatie: "{prompt}".

Regels:
- Kies zelf twee unieke en veelvoorkomende namen (bijv. 1 man en 1 vrouw).
- Voor niveau A1: Gebruik zinnen van max 8 woorden, basiswoordenschat, geen moeilijke bijzinnen.
- Voor niveau A2: Iets langer, maar nog steeds eenvoudig.
- Schrijf exact 8 tot 10 regels dialoog in totaal.
- Bedenk daarnaast 3 multiple choice luistervragen over dit gesprek (3 opties per vraag, en geef het juiste antwoord-index, beginnend bij 0).

Je MOET je antwoord geven in puur JSON formaat. Geen markdown block (```json), geen extra tekst. Alleen de JSON. Gebruik exact dit format:
{{
  "thema": "Een korte titel van het gesprek",
  "niveau": "{niveau}",
  "sprekers": {{
    "naam_persoon_1": {{"geslacht": "vrouw"}},
    "naam_persoon_2": {{"geslacht": "man"}}
  }},
  "conversatie": [
    {{"speaker": "naam_persoon_1", "text": "Hallo, hoe gaat het?"}},
    {{"speaker": "naam_persoon_2", "text": "Goed, en met jou?"}}
  ],
  "vragen": [
    {{
      "vraag": "Hoe gaat het met persoon 2?",
      "opties": ["Slecht", "Goed", "Hij is ziek"],
      "antwoord_index": 1
    }}
  ]
}}
"""

    response = model.generate_content(systeem_prompt)
    
    ruwe_tekst = response.text.strip()
    if ruwe_tekst.startswith("```json"):
        ruwe_tekst = ruwe_tekst[7:]
    if ruwe_tekst.startswith("```"):
        ruwe_tekst = ruwe_tekst[3:]
    if ruwe_tekst.endswith("```"):
        ruwe_tekst = ruwe_tekst[:-3]
        
    ruwe_tekst = ruwe_tekst.strip()
    
    try:
        data = json.loads(ruwe_tekst)
        return data
    except json.JSONDecodeError as e:
        print(f"Fout: Gemini gaf geen geldig JSON formaat terug: {e}")
        print("Ruwe tekst was:")
        print(ruwe_tekst)
        sys.exit(1)

def genereer_audio_elevenlabs(text, voice_id, api_key, output_path):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            f.write(response.content)
        return True
    else:
        print(f"ElevenLabs Error: {response.text}")
        return False

def opslaan_in_database(les_data):
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            try:
                db = json.load(f)
            except json.JSONDecodeError:
                db = []
    else:
        db = []
        
    # Genereer unieke id
    les_data['id'] = f"{les_data['niveau'].lower()}_{int(time.time())}"
    db.append(les_data)
    
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(db, f, indent=4)
        
    return les_data['id']

def main():
    if len(sys.argv) < 3:
        print("Gebruik: python genereer_les.py \"Onderwerp\" \"Niveau\"")
        print("Bijvoorbeeld: python genereer_les.py \"in de supermarkt\" \"A1\"")
        prompt = input("Waar wil je een les over genereren? Typ het onderwerp: ")
        niveau = input("Op welk niveau? (bijv. A1 of A2): ").upper()
    else:
        prompt = sys.argv[1]
        niveau = sys.argv[2].upper()
        
    gemini_key = load_gemini_key()
    eleven_key = load_eleven_key()
    voices = load_voices()
    
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)
    if not os.path.exists(AUDIO_DIR):
        os.makedirs(AUDIO_DIR)
        
    # 1. Genereer lesdata met Gemini
    les_data = genereer_les_data(prompt, niveau, gemini_key)
    titel = les_data['thema']
    print(f"\n✅ Les gegenereerd: [{niveau}] {titel}")
    
    # Koppel namen aan Voice IDs o.b.v. geslacht
    speaker_to_voiceid = {}
    for naam, info in les_data['sprekers'].items():
        geslacht = info.get('geslacht', 'vrouw').lower()
        if 'man' in geslacht and not 'vrouw' in geslacht:
            speaker_to_voiceid[naam] = voices.get('Man')
        else:
            speaker_to_voiceid[naam] = voices.get('Vrouw')
            
        if not speaker_to_voiceid[naam]:
            print(f"Fout: Geen voice_id gevonden in stemmen.json voor geslacht '{geslacht}' (Speaker {naam}).")
            sys.exit(1)

    # 2. Genereer audio met ElevenLabs
    print("\n2. Audio genereren via ElevenLabs...")
    audio_segments = []
    silence = AudioSegment.silent(duration=500) # 0.5 seconde stilte
    
    conversatie = les_data['conversatie']
    for i, zin in enumerate(conversatie):
        speaker = zin['speaker']
        text = zin['text']
        voice_id = speaker_to_voiceid.get(speaker)
        
        temp_file = os.path.join(TEMP_DIR, f"line_{i}.mp3")
        print(f"   Spraak ophalen voor regel {i+1} ({speaker})...")
        
        if genereer_audio_elevenlabs(text, voice_id, eleven_key, temp_file):
            seg = AudioSegment.from_mp3(temp_file)
            if audio_segments:
                audio_segments.append(silence)
            audio_segments.append(seg)
        else:
            print("Gestopt wegens API fout.")
            sys.exit(1)
            
        time.sleep(0.5)
        
    # 3. Audio samenvoegen
    print("\n3. Audio samenvoegen...")
    combined = AudioSegment.empty()
    for seg in audio_segments:
        combined += seg
        
    slug = re.sub(r'[^a-zA-Z0-9]', '_', titel)[:25].strip('_').lower()
    mp3_filename = f"{niveau}_{slug}_{int(time.time())}.mp3"
    mp3_path = os.path.join(AUDIO_DIR, mp3_filename)
    
    combined.export(mp3_path, format="mp3")
    print(f"   Succes: {mp3_filename} opgeslagen in audio map.")
    
    # Update de les_data met de audio link en sla op in db
    les_data['audio_url'] = f"audio/{mp3_filename}"
    les_id = opslaan_in_database(les_data)
    
    print(f"\n🎉 KLAAR! De les is opgeslagen in de database onder ID '{les_id}'.")
    print("Open 'luisteren.html' om de nieuwe les te bekijken.")

if __name__ == "__main__":
    main()
