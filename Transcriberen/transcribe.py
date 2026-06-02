import os
import sys
import json
from google import genai

# ================================================
# 1. API KEY INSTELLEN
root_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(root_dir)
api_key_path = os.path.join(parent_dir, "API.txt")

GEMINI_API_KEY = None
if os.path.exists(api_key_path):
    with open(api_key_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("GEMINI_API_KEY="):
                GEMINI_API_KEY = line.split("=", 1)[1].strip()
                break

if not GEMINI_API_KEY:
    print("❌ Kan GEMINI_API_KEY niet vinden in API.txt in de hoofdmap.")
    sys.exit(1)

os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY

audio_extensies = ('.mp3', '.m4a', '.wav', '.ogg', '.flac', '.3gp', '.aac', '.webm')

groepen = [
    "Microsoft", "KPN", "Westport", "VDL", "Neways", "Shell", 
    "Coca-Cola", "NS", "B-A1", "B-A2", "B-Alfa", "B-Z-route", "B-ONA"
]

if len(sys.argv) > 1:
    doel_groep = sys.argv[1]
    if doel_groep in groepen:
        groepen = [doel_groep]
        print(f"📌 Filter actief: Alleen de groep '{doel_groep}' wordt verwerkt.")
    else:
        print(f"❌ Groep '{doel_groep}' niet gevonden in de lijst. Beschikbaar: {', '.join(groepen)}")
        sys.exit(1)

data_file = os.path.join(root_dir, "data.js")

def load_data():
    if os.path.exists(data_file):
        try:
            with open(data_file, "r", encoding="utf-8") as f:
                content = f.read()
                json_str = content.replace("window.geminiData =", "").strip()
                if json_str.endswith(";"):
                    json_str = json_str[:-1]
                return json.loads(json_str)
        except Exception as e:
            print(f"Waarschuwing: Kon bestaande data.js niet inladen ({e}). Er wordt een nieuwe gestart.")
    return {grp: [] for grp in groepen}

def save_data(data):
    with open(data_file, "w", encoding="utf-8") as f:
        f.write("window.geminiData = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n")

def main():
    data = load_data()
    
    # Zorg dat alle groepen in de data staan
    for grp in groepen:
        if grp not in data:
            data[grp] = []

    to_process = []
    
    # Scan alle groepen mappen
    for grp in groepen:
        grp_dir = os.path.join(root_dir, grp)
        if not os.path.exists(grp_dir):
            os.makedirs(grp_dir)
            
        for entry in os.scandir(grp_dir):
            if entry.is_file() and entry.name.lower().endswith(audio_extensies):
                # Check of dit bestand al in data.js staat
                already_done = any(item["filename"] == entry.name for item in data[grp])
                if not already_done:
                    to_process.append((grp, entry.name, entry.path))
                    
    if not to_process:
        print("\n📂 Geen nieuwe audiobestanden gevonden om te transcriberen.")
        sys.exit(0)
        
    print(f"\n🎧 {len(to_process)} nieuwe audiobestand(en) gevonden. We gaan beginnen!")

    try:
        client = genai.Client()
    except Exception as e:
        print(f"❌ Kon geen verbinding maken met Gemini. Klopt de API key? Fout: {e}")
        sys.exit(1)

    import time

    for grp, filename, filepath in to_process:
        print(f"\n⏳ Bezig met: [{grp}] {filename}")
        
        while True:
            try:
                print("   Uploaden...")
                audio_file = client.files.upload(file=filepath)
                
                print("   Transcriberen...")
                
                # NT2-specifieke prompt voor Zin-voor-Zin analyse (in JSON)
                prompt = f"""Je bent een strenge maar opbouwende NT2 docent (Nederlands als Tweede Taal).
De bestandsnaam van de audio is "{filename}". De namen in deze bestandsnaam verwijzen vaak naar de sprekers (bijvoorbeeld: "Spreker1 Spreker2" betekent Spreker1 praat als eerste, Spreker2 als tweede). Gebruik deze namen om de sprekers te identificeren in je analyse. Als er geen namen staan, gebruik dan Spreker A en Spreker B.

Maak een grondige ZIN-VOOR-ZIN analyse. Geef EXACT het volgende JSON formaat terug:

{{
  "gesprek": [
    {{
      "spreker": "Naam van de spreker",
      "zin_fonetisch": "Schrijf exact en fonetisch uit wat er werd gezegd, inclusief stotteren, pauzes (uhm) of taalfouten.",
      "zin_correct": "Hoe de cursist deze zin in perfect Nederlands had moeten uitspreken en formuleren.",
      "uitspraak_analyse": {{
        "goed": true,
        "fout": "Wat er fout klonk (of laat leeg als het goed was)",
        "uitleg": "Waarom het fout is (bijv. verkeerde klank, klemtoon)"
      }},
      "grammatica_analyse": {{
        "goed": false,
        "fout": "Wat de grammaticale fout was (of laat leeg als het goed was)",
        "uitleg": "De grammaticaregel (bijv. inversie, verkeerd lidwoord)"
      }}
    }}
  ],
  "feedback_brieven": [
    {{
      "naam": "Naam van de cursist",
      "brief": "Hallo [Naam]! 👋\\n\\nWat goed dat je hebt geoefend! Hieronder heb ik jouw hele verhaal letterlijk zin voor zin uitgeschreven. Ik vertel je per zin wat er supergoed ging, en wat nog beter kan.\\n\\n🔍 **Zin-voor-Zin Analyse:**\\n\\n**Zin 1:** \\"[Fonetische zin van cursist]\\"\\n👍 Wat was goed: [Compliment over uitspraak of woordkeuze]\\n💡 Correctie: \\"[Correcte zin]\\"\\n🧠 Waarom: [Uitleg over de grammaticaregel of klank]\\n\\n**Zin 2:** \\"[Fonetische zin 2]\\"\\n... [herhaal voor ALLE gesproken zinnen van deze cursist]\\n\\n🏁 **Samenvatting & Jouw volgende stap:**\\n[Korte samenvatting van de belangrijkste valkuil en een aanmoediging]. Ga zo door! 🚀\\n\\nGemaakt door Rida Abouhayan✉ r.abouhayan@hotmail.nl | 📱 +31 6 26211106"
    }}
  ]
}}

Geef ALLEEN deze JSON terug. Zorg dat de JSON valide is. Geef geen extra tekst buiten de JSON."""
                
                # Lage temperatuur (0.1) zorgt ervoor dat Gemini niet gaat 'gissen' of 'creatief' wordt.
                # response_mime_type="application/json" dwingt Gemini om correcte JSON terug te geven.
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[audio_file, prompt],
                    config={'temperature': 0.1, 'response_mime_type': 'application/json'}
                )
                
                # Parse the JSON response
                try:
                    result = json.loads(response.text.strip())
                except json.JSONDecodeError:
                    print("Waarschuwing: Gemini gaf geen geldige JSON terug. Fallback naar ruwe tekst.")
                    result = {
                        "gesprek": [],
                        "feedback_brieven": []
                    }
                
                # Haal bestandsdatum op (laatst gewijzigd)
                mtime = os.path.getmtime(filepath)
                file_date = time.strftime('%d-%m-%Y', time.localtime(mtime))

                data[grp].append({
                    "filename": filename,
                    "path": f"{grp}/{filename}",
                    "date": file_date,
                    "analyse": result
                })
                
                # Sla direct op na elk succesvol bestand
                save_data(data)
                print(f"✅ Klaar! Opgeslagen in data.js")
                
                # Standaard 4 seconden wachten om de API-limiet (15 per minuut) niet te raken
                time.sleep(4)
                break # Uit de while loop stappen (succes!)
                
            except Exception as e:
                err_str = str(e)
                print(f"❌ EXACT ERROR: {err_str}")
                if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str or "503" in err_str or "UNAVAILABLE" in err_str or "11001" in err_str or "getaddrinfo" in err_str or "Connection" in err_str:
                    print(f"⏳ API-limiet, netwerkfout of drukte op server bereikt. Even pauze (60 seconden) voordat we onbeperkt doorgaan...")
                    time.sleep(60)
                else:
                    print(f"❌ Fout bij '{filename}': {err_str}")
                    break # Stop bij een andere (onbekende) fout, ga naar volgende bestand

    print("\n🎉 Alle nieuwe bestanden zijn succesvol verwerkt!")

if __name__ == "__main__":
    main()
