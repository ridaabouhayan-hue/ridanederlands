import os
import sys
import json
import requests
import time
import re
import random
import threading
import webbrowser
from google import genai
from pydub import AudioSegment

import tkinter as tk
from tkinter import ttk, messagebox

GEMINI_API_FILE = "API.txt"
ELEVEN_API_FILE = "API_ELEVENLABS.txt"
VOICES_FILE = "stemmen.json"

OUTPUT_DIR = "Luisterlessen"
AUDIO_DIR = os.path.join(OUTPUT_DIR, "audio")
DATA_FILE = os.path.join(OUTPUT_DIR, "data.json")
TEMP_DIR = "temp_audio"

class LesGeneratorError(Exception):
    pass

def load_gemini_key():
    if not os.path.exists(GEMINI_API_FILE):
        raise LesGeneratorError(f"Fout: {GEMINI_API_FILE} niet gevonden.")
    with open(GEMINI_API_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith("GEMINI_API_KEY="):
                return line.split("=", 1)[1].strip()
    raise LesGeneratorError("Fout: GEMINI_API_KEY niet gevonden in API.txt.")

def load_eleven_key():
    if not os.path.exists(ELEVEN_API_FILE):
        raise LesGeneratorError(f"Fout: {ELEVEN_API_FILE} niet gevonden. Maak dit bestand aan en zet hier puur je ElevenLabs API key in.")
    with open(ELEVEN_API_FILE, 'r', encoding='utf-8') as f:
        return f.read().strip()

def load_voices():
    if not os.path.exists(VOICES_FILE):
        dummy_data = {
            "Vrouwen": [
                "vul_hier_vrouwen_voice_id_1",
                "vul_hier_vrouwen_voice_id_2"
            ],
            "Mannen": [
                "vul_hier_mannen_voice_id_1",
                "vul_hier_mannen_voice_id_2"
            ]
        }
        with open(VOICES_FILE, 'w', encoding='utf-8') as f:
            json.dump(dummy_data, f, indent=4)
        raise LesGeneratorError(f"Bestand {VOICES_FILE} aangemaakt met een voorbeeldstructuur. Vul hier je Voice ID's in!")
        
    with open(VOICES_FILE, 'r', encoding='utf-8') as f:
        voices = json.load(f)
        
    # Controleer of er ten minste één geldige voice ID in staat
    has_valid_voice = False
    for k, v in voices.items():
        if isinstance(v, list):
            for item in v:
                if item and "vul_hier" not in item:
                    has_valid_voice = True
        elif isinstance(v, str):
            if v and "vul_hier" not in v:
                has_valid_voice = True
                
    if not has_valid_voice:
        raise LesGeneratorError(f"Let op: Vul eerst ten minste één geldige Voice ID in in {VOICES_FILE}.")
            
    return voices

def assign_speaker_voices(sprekers, voices):
    # Haal vrouwelijke stemmen op (ondersteunt "Vrouwen" lijst of "Vrouw" string/lijst)
    vrouwen_ids = []
    if "Vrouwen" in voices:
        vrouwen_ids = voices["Vrouwen"] if isinstance(voices["Vrouwen"], list) else [voices["Vrouwen"]]
    elif "Vrouw" in voices:
        vrouwen_ids = voices["Vrouw"] if isinstance(voices["Vrouw"], list) else [voices["Vrouw"]]
        
    # Haal mannelijke stemmen op (ondersteunt "Mannen" lijst of "Man" string/lijst)
    mannen_ids = []
    if "Mannen" in voices:
        mannen_ids = voices["Mannen"] if isinstance(voices["Mannen"], list) else [voices["Mannen"]]
    elif "Man" in voices:
        mannen_ids = voices["Man"] if isinstance(voices["Man"], list) else [voices["Man"]]
        
    # Filter placeholder-teksten eruit
    vrouwen_ids = [vid for vid in vrouwen_ids if vid and "vul_hier" not in vid]
    mannen_ids = [vid for vid in mannen_ids if vid and "vul_hier" not in vid]
    
    if not vrouwen_ids and not mannen_ids:
        raise LesGeneratorError("Fout: Geen geldige Voice IDs gevonden in stemmen.json.")
        
    # Kopieer en schud de stemmenlijsten om willekeurig unieke stemmen toe te wijzen
    available_vrouwen = vrouwen_ids.copy()
    random.shuffle(available_vrouwen)
    available_mannen = mannen_ids.copy()
    random.shuffle(available_mannen)
    
    assigned = {}
    for naam, info in sprekers.items():
        geslacht = info.get('geslacht', 'vrouw').lower()
        if 'man' in geslacht and not 'vrouw' in geslacht:
            if available_mannen:
                assigned[naam] = available_mannen.pop(0)
            elif mannen_ids:
                assigned[naam] = random.choice(mannen_ids)
            else:
                assigned[naam] = random.choice(vrouwen_ids) if vrouwen_ids else None
        else:
            if available_vrouwen:
                assigned[naam] = available_vrouwen.pop(0)
            elif vrouwen_ids:
                assigned[naam] = random.choice(vrouwen_ids)
            else:
                assigned[naam] = random.choice(mannen_ids) if mannen_ids else None
                
        if not assigned[naam]:
            raise LesGeneratorError(f"Fout: Kan geen stem toewijzen aan {naam} ({geslacht}) omdat er geen stemmen in stemmen.json staan.")
            
    return assigned

def genereer_les_data(prompt, niveau, gemini_key):
    client = genai.Client(api_key=gemini_key)
    
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

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=systeem_prompt
    )
    
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
        raise LesGeneratorError(f"Fout: Gemini gaf geen geldig JSON formaat terug: {e}")

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
        raise LesGeneratorError(f"ElevenLabs Error: {response.text}")

