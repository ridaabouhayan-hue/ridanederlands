import whisper
import json
import os
import sys

# Ensure ffmpeg path is in environmental PATH for this session
ffmpeg_path = r"C:\Users\Rabou\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin"
if os.path.exists(ffmpeg_path):
    if ffmpeg_path not in os.environ["PATH"]:
        os.environ["PATH"] = ffmpeg_path + os.pathsep + os.environ["PATH"]
else:
    print(f"Waarschuwing: ffmpeg map niet gevonden op {ffmpeg_path}. Zorg dat ffmpeg is geïnstalleerd en in je PATH staat.")

# Zet hier de naam van je audiobestand
audiobestand = "nos_26mei.mp3"

# Controleer of het bestand bestaat
if not os.path.exists(audiobestand):
    print(f"FOUT: bestand '{audiobestand}' niet gevonden.")
    print(f"Zorg dat het bestand in deze map staat: {os.getcwd()}")
    print("Herneem de naam van je bestand in 'transcribe.py' als het anders heet.")
    sys.exit(1)

print(f"Bestand gevonden: {audiobestand}")
print("Model laden ('base' model voor betere Nederlandse nauwkeurigheid)...")

# We gebruiken "base" model. Je kunt ook "tiny" (sneller) of "small" (nauwkeuriger) proberen.
model = whisper.load_model("base")

print("Transcriberen... even geduld, dit kan 1-2 minuten duren.")
result = model.transcribe(
    audiobestand,
    language="nl",
    word_timestamps=True,
    verbose=False
)

# Woorden verzamelen met timestamps
woorden = []
woorden_zonder_tijd = 0

for segment in result["segments"]:
    for woord in segment.get("words", []):
        tekst = woord["word"].strip()
        if not tekst:
            continue
        if "start" in woord and "end" in woord:
            woorden.append({
                "word":  tekst,
                "start": round(woord["start"], 3),
                "end":   round(woord["end"],   3)
            })
        else:
            woorden_zonder_tijd += 1

# JSON opslaan
uitvoer = audiobestand.rsplit(".", 1)[0] + "_timestamps.json"
with open(uitvoer, "w", encoding="utf-8") as f:
    json.dump(woorden, f, ensure_ascii=False, indent=2)

# Samenvatting
print(f"\n{'='*45}")
print(f"  Klaar!")
print(f"  Woorden met timestamp : {len(woorden)}")
if woorden_zonder_tijd:
    print(f"  Woorden zonder tijd   : {woorden_zonder_tijd} (normaal)")
print(f"  Opgeslagen als        : {uitvoer}")
print(f"{'='*45}")

print("\nEerste 8 woorden als voorbeeld:")
print(f"  {'WOORD':<20} {'START':>8}   {'EINDE':>8}")
print(f"  {'-'*40}")
for w in woorden[:8]:
    print(f"  {w['word']:<20} {w['start']:>7}s   {w['end']:>7}s")

print(f"\nVolledige tekst:")
print(" ".join(w["word"] for w in woorden))
