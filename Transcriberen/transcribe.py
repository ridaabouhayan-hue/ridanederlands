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

# Model selectie: gebruik Pro/Flash model voor maximale nauwkeurigheid en perfecte naleving van instructies.
# Fallback is ingesteld op gemini-2.5-pro als gemini-3.5-flash niet beschikbaar is op dit API-key tier.
GEMINI_MODEL = "gemini-3.5-flash"

audio_extensies = ('.mp3', '.m4a', '.wav', '.ogg', '.flac', '.3gp', '.aac', '.webm', '.mp4')

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
                # Check of dit bestand al in data.js staat met een succesvolle analyse
                already_done = False
                existing_item = None
                entry_basename = os.path.splitext(entry.name)[0]
                for item in data[grp]:
                    item_basename = os.path.splitext(item["filename"])[0]
                    if item_basename == entry_basename:
                        existing_item = item
                        analyse = item.get("analyse", {})
                        if isinstance(analyse, dict) and (analyse.get("gesprek") or analyse.get("feedback_brieven")):
                            already_done = True
                        break
                
                if not already_done:
                    # Als het bestand al in data.js staat maar de analyse mislukt of leeg was,
                    # verwijderen we de oude entry zodat we hem opnieuw schoon kunnen toevoegen.
                    if existing_item:
                        data[grp].remove(existing_item)
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
        
        audio_file = None
        while True:
            try:
                if not audio_file:
                    print("   Uploaden...")
                    audio_file = client.files.upload(file=filepath)
                
                # Wacht tot het bestand verwerkt is
                print("   Wachten tot het bestand actief is...")
                while audio_file.state.name == "PROCESSING":
                    time.sleep(2)
                    audio_file = client.files.get(name=audio_file.name)
                
                if audio_file.state.name != "ACTIVE":
                    raise Exception(f"Bestand uploaden mislukt (status: {audio_file.state.name})")
                
                print("   Transcriberen...")
                # NT2-specifieke prompt voor Zin-voor-Zin analyse (in JSON)
                prompt = f"""Je bent een strenge maar opbouwende NT2 docent (Nederlands als Tweede Taal).
De bestandsnaam van de audio is "{filename}".

IDENTIFICATIE VAN DE SPREKERS:
1. Luister heel goed en kritisch naar de audio om te bepalen wie er spreekt en de stemmen te koppelen aan de juiste namen.
2. Vaak noemen de sprekers hun eigen naam in het gesprek (bijvoorbeeld: 'Hallo, ik ben Malwina' of 'Hoi, met Tomasz') of noemen ze elkaar bij naam (bijvoorbeeld: 'En jij, Malwina?'). Als er namen genoemd worden in de audio, gebruik die dan altijd om de sprekers te identificeren.
3. Als er absoluut geen namen genoemd worden in de audio, kijk dan naar de bestandsnaam "{filename}". De namen in de bestandsnaam (bijvoorbeeld 'Malwina Dorota interview.mp3' of 'Kojo Emad 4-6.ogg') vertellen je wie de sprekers zijn en in welke volgorde ze praten. De eerste naam in de bestandsnaam begint meestal met praten, en de tweede reageert.
4. Zorg dat je de sprekers correct identificeert en hun echte namen gebruikt in de 'gesprek' array (in de 'spreker' velden) in plaats van generieke aanduidingen zoals 'Spreker A' of 'Spreker B' of 'Spreker A/B'.

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
      }},
      "logica_analyse": {{
        "goed": false,
        "fout": "Wat er onlogisch of vreemd was aan de betekenis/samenhang in de context (of laat leeg als het logisch was)",
        "uitleg": "Waarom het onlogisch is in deze context en wat een betere logische verwoording is"
      }}
    }}
  ],
  "feedback_brieven": [
    {{
      "naam": "Naam van de cursist",
      "brief": "Hallo [Naam]! 👋\\n\\nWat goed dat je hebt geoefend! Hieronder heb ik jouw hele verhaal letterlijk zin voor zin uitgeschreven. Ik vertel je per zin wat er goed ging, en wat nog beter kan.\\n\\n🔍 *Zin-voor-Zin Analyse:*\\n\\n*Zin 1:* \\"[Fonetische zin van cursist]\\"\\n👍 *Wat was goed:* [Compliment over uitspraak of woordkeuze]\\n💡 *Correctie:* \\"[Correcte zin]\\"\\n🧠 *Waarom:* [Uitleg over de grammaticaregel of klank]\\n🤔 *Logica:* [Uitleg over waarom de zin qua betekenis/samenhang onlogisch of vreemd is in deze context, en wat het logische alternatief is. LAAT DEZE REGEL COMPLEET WEG ALS DE ZIN LOGISCH IS EN KLOPT IN DE CONTEXT! OOK GEEN LEGE REGELS DAARVOOR OVERLATEN]\\n\\n*Zin 2:* \\"[Fonetische zin 2]\\"\\n... [herhaal voor ALLE gesproken zinnen van deze cursist]\\n\\n🏁 *Samenvatting & Belangrijkste leerpunten:*\\n• *Grammatica:* [Gedetailleerde samenvatting van veelgemaakte grammaticafouten in de opname, wat er vaak misging en waarom]\\n• *Uitspraak:* [Gedetailleerde samenvatting van veelgemaakte uitspraakfouten of klanken die vaak verkeerd gingen, met concrete tips]\\n• *Samenhang & Logica:* [Samenvatting van zinnen die grammaticaal of qua uitspraak wel goed waren, maar die inhoudelijk niet logisch waren in het gesprek, met uitleg waarom]\\n\\n🧠 *Jouw volgende stap & advies:*\\n[Concreet advies over waar de cursist de komende tijd op moet letten om stappen te maken en een bemoedigende uitsmijter]. Ga zo door! 🚀\\n\\nGemaakt door Rida Abouhayan✉ r.abouhayan@hotmail.nl | 📱 +31 6 26211106",
      "brief_en": "Hello [Name]! 👋\\n\\nGreat job practicing! Below I have transcribed your entire story literally sentence by sentence. I will tell you per sentence what went well, and what could be improved.\\n\\n🔍 *Sentence-by-Sentence Analysis:*\\n\\n*Sentence 1:* \\"[Phonetic sentence of student]\\"\\n👍 *What was good:* [Compliment on pronunciation or word choice]\\n💡 *Correction:* \\"[Correct sentence]\\"\\n🧠 *Why:* [Explanation of grammar rule or sound]\\n🤔 *Logic:* [Explanation of why the sentence is not logical or sounds strange in this context, and what the logical alternative is. OMIT THIS LINE COMPLETELY IF THE SENTENCE IS SEMANTICALLY LOGICAL AND MAKES SENSE IN CONTEXT! DO NOT LEAVE EMPTY LINES EITHER]\\n\\n*Sentence 2:* \\"[Phonetic sentence 2]\\"\\n... [repeat for ALL spoken sentences of this student]\\n\\n🏁 *Summary & Key Takeaways:*\\n• *Grammar:* [Detailed summary of common grammatical errors in the recording, what went wrong often and why]\\n• *Pronunciation:* [Detailed summary of common pronunciation errors or sounds that went wrong often, with concrete tips]\\n• *Coherence & Logic:* [Summary of sentences that were grammatically correct but semantically illogical or weird in context, with explanation]\\n\\n🧠 *Your next step & advice:*\\n[Concrete advice on what the student should focus on in the near future to make progress, and an encouraging closing statement]. Keep it up! 🚀\\n\\nMade by Rida Abouhayan✉ r.abouhayan@hotmail.nl | 📱 +31 6 26211106"
    }}
  ]
}}

BELANGRIJK:
1. Zowel 'brief' als 'brief_en' moeten geformatteerd zijn voor WhatsApp: gebruik een enkele asterisk (*) voor vetgedrukte woorden (bijv. *Zin 1:* en *Correctie:* en *Waarom:*). Gebruik GEEN dubbele asterisks (**).
2. Zeg bij een uitspraak of grammatica die correct is NOOIT dat het 'perfect' of 'foutloos' is (dit niveau is voor B2/C1). Zeg in plaats daarvan dat het 'goed', 'duidelijk' of 'begrijpelijk' is.
3. Evalueer de betekenis en logica van elke zin in context. Als een zin grammaticaal correct en goed uitgesproken is, maar betekenisvol niet klopt in het lopende gesprek (bijvoorbeeld: "Ik wil naar huis gaan, maar ik heb geen extra tijd" in plaats van "Ik wil naar huis gaan, maar ik ben nog niet klaar"), rapporteer dit dan in 'logica_analyse' en leg uit wat een betere logische verwoording is.
4. Je MOET absoluut feedback geven op ELKE zin die de cursist in het gesprek uitspreekt. Het is ten strengste verboden om zinnen over te slaan, samen te voegen of weg te laten uit de brieven! Als een zin helemaal goed was en geen fouten bevatte, noteer dit dan ook in de brief (bijv. "👍 *Wat was goed:* Je spreekt deze zin heel duidelijk uit. 💡 *Correctie:* [schrijf hier de originele zin]").
5. ALS ER MEERDERE SPREKERS/CURSISTEN ZIJN (bijvoorbeeld twee cursisten die met elkaar praten):
   - Je MOET voor IEDERE cursist/spreker een APARTE feedbackbrief genereren in de `feedback_brieven` array. Dus als Malwina en Dorota praten, maak je EXACT twee objecten in `feedback_brieven` aan: één voor Malwina en één voor Dorota.
   - De feedbackbrief voor een specifieke cursist mag ALLEEN de zinnen bevatten die door die SPECIFIEKE cursist zijn uitgesproken (genummerd als *Zin 1:* t/m *Zin N:* voor die persoon). Sla geen zinnen over die door die persoon zijn gezegd, en voeg geen zinnen van de andere spreker(s) toe!
   - Zorg dat de samenvatting, feedback en het advies in de brief volledig en respectievelijk gericht zijn op hoe die specifieke persoon het heeft gedaan, zodat de docent deze brief direct per WhatsApp individueel naar hen kan sturen."""
                
                # Lage temperatuur (0.1) zorgt ervoor dat Gemini niet gaat 'gissen' of 'creatief' wordt.
                # response_mime_type="application/json" dwingt Gemini om correcte JSON terug te geven.
                try:
                    response = client.models.generate_content(
                        model=GEMINI_MODEL,
                        contents=[audio_file, prompt],
                        config={'temperature': 0.1, 'response_mime_type': 'application/json'}
                    )
                except Exception as model_err:
                    err_lower = str(model_err).lower()
                    if "404" in err_lower or "not found" in err_lower or "not_found" in err_lower:
                        print(f"⚠️ Model '{GEMINI_MODEL}' niet ondersteund of niet gevonden op deze API-sleutel tier. Fallback naar 'gemini-2.5-pro'...")
                        response = client.models.generate_content(
                            model='gemini-2.5-pro',
                            contents=[audio_file, prompt],
                            config={'temperature': 0.1, 'response_mime_type': 'application/json'}
                        )
                    else:
                        raise model_err
                
                # Parse the JSON response
                if not response.text or not response.text.strip():
                    raise Exception("Gemini returned empty response.text (retryable)")
                    
                try:
                    result = json.loads(response.text.strip())
                except json.JSONDecodeError as je:
                    raise Exception(f"Gemini returned invalid JSON (retryable): {je}")
                
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
                
                # Standaard 8 seconden wachten om de API-limiet (15 per minuut) niet te raken
                time.sleep(8)
                break # Uit de while loop stappen (succes!)
                
            except Exception as e:
                err_str = str(e)
                print(f"❌ EXACT ERROR: {err_str}")
                if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str or "503" in err_str or "UNAVAILABLE" in err_str or "11001" in err_str or "getaddrinfo" in err_str or "Connection" in err_str or "retryable" in err_str:
                    print(f"⏳ Tijdelijke fout of API-limiet. Even pauze (80 seconden) voordat we het opnieuw proberen...")
                    time.sleep(80)
                else:
                    print(f"❌ Fout bij '{filename}': {err_str}")
                    break # Stop bij een andere (onbekende) fout, ga naar volgende bestand

    print("\n🎉 Alle nieuwe bestanden zijn succesvol verwerkt!")

if __name__ == "__main__":
    main()
