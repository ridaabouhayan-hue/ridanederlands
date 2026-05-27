import os
import json
import re
import sys

# Ensure ffmpeg path is in environmental PATH for this session
ffmpeg_path = r"C:\Users\Rabou\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin"
if os.path.exists(ffmpeg_path):
    if ffmpeg_path not in os.environ["PATH"]:
        os.environ["PATH"] = ffmpeg_path + os.pathsep + os.environ["PATH"]

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
        result = model.transcribe(
            audio_path,
            language="nl",
            initial_prompt=nt2_prompt,
            temperature=0.2, # Laag genoeg voor stabiliteit, hoog genoeg om fouten niet weg te poetsen
            word_timestamps=False
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

    changed = False
    
    for grp in groepen:
        grp_dir = os.path.join(audio_groepen_dir, grp)
        for entry in os.scandir(grp_dir):
            if entry.is_file() and entry.name.lower().endswith(audio_extensions):
                rel_path = f"audio/groepen/{grp}/{entry.name}"
                
                # Check of dit bestand al getranscribeerd is
                if rel_path in cache:
                    continue
                    
                print(f"\nNieuw audiobestand gevonden in groep {grp}!")
                transcript = transcribe_audio(entry.path, model_name="medium")
                
                if transcript:
                    cache[rel_path] = {
                        "filename": entry.name,
                        "group": grp,
                        "transcript": transcript
                    }
                    changed = True
                    # Tussentijds opslaan
                    with open(transcripts_cache_file, "w", encoding="utf-8") as f:
                        json.dump(cache, f, ensure_ascii=False, indent=2)

    # 3. Genereer het index.js bestand voor het HTML dashboard
    # Dit zorgt ervoor dat het dashboard alle audio's en transcripts direct CORS-safe kan inlezen!
    index_js_path = os.path.join(audio_groepen_dir, "index.js")
    
    # Groepeer de cache data per groep
    grouped_data = {grp: [] for grp in groepen}
    for rel_path, data in cache.items():
        grp = data["group"]
        if grp in grouped_data:
            grouped_data[grp].append({
                "filename": data["filename"],
                "path": "../" + rel_path, # Relatief pad vanuit Groepen/ map
                "transcript": data["transcript"]
            })
            
    js_content = f"// Automatisch gegenereerd door transcribe_groepen.py\nwindow.groepenAudioData = {json.dumps(grouped_data, ensure_ascii=False, indent=2)};\n"
    
    with open(index_js_path, "w", encoding="utf-8") as f:
        f.write(js_content)
        
    print(f"\n{'='*50}")
    print("Klaar! De groepen index is succesvol bijgewerkt.")
    print(f"Javascript index opgeslagen: {os.path.relpath(index_js_path, root_dir)}")
    print(f"Totaal aantal getranscribeerde opnames: {len(cache)}")
    print(f"{'='*50}\n")
    print("Instructie:")
    print("1. Sleep de MP3/M4A spraakopnames van je studenten in de juiste groepsmappen onder audio/groepen/.")
    print("2. Run dit script: python transcribe_groepen.py")
    print("3. Open het dashboard op je website om de transcripts te bekijken.")

if __name__ == "__main__":
    main()
