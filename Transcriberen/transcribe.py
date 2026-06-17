import os
import sys

# Ensure stdout/stderr use UTF-8 on Windows to prevent UnicodeEncodeError when printing emojis
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
if hasattr(sys.stderr, 'reconfigure'):
    try:
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

import json
import re
import requests
from google import genai

# =====================================================================
# CONFIGURATIE VOOR TRANSCRIPTIE
# Service: "gemini" of "elevenlabs"
# - "gemini": Directe multimodal transcriptie door Gemini (Pro of Flash).
# - "elevenlabs": ElevenLabs Scribe voor letterlijke transcriptie + diarization,
#                 waarna Gemini de NT2-analyse en brieven genereert.
#                 AANBEVOLEN: trouwere letterlijke transcriptie en betere
#                 sprekersherkenning dan directe Gemini-audioperceptie.
# Vereist een geldige sleutel in API_ELEVENLABS.txt in de hoofdmap.
TRANSCRIPTION_SERVICE = "elevenlabs"

# Model selectie voor Gemini (bijv. "gemini-1.5-pro" of "gemini-1.5-flash")
# "gemini-1.5-pro" wordt sterk aanbevolen voor maximale nauwkeurigheid en correcte klankweergave.
GEMINI_MODEL = "gemini-1.5-pro"
# Fallback-model als GEMINI_MODEL niet beschikbaar is op deze API-sleutel (404).
GEMINI_FALLBACK_MODEL = "gemini-1.5-flash"

# ElevenLabs Speech-to-Text model id. Pas dit aan als jouw account een ander
# model gebruikt (scribe_v2 is in 2026 het actuele model; scribe_v1 is deprecated).
# Een verkeerde id geeft een fout en valt terug op Gemini-audio.
ELEVENLABS_MODEL = "scribe_v2"

# Maximum aantal pogingen per bestand voordat we het overslaan. Voorkomt dat een
# tijdelijke fout of een afgekapte JSON-respons het script eindeloos laat hangen.
MAX_ATTEMPTS = 4

# Maximum aantal output-tokens voor Gemini. Hoog genoeg voor lange gesprekken met
# twee sprekers (volledige transcriptie + twee brieven) zodat de JSON niet afkapt.
GEMINI_MAX_OUTPUT_TOKENS = 8192

# ---------------------------------------------------------------------
# OPTIONELE EXTRA ANALYSELAGEN (standaard UIT). Zet op True zodra de
# bijbehorende dienst draait en de sleutel/configuratie aanwezig is.
# Beide lagen werken alleen in de 'elevenlabs'-modus (we hebben dan al
# een letterlijke transcriptie als basis).

# LanguageTool: regelgebaseerde grammatica-/spellingcontrole (self-hosted, gratis).
# Start lokaal met Docker (zie SETUP_EXTRA_LAGEN.md), bijv.:
#   docker run -d -p 8081:8010 --name languagetool erikvl87/languagetool
ENABLE_LANGUAGETOOL = False
LANGUAGETOOL_URL = "http://localhost:8081/v2/check"
LANGUAGETOOL_LANG = "nl"

# Azure Pronunciation Assessment: objectieve uitspraakscores per klank (nl-NL).
# Vereist: pip install azure-cognitiveservices-speech  EN  ffmpeg geinstalleerd.
# Sleutel + regio in API_AZURE.txt in de hoofdmap (zie SETUP_EXTRA_LAGEN.md).
ENABLE_AZURE_PRONUNCIATION = False
AZURE_PRON_LANG = "nl-NL"
# =====================================================================

# ================================================
# 1. API KEY INSTELLEN
root_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(root_dir)
api_key_path = os.path.join(parent_dir, "API.txt")
eleven_key_path = os.path.join(parent_dir, "API_ELEVENLABS.txt")

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

ELEVENLABS_API_KEY = None
if os.path.exists(eleven_key_path):
    with open(eleven_key_path, "r", encoding="utf-8") as f:
        ELEVENLABS_API_KEY = f.read().strip()

