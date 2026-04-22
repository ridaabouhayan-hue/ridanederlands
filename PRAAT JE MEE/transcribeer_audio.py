import os
import sys

try:
    import imageio_ffmpeg
    import shutil
    
    # Imageio downloadt ffmpeg onder een gekke naam (zoals ffmpeg-win64.exe). 
    # Whisper zoekt exact naar 'ffmpeg.exe'. We kopiëren hem daarom even naar een bin-mapje.
    original_ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    ffmpeg_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bin")
    if not os.path.exists(ffmpeg_dir):
        os.makedirs(ffmpeg_dir)
        
    local_ffmpeg = os.path.join(ffmpeg_dir, "ffmpeg.exe")
    if not os.path.exists(local_ffmpeg):
        shutil.copy2(original_ffmpeg, local_ffmpeg)
        
    # Voeg de bin-map toe aan de Windows PATH (zodat Whisper hem kan vinden)
    os.environ["PATH"] += os.pathsep + ffmpeg_dir
except ImportError:
    pass # we install it via pip in the background anyway

import whisper
import glob

# Map voor de audioberichten
AUDIO_DIR = "audioberichten"

# Welke bestandstypen WhatsApp/telefoons/videos meestal gebruiken
AUDIO_EXTENSIONS = ('*.ogg', '*.m4a', '*.mp3', '*.wav', '*.aac', '*.wma', '*.mp4', '*.mov', '*.avi', '*.webm')

def main():
    if not os.path.exists(AUDIO_DIR):
        os.makedirs(AUDIO_DIR)
        print(f"[*] Ik heb de map '{AUDIO_DIR}' voor je aangemaakt.")
        print("Sleep al jouw voice memo's in deze map en draai mij opnieuw!")
        return

    # Zoek alle audiobestanden in de map
    files = []
    for ext in AUDIO_EXTENSIONS:
        files.extend(glob.glob(os.path.join(AUDIO_DIR, ext)))

    if not files:
        print(f"Geen audiobestanden gevonden in de map '{AUDIO_DIR}'.")
        print("Zet er eerst een bestandje in (.ogg, .mp3, etc.)")
        return

    print("[AI] Ai-model (Whisper) wordt opgestart... (dit kan de eerste keer even duren i.v.m. downloaden)\n")
    try:
        # We gebruiken het 'base' model. Dat is snel en erg goed voor Nederlands.
        # Als de laptop sterk is kun je ook 'small' gebruiken.
        model = whisper.load_model("base")
    except Exception as e:
        print(f"FOUT bij inladen Whisper: {e}")
        return

    for count, file in enumerate(files, 1):
        filename = os.path.basename(file)
        name_only = os.path.splitext(filename)[0]
        output_txt = os.path.join(AUDIO_DIR, f"{name_only}.txt")

        if os.path.exists(output_txt):
            print(f"[{count}/{len(files)}] Sla ik over (bestaat al): {filename}")
            continue

        print(f"[{count}/{len(files)}] [>] Ben aan het luisteren naar: {filename} ...")
        
        try:
            # Transcribeer het audiobestand in het Nederlands
            result = model.transcribe(file, language="nl")
            text = result["text"].strip()
            
            # Schrijf weg naar bestand
            with open(output_txt, 'w', encoding='utf-8') as f:
                f.write(f"Bestand: {filename}\n")
                f.write("-" * 40 + "\n\n")
                f.write(text)
                
            print(f"  -> Klaar! Opgeslagen als {name_only}.txt")
        except Exception as e:
            print(f"  -> Fout bij script: {e}")

    print("\n[V] ALLES KLAAR! Je kunt de uitgetypte teksten nu vinden in de map 'audioberichten'.")

if __name__ == "__main__":
    main()
