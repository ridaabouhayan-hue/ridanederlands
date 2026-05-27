import os
import json
import re
import sys
import urllib.request
import urllib.error

# Ensure ffmpeg path is in environmental PATH for this session
ffmpeg_path = r"C:\Users\Rabou\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin"
if os.path.exists(ffmpeg_path):
    if ffmpeg_path not in os.environ["PATH"]:
        os.environ["PATH"] = ffmpeg_path + os.pathsep + os.environ["PATH"]

def load_anthropic_key(root_dir):
    """Laadt de Anthropic API-sleutel uit de TRANSCRIPT API map."""
    api_file = os.path.join(root_dir, "TRANSCRIPT API", "API.txt")
    if os.path.exists(api_file):
        try:
            with open(api_file, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]
                for line in lines:
                    if line.startswith("sk-ant-"):
                        return line
        except Exception:
            pass
    return None

def get_ai_corrections(transcript, api_key):
    """Haalt de twee gecorrigeerde versies op via de Claude API."""
    if not api_key:
        print("WAARSCHUWING: Geen Anthropic API key gevonden. Claude correcties worden overgeslagen.")
        return "", ""
        
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    
    prompt = (
        "Je bent een uitspraakdocent Nederlands NT2.\n"
        "Ik geef je een letterlijk, fonetisch transcript van een cursist met een zwaar accent en grammaticafouten. "
        "Geef me twee gecorrigeerde versies terug in een JSON-formaat.\n\n"
        "1. 'uitspraak_gecorrigeerd': Corrigeer alleen de verkeerd uitgesproken woorden en spelfouten naar correcte Nederlandse woorden, "
        "maar laat de grammaticale fouten, verkeerde zinsbouw en woordvolgorde exact zoals ze zijn. Verander bijvoorbeeld 'Noor-en-Bugestrat' naar 'Noorderbuurtstraat' "
        "en 'commenta' naar 'gemeente', maar laat 'In welke gemeente woon jij?' of 'Ik drinken koffie' ongewijzigd.\n"
        "2. 'volledig_gecorrigeerd': Corrigeer alles: spelling, uitspraak, grammatica, lidwoorden en zinsbouw naar perfect, natuurlijk Nederlands.\n\n"
        "Het antwoord MOET alleen een geldige JSON zijn met exact de keys 'uitspraak_gecorrigeerd' en 'volledig_gecorrigeerd'. "
        "Geen andere tekst, inleiding, toelichting of markdown blocks.\n\n"
        f"Transcript:\n\"{transcript}\""
    )
    
    data = {
        "model": "claude-haiku-4-5-20251001",
        "max_tokens": 1000,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    req = urllib.request.Request(
        url, 
        data=json.dumps(data).encode("utf-8"), 
        headers=headers, 
        method="POST"
    )
    
    print("Ophalen van correcties via Claude API...")
    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            content_text = res_data["content"][0]["text"].strip()
            
            # Strip markdown json blocks if present
            if content_text.startswith("```"):
                content_text = re.sub(r"^```(?:json)?\n", "", content_text)
                content_text = re.sub(r"\n```$", "", content_text)
            
            parsed = json.loads(content_text.strip())
            return parsed.get("uitspraak_gecorrigeerd", ""), parsed.get("volledig_gecorrigeerd", "")
    except Exception as e:
        print(f"Fout bij ophalen correcties via Claude API: {e}")
        return "", ""

def transcribe_audio(audio_path, model_name="medium"):
    try:
        import whisper
    except ImportError:
        print("FOUT: OpenAI Whisper is niet geïnstalleerd in deze Python-omgeving.")
        print("Installeer het met: pip install openai-whisper")
        return None

    print(f"Laden van Whisper-model '{model_name}'...")
    try:
        model = whisper.load_model(model_name)
    except Exception as e:
        print(f"FOUT bij laden model: {e}")
        # Probeer fallback naar base model als medium faalt (bijv. te weinig VRAM/RAM)
        print("Fallback naar 'base' model...")
        model = whisper.load_model("base")

    # NT2 Prompt optimalisatie voor uitspraakfouten en grammaticafouten
    # We geven Whisper de specifieke instructie om letterlijk te transcriberen en geen fouten te corrigeren!
    nt2_prompt = (
        "Dit is een geluidsopname van een buitenlandse cursist die Nederlands leert praten. "
        "De cursist spreekt met een zwaar accent en maakt grammaticafouten, uitspraakfouten en zinsbouwfouten. "
        "Transcribeer exact en letterlijk wat er wordt gezegd. Corrigeer de grammatica en de spelling NIET. "
        "Behoud aarzelingen en herhalingen zoals 'eh', 'uh', 'ik drinken', 'de groene auto'."
    )

    print(f"Transcriberen van: {os.path.basename(audio_path)}")
    try:
        # We zetten no_speech_threshold en logprob_threshold op None om te voorkomen dat Whisper zinnen skipt!
        result = model.transcribe(
            audio_path,
            language="nl",
            initial_prompt=nt2_prompt,
            temperature=0.2, # Laag genoeg voor stabiliteit, hoog genoeg om fouten niet weg te poetsen
            word_timestamps=False,
            no_speech_threshold=None,
            logprob_threshold=None,
            compression_ratio_threshold=None
        )
        return result["text"].strip()
    except Exception as e:
        print(f"Fout tijdens transcriberen: {e}")
        return None

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    audio_groepen_dir = os.path.join(root_dir, "audio", "groepen")
    
    # Lijst van alle groepsnamen uit het dashboard
    groepen = [
        "Microsoft", "KPN", "Westport", "VDL", "Neways", "Shell", 
        "Coca-Cola", "NS", "B-A1", "B-A2", "B-Alfa", "B-Z-route", "B-ONA"
    ]
    
    # 1. Maak de mappen aan als ze nog niet bestaan
    if not os.path.exists(audio_groepen_dir):
        os.makedirs(audio_groepen_dir)
        
    for grp in groepen:
        grp_dir = os.path.join(audio_groepen_dir, grp)
        if not os.path.exists(grp_dir):
            os.makedirs(grp_dir)
            print(f"Groepsmap aangemaakt: {os.path.relpath(grp_dir, root_dir)}")

    # 2. Doorzoek alle groepsmappen op audiobestanden
    audio_extensions = (".mp3", ".wav", ".m4a", ".ogg", ".3gp", ".aac", ".webm")
    transcripts_cache_file = os.path.join(audio_groepen_dir, "transcripts_cache.json")
    
    # Laad bestaande cache om dubbel werk te voorkomen
    cache = {}
    if os.path.exists(transcripts_cache_file):
        try:
            with open(transcripts_cache_file, "r", encoding="utf-8") as f:
                cache = json.load(f)
        except Exception:
            cache = {}

    anthropic_key = load_anthropic_key(root_dir)

    # Verzamel bestanden die verwerkt moeten worden
    to_process = []
    for grp in groepen:
        grp_dir = os.path.join(audio_groepen_dir, grp)
        for entry in os.scandir(grp_dir):
            if entry.is_file() and entry.name.lower().endswith(audio_extensions):
                rel_path = f"audio/groepen/{grp}/{entry.name}"
                if rel_path not in cache:
                    to_process.append((rel_path, entry.path, grp, entry.name))

    # Als er geen nieuwe bestanden zijn
    if not to_process:
        print("Geen nieuwe audiobestanden gevonden.")
        # Genereer index alsnog ter controle
        generate_index_js(cache, audio_groepen_dir, groepen)
        return

    # Toon overzicht en vraag gebruiker om te runnen
    print(f"\n{'='*50}")
    print(f"Er zijn {len(to_process)} nieuwe audiobestanden gevonden:")
    for rel_path, _, grp, name in to_process:
        print(f"  - [{grp}] {name}")
    print(f"{'='*50}")
    
    if anthropic_key:
        print("Claude API sleutel is geladen. Correcties worden automatisch gegenereerd.")
    else:
        print("Let op: Geen Claude API sleutel gevonden in TRANSCRIPT API/API.txt.")
        print("Alleen letterlijke transcripties worden gegenereerd.")

    try:
        user_input = input("\nDruk op Enter om de transcriptie te starten (of Ctrl+C om te annuleren)... ")
    except KeyboardInterrupt:
        print("\nGeannuleerd door gebruiker.")
        sys.exit(0)

    # Transcribeer de nieuwe bestanden
    for rel_path, full_path, grp, name in to_process:
        transcript = transcribe_audio(full_path, model_name="medium")
        
        if transcript:
            uitspraak_corr, volledig_corr = "", ""
            if anthropic_key:
                uitspraak_corr, volledig_corr = get_ai_corrections(transcript, anthropic_key)
                
            cache[rel_path] = {
                "filename": name,
                "group": grp,
                "transcript": transcript,
                "transcript_uitspraak": uitspraak_corr,
                "transcript_volledig": volledig_corr
            }
            
            # Tussentijds opslaan in JSON cache
            with open(transcripts_cache_file, "w", encoding="utf-8") as f:
                json.dump(cache, f, ensure_ascii=False, indent=2)

    # Genereer index.js bestand
    generate_index_js(cache, audio_groepen_dir, groepen)
    print("\nAlle bestanden succesvol getranscribeerd en gecorrigeerd!")

def generate_index_js(cache, audio_groepen_dir, groepen):
    index_js_path = os.path.join(audio_groepen_dir, "index.js")
    
    # Groepeer de cache data per groep
    grouped_data = {grp: [] for grp in groepen}
    for rel_path, data in cache.items():
        grp = data["group"]
        if grp in grouped_data:
            grouped_data[grp].append({
                "filename": data["filename"],
                "path": "../" + rel_path, # Relatief pad vanuit Groepen/ map
                "transcript": data["transcript"],
                "transcript_uitspraak": data.get("transcript_uitspraak", ""),
                "transcript_volledig": data.get("transcript_volledig", "")
            })
            
    js_content = f"// Automatisch gegenereerd door transcribe_groepen.py\nwindow.groepenAudioData = {json.dumps(grouped_data, ensure_ascii=False, indent=2)};\n"
    
    with open(index_js_path, "w", encoding="utf-8") as f:
        f.write(js_content)

if __name__ == "__main__":
    main()