# Azure Speech-sleutel (alleen nodig als ENABLE_AZURE_PRONUNCIATION = True)
AZURE_SPEECH_KEY = None
AZURE_SPEECH_REGION = None
azure_key_path = os.path.join(parent_dir, "API_AZURE.txt")
if os.path.exists(azure_key_path):
    with open(azure_key_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("AZURE_SPEECH_KEY="):
                AZURE_SPEECH_KEY = line.split("=", 1)[1].strip()
            elif line.startswith("AZURE_SPEECH_REGION="):
                AZURE_SPEECH_REGION = line.split("=", 1)[1].strip()

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

def clean_reconstructed_text(word_list):
    text = " ".join(word_list)
    text = re.sub(r"\s+([.,!?;:])", r"\1", text)
    return text

def transcribe_with_elevenlabs(filepath, api_key):
    """Transcribeert een audiobestand via ElevenLabs Speech-to-Text API met Scribe v2 en diarization."""
    if not api_key:
        raise Exception("Geen ElevenLabs API-sleutel gevonden. Controleer API_ELEVENLABS.txt in de hoofdmap.")
        
    url = "https://api.elevenlabs.io/v1/speech-to-text"
    headers = {
        "xi-api-key": api_key
    }
    data = {
        "model_id": ELEVENLABS_MODEL,
        "diarize": "true"
    }
    
    print("   [ElevenLabs] Verzenden naar ElevenLabs Speech-to-Text API...")
    with open(filepath, "rb") as f:
        files = {
            "file": (os.path.basename(filepath), f, "audio/mpeg")
        }
        response = requests.post(url, headers=headers, data=data, files=files)
        
    if response.status_code != 200:
        raise Exception(f"ElevenLabs STT mislukt ({response.status_code}): {response.text}")
        
    res_json = response.json()
    words = res_json.get("words", [])
    if not words:
        return res_json.get("text", "")
        
    turns = []
    current_speaker = None
    current_turn_words = []
    
    for word in words:
        spk = word.get("speaker_id", "speaker_1")
        w_text = word.get("text", "")
        
        if current_speaker is None:
            current_speaker = spk
            current_turn_words.append(w_text)
        elif spk == current_speaker:
            current_turn_words.append(w_text)
        else:
            turn_text = clean_reconstructed_text(current_turn_words)
            turns.append(f"{current_speaker}: {turn_text}")
            current_speaker = spk
            current_turn_words = [w_text]
            
    if current_turn_words:
        turn_text = clean_reconstructed_text(current_turn_words)
        turns.append(f"{current_speaker}: {turn_text}")
        
    return "\n".join(turns)

def check_grammar_languagetool(text):
    """Stuurt tekst naar een (self-hosted) LanguageTool-server en geeft een
    compacte samenvatting van gevonden grammatica-/spelfouten terug.
    Geeft None als de laag uit staat of de server onbereikbaar is."""
    if not ENABLE_LANGUAGETOOL or not text:
        return None
    try:
        resp = requests.post(
            LANGUAGETOOL_URL,
            data={"text": text, "language": LANGUAGETOOL_LANG},
            timeout=30,
        )
        if resp.status_code != 200:
            print(f"   \u26a0\ufe0f LanguageTool fout ({resp.status_code}). Draait de server? Stap overgeslagen.")
            return None
        matches = resp.json().get("matches", [])
        if not matches:
            return "LanguageTool vond geen grammatica-/spelfouten."
        lines = []
        for m in matches[:60]:
            snippet = m.get("context", {}).get("text", "").strip()
            msg = m.get("message", "")
            repl = ", ".join(r.get("value", "") for r in m.get("replacements", [])[:3])
            line = f'- "{snippet}" -> {msg}'
            if repl:
                line += f" (suggestie: {repl})"
            lines.append(line)
        print(f"   \u2139\ufe0f LanguageTool: {len(matches)} melding(en) gevonden.")
        return "\n".join(lines)
    except Exception as e:
        print(f"   \u26a0\ufe0f LanguageTool niet bereikbaar: {e}. Stap overgeslagen.")
        return None


def _ensure_wav_16k_mono(filepath):
    """Converteert audio naar WAV 16kHz mono (vereist door Azure) met ffmpeg.
    Geeft het pad naar een tijdelijk wav-bestand terug."""
    import subprocess, tempfile
    base = os.path.splitext(os.path.basename(filepath))[0]
    out = os.path.join(tempfile.gettempdir(), f"azure_pron_{base}.wav")
    subprocess.run(
        ["ffmpeg", "-y", "-i", filepath, "-ar", "16000", "-ac", "1", out],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    return out


def assess_pronunciation_azure(filepath, reference_text):
    """Meet de uitspraak met Azure Pronunciation Assessment (nl-NL) en geeft een
    compacte scoresamenvatting terug (0-100). Geeft None bij uit/ontbrekende
    configuratie/fout.
    LET OP: scoort de hele opname tegen een referentietekst; het meest
    betrouwbaar voor monologen. Bij twee sprekers zijn de scores een ruwe
    indicatie van het geheel."""
    if not ENABLE_AZURE_PRONUNCIATION or not reference_text:
        return None
    if not AZURE_SPEECH_KEY or not AZURE_SPEECH_REGION:
        print("   \u26a0\ufe0f Azure niet geconfigureerd (API_AZURE.txt ontbreekt). Stap overgeslagen.")
        return None
    try:
        import azure.cognitiveservices.speech as speechsdk
    except ImportError:
        print("   \u26a0\ufe0f Pakket 'azure-cognitiveservices-speech' ontbreekt (pip install). Stap overgeslagen.")
        return None
    try:
        import time as _t, statistics
        wav_path = _ensure_wav_16k_mono(filepath)
        speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_SPEECH_REGION)
        audio_config = speechsdk.audio.AudioConfig(filename=wav_path)
        pron_config = speechsdk.PronunciationAssessmentConfig(
            reference_text=reference_text,
            grading_system=speechsdk.PronunciationAssessmentGradingSystem.HundredMark,
            granularity=speechsdk.PronunciationAssessmentGranularity.Phoneme,
            enable_miscue=False,
        )
        recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config, language=AZURE_PRON_LANG, audio_config=audio_config)
        pron_config.apply_to(recognizer)

        results = []
        done = {"v": False}

        def _recognized(evt):
            try:
                results.append(speechsdk.PronunciationAssessmentResult(evt.result))
            except Exception:
                pass

        def _stop(evt):
            done["v"] = True

        recognizer.recognized.connect(_recognized)
        recognizer.session_stopped.connect(_stop)
        recognizer.canceled.connect(_stop)
        recognizer.start_continuous_recognition()
        waited = 0
        while not done["v"] and waited < 300:
            _t.sleep(1)
            waited += 1
        recognizer.stop_continuous_recognition()

        if not results:
            return None

        def _avg(attr):
            vals = [getattr(r, attr) for r in results if getattr(r, attr, None) is not None]
            return round(statistics.mean(vals), 1) if vals else None

        acc, flu, comp = _avg("accuracy_score"), _avg("fluency_score"), _avg("completeness_score")
        weak = []
        for r in results:
            for w in (getattr(r, "words", None) or []):
                score = getattr(w, "accuracy_score", None)
                if score is not None and score < 60:
                    weak.append((getattr(w, "word", "?"), score))
        weak_sorted = sorted(weak, key=lambda x: x[1])[:10]
        lines = [f"Gemiddelde uitspraak-accuratesse: {acc}/100, vloeiendheid: {flu}/100, volledigheid: {comp}/100."]
        if weak_sorted:
            lines.append("Zwakst uitgesproken woorden: " + ", ".join(f"{w} ({s:.0f})" for w, s in weak_sorted))
        print(f"   \u2139\ufe0f Azure uitspraak: accuratesse {acc}, vloeiendheid {flu}.")
        return "\n".join(lines)
    except Exception as e:
        print(f"   \u26a0\ufe0f Azure uitspraakanalyse mislukt: {e}. Stap overgeslagen.")
        return None


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
        
        # Check of er een opdracht- of contextbestand is in de groepsmap
        grp_dir = os.path.join(root_dir, grp)
        assignment_context = ""
        for name in ["opdracht.txt", "context.txt"]:
            context_path = os.path.join(grp_dir, name)
            if os.path.exists(context_path):
                try:
                    with open(context_path, "r", encoding="utf-8") as cf:
                        assignment_context = cf.read().strip()
                    print(f"   ℹ️ Opdracht context geladen uit {name} ({len(assignment_context)} tekens)")
                    break
                except Exception as ce:
                    print(f"   ⚠️ Kon {name} niet lezen: {ce}")
        
        custom_instructions = ""
        for name in ["instructies.txt", "custom_instructions.txt", "maatwerk.txt"]:
            inst_path = os.path.join(grp_dir, name)
            if os.path.exists(inst_path):
                try:
                    with open(inst_path, "r", encoding="utf-8") as inf:
                        custom_instructions = inf.read().strip()
                    print(f"   ℹ️ Maatwerk instructies geladen uit {name} ({len(custom_instructions)} tekens)")
                    break
                except Exception as ie:
                    print(f"   ⚠️ Kon {name} niet lezen: {ie}")
        
        audio_file = None
        eleven_transcript = None
        if TRANSCRIPTION_SERVICE == "elevenlabs":
            try:
                eleven_transcript = transcribe_with_elevenlabs(filepath, ELEVENLABS_API_KEY)
                print(f"   ✅ ElevenLabs transcriptie voltooid ({len(eleven_transcript)} tekens)")
            except Exception as ee:
                print(f"   ⚠️ ElevenLabs transcriptie mislukt: {ee}")
                print("   Vallen terug op directe Gemini-audioperceptie...")

        # Optionele objectieve analyselagen (alleen zinvol als we al letterlijke
        # tekst hebben). Beide geven None terug als hun vlag uit staat.
        grammar_report = None
        pron_report = None
        if eleven_transcript:
            grammar_report = check_grammar_languagetool(eleven_transcript)
            pron_report = assess_pronunciation_azure(filepath, eleven_transcript)

        attempt = 0
        while attempt < MAX_ATTEMPTS:
            attempt += 1
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
De bestandsnaam van de audio is "{filename}"."""

                if TRANSCRIPTION_SERVICE == "elevenlabs" and eleven_transcript:
                    prompt += f"""\n\nHier is de letterlijke transcriptie van de audio, gegenereerd door een gespecialiseerd spraak-naar-tekst model (gebruik dit als de 'ground truth' leidraad om te horen wat er exact werd gezegd, en koppel de speaker_id labels aan de echte namen):
