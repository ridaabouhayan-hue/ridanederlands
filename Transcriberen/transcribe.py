import os
import sys
import json
from google import genai

# ================================================
# 1. API KEY INSTELLEN
GEMINI_API_KEY = "AIzaSyCsTsvbfmMQJQm4g0IBjCdw4VlG1fRA0Qk"
os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY

root_dir = os.path.dirname(os.path.abspath(__file__))
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
      "brief": "Hallo [Naam]! 👋\\n\\nWat goed dat je hebt geoefend! [Korte intro over logica/context]. 🎈\\n\\n👍 Wat ging er al heel goed?\\n[Noem iets positiefs over een woord, klank of grammatica] 🌟\\n\\n💡 Tips voor de volgende keer:\\n\\nTip 1: [Titel van tip 1] ❌\\nWat je zei: \\"[Foute zin/woord]\\"\\nHoe het moet: \\"[Correcte zin/woord]\\"\\nUitleg: [Waarom is dit de regel?]\\n\\nOefen nu hardop:\\n\\"[Voorbeeldzin 1]\\" 🗣️\\n\\"[Voorbeeldzin 2]\\" 🗣️\\n\\nTip 2: [Titel van tip 2] 🏡\\nWat je zei: \\"[Foute zin/woord]\\"\\nHoe het moet: \\"[Correcte zin/woord]\\"\\nUitleg: [Korte uitleg]\\n\\nOefen nu hardop:\\n\\"[Voorbeeldzin 3]\\" 🗣️\\n\\n🏁 Persoonlijk slotwoord\\n[Korte aanmoediging]. Je volgende stap is... Ga zo door! 🚀\\n\\nGemaakt door Rida Abouhayan✉ r.abouhayan@hotmail.nl | 📱 +31 6 26211106"
    }}
  ]
}}

Geef ALLEEN deze JSON terug. Zorg dat de JSON valide is. Geef geen extra tekst buiten de JSON."""
                
                # Lage temperatuur (0.1) zorgt ervoor dat Gemini niet gaat 'gissen' of 'creatief' wordt.
                # response_mime_type="application/json" dwingt Gemini om correcte JSON terug te geven.
                response = client.models.generate_content(
                    model='gemini-3.5-flash',
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
                
                data[grp].append({
                    "filename": filename,
                    "path": f"{grp}/{filename}",
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
                if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str or "503" in err_str or "UNAVAILABLE" in err_str or "11001" in err_str or "getaddrinfo" in err_str or "Connection" in err_str:
                    print(f"⏳ API-limiet, netwerkfout of drukte op server bereikt. Even pauze (60 seconden) voordat we onbeperkt doorgaan...")
                    time.sleep(60)
                else:
                    print(f"❌ Fout bij '{filename}': {err_str}")
                    break # Stop bij een andere (onbekende) fout, ga naar volgende bestand

    print("\n🎉 Alle nieuwe bestanden zijn succesvol verwerkt!")

if __name__ == "__main__":
    main()
