import os
import json
import requests
from pydub import AudioSegment
import time

# Bestandsnamen
API_FILE = "API_ELEVENLABS.txt"
VOICES_FILE = "stemmen.json"
INPUT_FILE = "gesprek.txt"
OUTPUT_FILE = "gesprek_compleet.mp3"
TEMP_DIR = "temp_audio"

def load_api_key():
    if not os.path.exists(API_FILE):
        print(f"Let op: Bestand '{API_FILE}' niet gevonden!")
        print("Maak dit bestand aan en plak je ElevenLabs API key erin.")
        return None
    with open(API_FILE, 'r', encoding='utf-8') as f:
        return f.read().strip()

def load_voices():
    if not os.path.exists(VOICES_FILE):
        print(f"Let op: Bestand '{VOICES_FILE}' niet gevonden!")
        print("We maken een voorbeeld aan. Vul daar de juiste Voice ID's van ElevenLabs in.")
        dummy_data = {
            "Rida": "vul_hier_jouw_voice_id_in_1",
            "Fatima": "vul_hier_jouw_voice_id_in_2"
        }
        with open(VOICES_FILE, 'w', encoding='utf-8') as f:
            json.dump(dummy_data, f, indent=4)
        return dummy_data
    with open(VOICES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_speech(text, voice_id, api_key, output_path):
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
        print(f"Fout bij genereren audio: {response.status_code}")
        print(response.text)
        return False

def main():
    api_key = load_api_key()
    if not api_key:
        return
        
    voices = load_voices()
    
    if not os.path.exists(INPUT_FILE):
        print(f"Maak een bestand genaamd '{INPUT_FILE}' en zet daar het gesprek in.")
        print("Voorbeeld format:")
        print("Rida: Hallo, hoe gaat het?")
        print("Fatima: Goed, dankjewel!")
        return
        
    # Lees gesprek in
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)
        
    audio_segments = []
    
    print("Start met genereren van het gesprek...")
    
    # Korte pauze tussen sprekers (in milliseconden)
    silence_duration = 600
    silence = AudioSegment.silent(duration=silence_duration)
    
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
            
        if ':' not in line:
            print(f"Regel overgeslagen (geen dubbele punt gevonden): {line}")
            continue
            
        speaker, text = line.split(':', 1)
        speaker = speaker.strip()
        text = text.strip()
        
        if speaker not in voices:
            print(f"Waarschuwing: Spreker '{speaker}' niet gevonden in {VOICES_FILE}. Regel wordt overgeslagen.")
            continue
            
        voice_id = voices[speaker]
        if "vul_hier" in voice_id:
            print(f"Fout: De voice ID voor {speaker} is nog niet ingevuld in {VOICES_FILE}.")
            return
            
        temp_file = os.path.join(TEMP_DIR, f"line_{i:03d}.mp3")
        
        print(f"[{i+1}/{len(lines)}] Genereren voor {speaker}: '{text}'")
        success = generate_speech(text, voice_id, api_key, temp_file)
        
        if success:
            # Voeg in in pydub
            segment = AudioSegment.from_mp3(temp_file)
            if audio_segments:
                # Voeg pauze toe na de vorige spreker
                audio_segments.append(silence)
            audio_segments.append(segment)
        else:
            print("Gestopt wegens een API fout.")
            return
            
        # Voorkom API rate limits (optioneel, maar veilig)
        time.sleep(0.5)
        
    if audio_segments:
        # Alles samenvoegen
        print("\nSamenvoegen van de bestanden...")
        combined = AudioSegment.empty()
        for seg in audio_segments:
            combined += seg
            
        combined.export(OUTPUT_FILE, format="mp3")
        print(f"Succes! Het complete gesprek is opgeslagen als: {OUTPUT_FILE}")
    else:
        print("Er was geen audio gegenereerd.")

if __name__ == "__main__":
    main()