---
{eleven_transcript}
---"""

                if custom_instructions:
                    prompt += f"""\n\nBELANGRIJKE EXTRA DOCENT-INSTRUCTIE (MAATWERK):
Houd rekening met de volgende extra instructie bij het genereren van de feedback en de brieven:
"{custom_instructions}" """

                if assignment_context:
                    prompt += f"""\n\nOPDRACHT / CONTEXT VAN DE TAAK:
Je moet controleren of de cursist(en) de opdracht goed hebben gevolgd. Hier is de context/opdrachtomschrijving:
"{assignment_context}"
Evalueer kritisch of ze de opdracht correct hebben uitgevoerd en de juiste grammatica/woordenschat voor deze taak hebben gebruikt. Verwerk dit in hun feedbackbrief."""

                if grammar_report:
                    prompt += f"""\n\nOBJECTIEVE GRAMMATICACONTROLE (LanguageTool, regelgebaseerd):
Hieronder staan automatisch gedetecteerde grammatica-/spelfouten in de letterlijke transcriptie. Gebruik dit als objectieve steun bij je grammatica-feedback, maar beoordeel zelf of een melding terecht is (spreektaal kan valse meldingen geven):
{grammar_report}"""

                if pron_report:
                    prompt += f"""\n\nOBJECTIEVE UITSPRAAKSCORES (Azure Pronunciation Assessment, nl-NL):