def opslaan_in_database(les_data):
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            try:
                db = json.load(f)
            except json.JSONDecodeError:
                db = []
    else:
        db = []
        
    les_data['id'] = f"{les_data['niveau'].lower()}_{int(time.time())}"
    db.append(les_data)
    
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(db, f, indent=4)
        
    # Sla ook op als data.js voor lokale file:// compatibiliteit
    js_file = os.path.join(OUTPUT_DIR, "data.js")
    with open(js_file, 'w', encoding='utf-8') as f:
        f.write(f"window.luisterportaalData = {json.dumps(db, indent=4)};\n")
        
    return les_data['id']

# ─── GUI LOGICA ───

def run_gui():
    root = tk.Tk()
    root.title("Les Generator - Luisterportaal")
    root.geometry("480x320")
    root.resizable(False, False)

    try:
        root.iconbitmap('favicon.ico')
    except:
        pass

    style = ttk.Style()
    style.theme_use('clam')

    # Fonts
    font_large = ('Segoe UI', 12)
    font_bold = ('Segoe UI', 12, 'bold')

    frame = tk.Frame(root, bg="#f0f4f8", padx=25, pady=25)
    frame.pack(fill=tk.BOTH, expand=True)

    tk.Label(frame, text="Maak een nieuwe Luisterles", font=('Segoe UI', 16, 'bold'), bg="#f0f4f8", fg="#1e293b").pack(anchor=tk.W, pady=(0, 20))

    # Onderwerp
    tk.Label(frame, text="Onderwerp (bijv. in de supermarkt):", font=font_large, bg="#f0f4f8").pack(anchor=tk.W)
    subject_var = tk.StringVar()
    subject_entry = ttk.Entry(frame, textvariable=subject_var, width=45, font=font_large)
    subject_entry.pack(fill=tk.X, pady=(5, 15))

    # Niveau
    tk.Label(frame, text="Niveau:", font=font_large, bg="#f0f4f8").pack(anchor=tk.W)
    level_var = tk.StringVar(value="A1")
    level_combo = ttk.Combobox(frame, textvariable=level_var, values=["Pre-A1", "A1", "A2", "B1", "B2", "C1", "C2"], state="readonly", font=font_large)
    level_combo.pack(fill=tk.X, pady=(5, 20))

    # Status
    status_var = tk.StringVar(value="")
    status_label = tk.Label(frame, textvariable=status_var, fg="#3b82f6", bg="#f0f4f8", font=font_large)
    status_label.pack(anchor=tk.W, pady=(0, 10))

    def on_generate():
        prompt = subject_var.get().strip()
        niveau = level_var.get()
        if not prompt:
            messagebox.showwarning("Waarschuwing", "Vul a.u.b. een onderwerp in.")
            return

        generate_btn.config(state=tk.DISABLED)
        status_var.set("Starten...")

        def worker():
            try:
                if not os.path.exists(TEMP_DIR): os.makedirs(TEMP_DIR)
                if not os.path.exists(AUDIO_DIR): os.makedirs(AUDIO_DIR)

                status_var.set("API sleutels inladen...")
                gemini_key = load_gemini_key()
                eleven_key = load_eleven_key()
                voices = load_voices()

                # Stap 1
                status_var.set("1/3: AI schrijft het script en de vragen...")
                les_data = genereer_les_data(prompt, niveau, gemini_key)
                
                speaker_to_voiceid = assign_speaker_voices(les_data['sprekers'], voices)

                # Stap 2
                status_var.set("2/3: Audio genereren met ElevenLabs...")
                audio_segments = []
                silence = AudioSegment.silent(duration=500)
                
                conversatie = les_data['conversatie']
                for i, zin in enumerate(conversatie):
                    speaker = zin['speaker']
                    text = zin['text']
                    voice_id = speaker_to_voiceid.get(speaker)
                    temp_file = os.path.join(TEMP_DIR, f"line_{i}.mp3")
                    
                    status_var.set(f"2/3: Audio opnemen regel {i+1} van {len(conversatie)}...")
                    genereer_audio_elevenlabs(text, voice_id, eleven_key, temp_file)
                    
                    seg = AudioSegment.from_mp3(temp_file)
                    if audio_segments:
                        audio_segments.append(silence)
                    audio_segments.append(seg)
                    time.sleep(0.5)

                # Stap 3
                status_var.set("3/3: Audio samenvoegen en opslaan...")
                combined = AudioSegment.empty()
                for seg in audio_segments:
                    combined += seg
                    
                slug = re.sub(r'[^a-zA-Z0-9]', '_', les_data['thema'])[:25].strip('_').lower()
                mp3_filename = f"{niveau}_{slug}_{int(time.time())}.mp3"
                mp3_path = os.path.join(AUDIO_DIR, mp3_filename)
                
                combined.export(mp3_path, format="mp3")
                
                les_data['audio_url'] = f"audio/{mp3_filename}"
                opslaan_in_database(les_data)

                status_var.set("✅ Klaar! Les is opgeslagen.")
                messagebox.showinfo("Succes!", f"Les '{les_data['thema']}' is succesvol gegenereerd en toegevoegd aan het portaal!")
                
                # Probeer lokaal de website te openen
                portal_path = os.path.abspath(os.path.join(OUTPUT_DIR, "index.html"))
                webbrowser.open(f"file:///{portal_path.replace(chr(92), '/')}")

            except LesGeneratorError as e:
                status_var.set("❌ Fout opgetreden.")
                messagebox.showerror("Fout", str(e))
            except Exception as e:
                status_var.set("❌ Fout opgetreden.")
                messagebox.showerror("Systeem Fout", str(e))
            finally:
                generate_btn.config(state=tk.NORMAL)

        threading.Thread(target=worker, daemon=True).start()

    generate_btn = tk.Button(frame, text="🚀 Genereer Les", bg="#3b82f6", fg="white", font=font_bold, cursor="hand2", relief="flat", command=on_generate)
    generate_btn.pack(fill=tk.X, ipady=8, pady=(10, 0))

    root.mainloop()

