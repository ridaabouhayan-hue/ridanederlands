import os
import json
import requests

API_FILE = "API_ELEVENLABS.txt"
VOICES_FILE = "stemmen.json"
AUDIO_DIR = os.path.join("audio", "A1", "thema1")
DICTEE_DIR = os.path.join(AUDIO_DIR, "dictee")

def load_api_key():
    if not os.path.exists(API_FILE):
        print(f"Fout: Bestand '{API_FILE}' niet gevonden!")
        return None
    with open(API_FILE, 'r', encoding='utf-8') as f:
        return f.read().strip()

def load_voices():
    if not os.path.exists(VOICES_FILE):
        print(f"Fout: Bestand '{VOICES_FILE}' niet gevonden!")
        return None
    with open(VOICES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_speech(text, voice_id, api_key, output_path, stability=0.78, similarity_boost=0.82):
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
            "stability": stability,
            "similarity_boost": similarity_boost
        }
    }
    
    print(f"Genereren: '{text}' (stability={stability}) -> {output_path}")
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            f.write(response.content)
        print(f"✅ Succesvol opgeslagen: {output_path}")
        return True
    else:
        print(f"❌ Fout bij genereren ({response.status_code}): {response.text}")
        return False

def get_dictee_filename(text):
    # Converteert tekst naar veilige bestandsnaam conform de JS-logica
    clean = text.lower()
    for char in ['?', '.', '!', ',']:
        clean = clean.replace(char, '')
    clean = clean.strip()
    # Vervang meerdere spaties door een enkele underscore
    clean = "_".join(clean.split())
    return f"{clean}.mp3"

def main():
    api_key = load_api_key()
    if not api_key:
        return
        
    voices = load_voices()
    if not voices:
        return
        
    # Kies stemmen (vrouw voor toets 1 en dictee, man voor toets 2)
    female_voice = voices.get("Vrouwen", [None])[0]
    male_voice = voices.get("Mannen", [None])[0]
    
    if not female_voice or not male_voice:
        print("Fout: Kon geen stemmen laden uit stemmen.json")
        return

    # Zorg dat de mappen bestaan
    os.makedirs(DICTEE_DIR, exist_ok=True)
    
    # --- OEFENTOETS 1 ---
    # Luistertekst
    oefentoets1_luisteren_text = (
        "Hallo, ik heet Julia. Ik ben dertig jaar oud. Ik kom uit Spanje. "
        "Ik woon nu in Nederland, in Utrecht. Ik heb een man en twee kinderen. "
        "Mijn man heet Thomas. Mijn zoon heet Max en mijn dochter heet Emma. "
        "Ik spreek Spaans en een beetje Nederlands."
    )
    generate_speech(
        oefentoets1_luisteren_text, 
        female_voice, 
        api_key, 
        os.path.join(AUDIO_DIR, "oefentoets1-luisteren.mp3")
    )
    
    # Dicteewoorden en -zinnen
    oefentoets1_dictee = [
        "naam", "wonen", "gezin", "moeder", "getrouwd", "letter",
        "Ik kom uit Spanje.", "Hoe heet jouw broer?", "Mijn vader woont in Utrecht."
    ]
    for text in oefentoets1_dictee:
        filename = get_dictee_filename(text)
        # Formatteer losse woorden met een hoofdletter en punt voor duidelijke NT2-uitspraak
        gen_text = text
        if " " not in text and not text.endswith("."):
            gen_text = text.capitalize() + "."
            
        generate_speech(
            gen_text, 
            female_voice, 
            api_key, 
            os.path.join(DICTEE_DIR, filename),
            stability=0.88,
            similarity_boost=0.85
        )
        
    # --- OEFENTOETS 2 ---
    # Luistertekst
    oefentoets2_luisteren_text = (
        "Hoi, ik ben Karim. Ik ben vijfentwintig jaar oud. Ik kom uit Syrië. "
        "Ik woon nu in Amsterdam. Ik ben niet getrouwd. Ik heb geen kinderen. "
        "Ik heb wel een broer en een zus. Mijn broer heet Samir en mijn zus heet Leyla. "
        "Ik spreek Arabisch en een beetje Nederlands. Ik leer Nederlands op school."
    )
    generate_speech(
        oefentoets2_luisteren_text, 
        male_voice, 
        api_key, 
        os.path.join(AUDIO_DIR, "oefentoets2-luisteren.mp3")
    )
    
    # Dicteewoorden en -zinnen
    oefentoets2_dictee = [
        "vader", "dochter", "praten", "school", "letter", "mevrouw",
        "Ik leer Nederlands op school.", "Waar woont jouw familie?", "Zij spreekt een beetje Nederlands."
    ]
    for text in oefentoets2_dictee:
        filename = get_dictee_filename(text)
        # Formatteer losse woorden met een hoofdletter en punt voor duidelijke NT2-uitspraak
        gen_text = text
        if " " not in text and not text.endswith("."):
            gen_text = text.capitalize() + "."
            
        generate_speech(
            gen_text, 
            female_voice, 
            api_key, 
            os.path.join(DICTEE_DIR, filename),
            stability=0.88,
            similarity_boost=0.85
        )
        
    print("\n🎉 Alle audiobestanden gegenereerd!")

if __name__ == "__main__":
    main()