Dit zijn gemeten scores (0-100), geen schatting. Gebruik deze concrete getallen in je uitspraakfeedback in plaats van te gissen hoe iets klonk:
{pron_report}"""

                prompt += f"""\n\nIDENTIFICATIE VAN DE SPREKERS:
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
      "brief": "Hallo [Naam]! 👋\\n\\nWat goed dat je hebt geoefend! Hieronder heb ik jouw hele verhaal letterlijk zin voor zin uitgeschreven. Ik vertel je per zin wat er goed ging, en wat nog beter kan.\\n\\n🔍 *Zin-voor-Zin Analyse:*\\n\\n*Zin 1:* \\\"[Fonetische zin van cursist]\\\"\\n👍 *Wat was goed:* [Compliment over uitspraak of woordkeuze]\\n💡 *Correctie:* \\\"[Correcte zin]\\\" (LAAT DEZE EN DE REGEL HIERONDER WEG ALS DE ZIN AL GOED EN CORRECT IS!)\\n🧠 *Waarom:* [Uitleg over de grammaticaregel of klank] (LAAT DEZE EN DE REGEL HIERBOVEN WEG ALS DE ZIN AL GOED EN CORRECT IS!)\\n🤔 *Logica:* [Uitleg over waarom de zin qua betekenis/samenhang onlogisch of vreemd is in deze context, en wat het logische alternatief is. LAAT DEZE REGEL COMPLEET WEG ALS DE ZIN LOGISCH IS EN KLOPT IN DE CONTEXT! OOK GEEN LEGE REGELS DAARVOOR OVERLATEN]\\n\\n*Zin 2:* \\\"[Fonetische zin 2]\\\"\\n... [herhaal voor ALLE gesproken zinnen van deze cursist]\\n\\n🏁 *Samenvatting & Belangrijkste leerpunten:*\\n• *Grammatica:* [Gedetailleerde samenvatting van veelgemaakte grammaticafouten in de opname, wat er vaak misging en waarom]\\n• *Uitspraak:* [Gedetailleerde samenvatting van veelgemaakte uitspraakfouten of klanken die vaak verkeerd gingen, met concrete tips]\\n• *Samenhang & Logica:* [Samenvatting van zinnen die grammaticaal of qua uitspraak wel goed waren, maar die inhoudelijk niet logisch waren in het gesprek, met uitleg waarom]\\n\\n🧠 *Jouw volgende stap & advies:*\\n[Concreet advies over waar de cursist de komende tijd op moet letten om stappen te maken en een bemoedigende uitsmijter]. Ga zo door! 🚀\\n\\nGemaakt door Rida Abouhayan✉ r.abouhayan@hotmail.nl | 📱 +31 6 26211106\",
      "brief_en": "Hello [Name]! 👋\\n\\nGreat job practicing! Below I have transcribed your entire story literally sentence by sentence. I will tell you per sentence what went well, and what could be improved.\\n\\n🔍 *Sentence-by-Sentence Analysis:*\\n\\n*Sentence 1:* \\\"[Phonetic sentence of student]\\\"\\n👍 *What was good:* [Compliment on pronunciation or word choice]\\n💡 *Correction:* \\\"[Correct sentence]\\\" (OMIT THIS AND THE WHY LINE BELOW COMPLETELY IF THE SENTENCE IS ALREADY CORRECT!)\\n🧠 *Why:* [Explanation of grammar rule or sound] (OMIT THIS AND THE CORRECTION LINE ABOVE COMPLETELY IF THE SENTENCE IS ALREADY CORRECT!)\\n🤔 *Logic:* [Explanation of why the sentence is not logical or sounds strange in this context, and what the logical alternative is. OMIT THIS LINE COMPLETELY IF THE SENTENCE IS SEMANTICALLY LOGICAL AND MAKES SENSE IN CONTEXT! DO NOT LEAVE EMPTY LINES EITHER]\\n\\n*Sentence 2:* \\\"[Phonetic sentence 2]\\\"\\n... [repeat for ALL spoken sentences of this student]\\n\\n🏁 *Summary & Key Takeaways:*\\n• *Grammar:* [Detailed summary of common grammatical errors in the recording, what went wrong often and why]\\n• *Pronunciation:* [Detailed summary of common pronunciation errors or sounds that went wrong often, with concrete tips]\\n• *Coherence & Logic:* [Summary of sentences that were grammatically correct but semantically illogical or weird in context, with explanation]\\n\\n🧠 *Your next step & advice:*\\n[Concrete advice on what the student should focus on in the near future to make progress, and an encouraging closing statement]. Keep it up! 🚀\\n\\nMade by Rida Abouhayan✉ r.abouhayan@hotmail.nl | 📱 +31 6 26211106"
    }}
  ]
}}