# ─── COMMAND LINE LOGICA ───

def run_cli():
    try:
        prompt = sys.argv[1]
        niveau = sys.argv[2].upper()
        
        gemini_key = load_gemini_key()
        eleven_key = load_eleven_key()
        voices = load_voices()
        
        if not os.path.exists(TEMP_DIR):
            os.makedirs(TEMP_DIR)
        if not os.path.exists(AUDIO_DIR):
            os.makedirs(AUDIO_DIR)
            
        print("1. AI aan het werk zetten via Gemini...")
        les_data = genereer_les_data(prompt, niveau, gemini_key)
        titel = les_data['thema']
        print(f"\n✅ Les gegenereerd: [{niveau}] {titel}")
        
        speaker_to_voiceid = assign_speaker_voices(les_data['sprekers'], voices)

        print("\n2. Audio genereren via ElevenLabs...")
        audio_segments = []
        silence = AudioSegment.silent(duration=500)
        
        conversatie = les_data['conversatie']
        for i, zin in enumerate(conversatie):
            speaker = zin['speaker']
            text = zin['text']
            voice_id = speaker_to_voiceid.get(speaker)
            
            temp_file = os.path.join(TEMP_DIR, f"line_{i}.mp3")
            print(f"   Spraak ophalen voor regel {i+1} ({speaker})...")
            
            genereer_audio_elevenlabs(text, voice_id, eleven_key, temp_file)
            seg = AudioSegment.from_mp3(temp_file)
            if audio_segments:
                audio_segments.append(silence)
            audio_segments.append(seg)
            time.sleep(0.5)
            
        print("\n3. Audio samenvoegen...")
        combined = AudioSegment.empty()
        for seg in audio_segments:
            combined += seg
            
        slug = re.sub(r'[^a-zA-Z0-9]', '_', titel)[:25].strip('_').lower()
        mp3_filename = f"{niveau}_{slug}_{int(time.time())}.mp3"
        mp3_path = os.path.join(AUDIO_DIR, mp3_filename)
        
        combined.export(mp3_path, format="mp3")
        print(f"   Succes: {mp3_filename} opgeslagen in audio map.")
        
        les_data['audio_url'] = f"audio/{mp3_filename}"
        les_id = opslaan_in_database(les_data)
        
        print(f"\n🎉 KLAAR! De les is opgeslagen in de database onder ID '{les_id}'.")
    except LesGeneratorError as e:
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if len(sys.argv) < 3:
            print("Fout: Geef een onderwerp én een niveau mee. Bijv: python genereer_les.py \"Bank\" \"A2\"")
            sys.exit(1)
        run_cli()
    else:
        # Geen argumenten? Open de grafische Windows interface!
        run_gui()
