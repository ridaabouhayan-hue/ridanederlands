import os
import glob
from openai import OpenAI
import sys

# ==========================================
# 1. VUL HIER JOUW OPENAI API SLEUTEL IN:
# Je haalt deze op via platform.openai.com
API_KEY = "VUL_HIER_JE_API_KEY_IN"
# ==========================================

AUDIO_DIR = "audioberichten"
AUDIO_EXTENSIONS = ('*.ogg', '*.m4a', '*.mp3', '*.wav', '*.aac', '*.wma', '*.mp4', '*.mov', '*.avi', '*.webm')

# Dit is het brein van jouw NT2 docent. Hier sturen we het transcript heen.
NT2_DOCENT_PROMPT = """Je bent een doorgewinterde NT2-docent (Nederlands als Tweede Taal) gespecialiseerd in niveau A1/A2. 
Je analyseert de transcriptie van een spraakbericht van een cursist. Let op: Je krijgt enkel de getypte tekst te zien via een Whisper-transcriptie. 

Jouw taak:
1. VERWACHTE UITSPRAAKFOUTEN: Omdat het via een spraakherkenner is gegaan, kunnen uitspraakfouten eruit zien als vreemde woorden. Bijvoorbeeld: als Whisper "maan" opschrijft in plaats van "man" (in "de maan loopt op straat"), of "bom" in plaats van "boom", wijs de docent er dan op dat de cursist hoogstwaarschijnlijk een fout maakte met de LANGE/KORTE klank (aa/a, oo/o, ee/e).
2. GRAMMATICA: Kijk door het accent of sprekersritme heen: kloppen de werkwoorden (ik werk, jij werkt) en de woordvolgorde?
3. RECONSTRUCTIE: Wat wilde de cursist waarschijnlijk exact zeggen?
4. FEEDBACK: Geef 2 positieve en 1 of 2 opbouwende tips specifiek gericht op wat je analyseerde.

Genereer een makkelijk leesbaar rapportje speciaal voor mij als docent."""

def main():
    if API_KEY == "VUL_HIER_JE_API_KEY_IN":
        print("WAARSCHUWING: Je hebt je OpenAI API-sleutel nog niet ingevuld!")
        print("Open 'transcribeer_pro.py' en plak je sleutel bovenaan bij API_KEY.")
        sys.exit(1)

    try:
        # Open een verbinding met de professionele cloud
        client = OpenAI(api_key=API_KEY)
    except Exception as e:
        print(f"Kon geen verbinding maken met OpenAI: {e}")
        sys.exit(1)

    if not os.path.exists(AUDIO_DIR):
        os.makedirs(AUDIO_DIR)
        print(f"Map '{AUDIO_DIR}' aangemaakt. Zet hier je spraakberichten in.")
        return

    files = []
    for ext in AUDIO_EXTENSIONS:
        files.extend(glob.glob(os.path.join(AUDIO_DIR, ext)))

    if not files:
        print(f"Geen nieuwe audiobestanden gevonden in '{AUDIO_DIR}'.")
        return

    for count, file_path in enumerate(files, 1):
        filename = os.path.basename(file_path)
        name_only = os.path.splitext(filename)[0]
        output_txt = os.path.join(AUDIO_DIR, f"{name_only}_NAGEKEKEN.txt")

        # Skip de audioberichten die al zijn nagekeken
        if os.path.exists(output_txt):
            continue

        print(f"\n[{count}/{len(files)}] 🎧 Bezig met {filename}...")
        
        try:
            # STAP 1: Gebruik Cloud Whisper (veel sterker dan lokaal)
            print("  -> Spraakherkenning op zware accenten via Whisper-1 (Cloud)...")
            with open(file_path, "rb") as audio_file:
                transcription = client.audio.transcriptions.create(
                    model="whisper-1", 
                    file=audio_file,
                    language="nl",
                    prompt="Uhm, dit is een spraakbericht van een buitenlandse cursist, NT2 niveau A1. Er worden fouten gemaakt."
                )
            
            ruwe_tekst = transcription.text
            print(f"  -> Transcriptie succesvol. Tekst: '{ruwe_tekst}'")

            # STAP 2: Stuur het naar de slimme NT2 docent AI
            print("  -> Nakijken op grammaticale en uitspraakfouten met GPT-4o...")
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": NT2_DOCENT_PROMPT},
                    {"role": "user", "content": f"De ruwe transcriptie van de cursist is:\n\n{ruwe_tekst}"}
                ],
                temperature=0.3
            )

            nakijk_rapport = response.choices[0].message.content

            # STAP 3: Sla zowel het rapport als de ruwe tekst op in een bestand!
            with open(output_txt, 'w', encoding='utf-8') as f:
                f.write(f"=== AUDIO BERICHT: {filename} ===\n")
                f.write(f"WAT WHISPER HOORDE:\n{ruwe_tekst}\n")
                f.write("="*40 + "\n\n")
                f.write(nakijk_rapport)
                
            print(f"  -> ✅ Klaar! Feedback rapport opgeslagen in '{name_only}_NAGEKEKEN.txt'")
            
        except Exception as e:
            print(f"  -> ❌ Fout bij bestand {filename}: {e}")

    print("\nAlle nieuwe audioberichten zijn professioneel nagekeken en liggen voor je klaar!")

if __name__ == "__main__":
    main()