BELANGRIJK:
1. Zowel 'brief' als 'brief_en' moeten geformatteerd zijn voor WhatsApp: gebruik een enkele asterisk (*) voor vetgedrukte woorden (bijv. *Zin 1:* en *Correctie:* en *Waarom:*). Gebruik GEEN dubbele asterisks (**).
2. Evalueer de uitspraak met reële verwachtingen voor NT2-beginners (A1-A2). Gebruik NOOIT termen als 'natuurlijk en vloeiend', 'perfect' of 'foutloos'. Zeg in plaats daarvan dat het 'goed uitgesproken', 'verstaanbaar', 'duidelijk' of 'begrijpelijk' is.
3. Evalueer de betekenis en logica van elke zin in context. Als een zin grammaticaal correct en goed uitgesproken is, maar betekenisvol niet klopt in het lopende gesprek (bijvoorbeeld: "Ik wil naar huis gaan, maar ik heb geen extra tijd" in plaats van "Ik wil naar huis gaan, maar ik ben nog niet klaar"), rapporteer dit dan in 'logica_analyse' en leg uit wat een betere logische verwoording is.
4. Je MOET absoluut feedback geven op ELKE zin die de cursist in het gesprek uitspreekt. Het is ten strengste verboden om zinnen over te slaan, samen te voegen of weg te laten uit de brieven! Als een zin grammaticaal correct is en er geen uitspraakfouten zijn (dus als er geen correctie nodig is), schrijf dan ALLEEN het compliment bij "👍 *Wat was goed:*". Laat de regels "💡 *Correctie:*" en "🧠 *Waarom:*" in dat geval volledig weg! Schrijf dus nooit een correctieopgave of waarom-uitleg als de zin al goed was.
5. ALS ER MEERDERE SPREKERS/CURSISTEN ZIJN (bijvoorbeeld twee cursisten die met elkaar praten):
   - Je MOET voor IEDERE cursist/spreker een APARTE feedbackbrief genereren in de `feedback_brieven` array. Dus als Malwina en Dorota praten, maak je EXACT twee objecten in `feedback_brieven` aan: één voor Malwina en één voor Dorota.
   - In de feedbackbrief voor een specifieke cursist (bijv. ALI) toon je het GEHELE gesprek in chronologische volgorde zodat de volgorde van de dialoog duidelijk is.
   - Voor de zinnen die door ALI zelf zijn uitgesproken, nummer je ze (bijv. *Zin 1:*, *Zin 2:*) en geef je gedetailleerde feedback. Format:
     Jij zei
     *Zin X:* "[Fonetische zin van ALI]"
     👍 *Wat was goed:* [Compliment]
     💡 *Correctie:* "[Correcte zin]" (alleen als correctie nodig is)
     🧠 *Waarom:* [Uitleg] (alleen als correctie nodig is)
   - Voor de zinnen die door de ANDERE cursist (bijv. SARAH) zijn uitgesproken, toon je deze chronologisch tussendoor als context. Format:
     *SARAH vroeg/zei toen:* "[Zin van Sarah]" (als het een vraag is, gebruik "vroeg", anders "zei")
   - Op deze manier leest de brief voor elke cursist als een chronologisch gesprek waarin hun eigen zinnen gedetailleerd geanalyseerd worden en de zinnen van de ander als pure context ertussen staan.
6. HOUD REKENING MET HET DOELNIVEAU (tussen A0 en B2):
   - De cursisten zijn NT2-leerders van lagere niveaus. De uitleg moet uiterst eenvoudig en begrijpelijk zijn (alsof je het uitlegt aan een kind van 6). Gebruik geen ingewikkeld grammaticaal jargon.
   - Als de cursist geen voorbeeldzin of geen vertaling heeft ingevuld (voor zover dat relevant is in de context van de spreekopdracht), meld dit dan expliciet met een let-op-teken (⚠️).
   - Zorg dat de vertaalde feedbackbrief (`brief_en`) die in de doeltaal is geschreven, de Nederlandse termen (zoals de originele Nederlandse zinnen en correcties) in het Nederlands laat staan, zodat de cursisten niet hoeven te scrollen tussen talen om te zien wat de Nederlandse zinnen waren."""
                
                # Lage temperatuur (0.1) zorgt ervoor dat Gemini niet gaat 'gissen' of 'creatief' wordt.
                # response_mime_type="application/json" dwingt Gemini om correcte JSON terug te geven.
                gen_config = {
                    'temperature': 0.1,
                    'response_mime_type': 'application/json',
                    'max_output_tokens': GEMINI_MAX_OUTPUT_TOKENS,
                }
                try:
                    response = client.models.generate_content(
                        model=GEMINI_MODEL,
                        contents=[audio_file, prompt],
                        config=gen_config
                    )
                except Exception as model_err:
                    err_lower = str(model_err).lower()
                    if ("404" in err_lower or "not found" in err_lower or "not_found" in err_lower) and GEMINI_FALLBACK_MODEL != GEMINI_MODEL:
                        print(f"⚠️ Model '{GEMINI_MODEL}' niet beschikbaar op deze API-sleutel. Fallback naar '{GEMINI_FALLBACK_MODEL}'...")
                        response = client.models.generate_content(
                            model=GEMINI_FALLBACK_MODEL,
                            contents=[audio_file, prompt],
                            config=gen_config
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

                # Schema-controle: sla nooit een half/leeg resultaat op.
                if not isinstance(result, dict) or not (result.get("gesprek") or result.get("feedback_brieven")):
                    raise Exception("Gemini-respons mist 'gesprek'/'feedback_brieven' (retryable)")

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
                print(f"❌ EXACT ERROR (poging {attempt}/{MAX_ATTEMPTS}): {err_str}")
                is_retryable = ("429" in err_str or "RESOURCE_EXHAUSTED" in err_str or "503" in err_str
                                or "UNAVAILABLE" in err_str or "11001" in err_str or "getaddrinfo" in err_str
                                or "Connection" in err_str or "retryable" in err_str)
                if not is_retryable:
                    print(f"❌ Niet-herstelbare fout bij '{filename}': {err_str}. Bestand overgeslagen.")
                    break  # Onbekende fout: ga naar volgende bestand
                if attempt >= MAX_ATTEMPTS:
                    print(f"❌ Na {MAX_ATTEMPTS} pogingen nog steeds een fout bij '{filename}'. Bestand overgeslagen.")
                    break  # Pogingen op: niet eindeloos blijven hangen
                print(f"⏳ Tijdelijke fout of API-limiet. Even pauze (80 seconden) voordat we het opnieuw proberen...")
                time.sleep(80)

    print("\n🎉 Alle nieuwe bestanden zijn succesvol verwerkt!")

if __name__ == "__main__":
    main()
